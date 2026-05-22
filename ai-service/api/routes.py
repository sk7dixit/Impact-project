import os
from typing import List, Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import get_async_session
from database.queries import DocumentQueries
from database.schema import create_tables
from pdf_processing.extractor import PDFExtractor
from pdf_processing.cleaner import TextCleaner
from pdf_processing.chunker import TextChunker, TextChunk
from pdf_processing.metadata import MetadataExtractor
from embeddings.embedding_model import EmbeddingModel
from embeddings.pgvector_store import PgVectorStore
from database.schema import DocumentChunk
from utils.logger import get_logger
from utils.helpers import generate_unique_filename, clean_filename, safe_get
from utils.validators import validate_pdf_file, ValidationError

logger = get_logger(__name__)

router = APIRouter(prefix="/api", tags=["Core"])


@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "AI Exam Assistant Service",
        "version": "1.0.0",
    }


@router.post("/upload-pdf")
async def upload_pdf(
    file: UploadFile = File(...),
    user_id: str = Form(...),
    subject: Optional[str] = Form(None),
    title: Optional[str] = Form(None),
    session: AsyncSession = Depends(get_async_session),
):
    try:
        if not file.filename or not file.filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only PDF files are supported",
            )

        upload_dir = os.getenv("UPLOAD_DIR", "uploads")
        os.makedirs(upload_dir, exist_ok=True)

        safe_filename = clean_filename(file.filename)
        unique_filename = generate_unique_filename(safe_filename)
        file_path = os.path.join(upload_dir, unique_filename)

        content = await file.read()
        if len(content) > 50 * 1024 * 1024:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File size exceeds 50MB limit",
            )

        with open(file_path, "wb") as f:
            f.write(content)

        validate_pdf_file(file_path)

        doc_queries = DocumentQueries(session)
        metadata_extractor = MetadataExtractor()

        doc = await doc_queries.create_document(
            user_id=user_id,
            filename=unique_filename,
            file_path=file_path,
            file_size=len(content),
            file_type="application/pdf",
            title=title or safe_filename,
            subject=subject or metadata_extractor.extract_subject_from_filename(safe_filename),
            status="uploaded",
        )

        logger.info(f"PDF uploaded: id={doc.id}, filename={unique_filename}")

        return {
            "success": True,
            "document_id": doc.id,
            "filename": unique_filename,
            "original_filename": safe_filename,
            "file_size": len(content),
            "status": "uploaded",
            "message": "PDF uploaded successfully",
        }

    except ValidationError as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        if "file_path" in locals() and os.path.exists(file_path):
            os.remove(file_path)
        logger.error(f"Upload failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Upload failed: {str(e)}",
        )


@router.post("/extract-text")
async def extract_text(
    document_id: int = Form(...),
    user_id: str = Form(...),
    session: AsyncSession = Depends(get_async_session),
):
    doc_queries = DocumentQueries(session)
    doc = await doc_queries.get_document(document_id)

    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    if doc.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    if doc.status != "uploaded":
        raise HTTPException(status_code=400, detail=f"Document status is '{doc.status}', expected 'uploaded'")

    try:
        extractor = PDFExtractor()
        result = extractor.extract(doc.file_path)

        cleaner = TextCleaner()
        cleaned_text = cleaner.clean(result.text)

        await doc_queries.update_document_status(
            document_id=doc.id,
            status="extracted",
            page_count=result.page_count,
            raw_text=result.text[:50000],
            cleaned_text=cleaned_text[:50000],
        )

        logger.info(f"Text extracted: document_id={doc.id}, pages={result.page_count}")

        return {
            "success": True,
            "document_id": doc.id,
            "page_count": result.page_count,
            "total_characters": len(result.text),
            "cleaned_characters": len(cleaned_text),
            "status": "extracted",
            "metadata": result.metadata,
        }

    except Exception as e:
        logger.error(f"Text extraction failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Text extraction failed: {str(e)}",
        )


@router.post("/generate-embeddings")
async def generate_embeddings(
    document_id: int = Form(...),
    user_id: str = Form(...),
    session: AsyncSession = Depends(get_async_session),
):
    doc_queries = DocumentQueries(session)
    doc = await doc_queries.get_document(document_id)

    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    if doc.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    if doc.status not in ("extracted", "chunked"):
        raise HTTPException(status_code=400, detail=f"Invalid document status: {doc.status}")

    try:
        extractor = PDFExtractor()
        result = extractor.extract(doc.file_path)

        cleaner = TextCleaner()
        cleaned_text = cleaner.clean(result.text)

        chunker = TextChunker()
        chunks = chunker.chunk_text(cleaned_text, pages=result.pages)

        from database.schema import DocumentChunk as DBSchema
        db_chunks = []
        for chunk in chunks:
            db_chunks.append(DBSchema(
                document_id=doc.id,
                chunk_index=chunk.chunk_index,
                chunk_text=chunk.text,
                chunk_size=len(chunk.text),
                page_number=chunk.page_number,
                heading=chunk.heading,
                metadata_json=chunk.metadata,
            ))

        session.add_all(db_chunks)
        await session.flush()

        embedding_model = EmbeddingModel()
        texts = [c.text for c in chunks]

        logger.info(f"Generating embeddings for {len(texts)} chunks...")
        embeddings = embedding_model.encode_batch(texts)

        vector_store = PgVectorStore(session)
        for i, (chunk, embedding) in enumerate(zip(db_chunks, embeddings)):
            embedding_list = embedding.tolist() if hasattr(embedding, "tolist") else list(embedding)
            await vector_store.store_embedding(
                document_id=doc.id,
                chunk_id=chunk.id,
                text=chunk.chunk_text,
                embedding=embedding_list,
            )

        await doc_queries.update_document_status(
            document_id=doc.id,
            status="ready",
            total_chunks=len(chunks),
        )

        logger.info(f"Embeddings generated: document_id={doc.id}, chunks={len(chunks)}")

        return {
            "success": True,
            "document_id": doc.id,
            "total_chunks": len(chunks),
            "embedding_dimension": embedding_model.dimension,
            "status": "ready",
            "message": "Embeddings generated and stored successfully",
        }

    except Exception as e:
        await doc_queries.update_document_status(document_id=doc.id, status="error")
        logger.error(f"Embedding generation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Embedding generation failed: {str(e)}",
        )


@router.get("/document-status/{document_id}")
async def document_status(
    document_id: int,
    user_id: str = Query(...),
    session: AsyncSession = Depends(get_async_session),
):
    doc_queries = DocumentQueries(session)
    doc = await doc_queries.get_document(document_id)

    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    if doc.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    return {
        "document_id": doc.id,
        "filename": doc.filename,
        "title": doc.title,
        "subject": doc.subject,
        "status": doc.status,
        "page_count": doc.page_count,
        "total_chunks": doc.total_chunks,
        "file_size": doc.file_size,
        "created_at": doc.created_at.isoformat(),
        "updated_at": doc.updated_at.isoformat(),
    }


@router.get("/documents")
async def list_documents(
    user_id: str = Query(...),
    status: Optional[str] = Query(None),
    limit: int = Query(50, le=100),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_async_session),
):
    doc_queries = DocumentQueries(session)
    docs = await doc_queries.get_user_documents(
        user_id=user_id, status=status, limit=limit, offset=offset
    )

    return {
        "total": len(docs),
        "documents": [
            {
                "id": d.id,
                "filename": d.filename,
                "title": d.title,
                "subject": d.subject,
                "status": d.status,
                "page_count": d.page_count,
                "total_chunks": d.total_chunks,
                "file_size": d.file_size,
                "created_at": d.created_at.isoformat(),
            }
            for d in docs
        ],
    }


@router.delete("/documents/{document_id}")
async def delete_document(
    document_id: int,
    user_id: str = Query(...),
    session: AsyncSession = Depends(get_async_session),
):
    doc_queries = DocumentQueries(session)
    doc = await doc_queries.get_document(document_id)

    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    if doc.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    if os.path.exists(doc.file_path):
        os.remove(doc.file_path)

    await doc_queries.delete_document(document_id)

    return {"success": True, "message": "Document deleted successfully"}


@router.post("/process-pdf")
async def process_pdf_full_pipeline(
    file: UploadFile = File(...),
    user_id: str = Form(...),
    subject: Optional[str] = Form(None),
    title: Optional[str] = Form(None),
    session: AsyncSession = Depends(get_async_session),
):
    try:
        if not file.filename or not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")

        upload_dir = os.getenv("UPLOAD_DIR", "uploads")
        os.makedirs(upload_dir, exist_ok=True)

        safe_filename = clean_filename(file.filename)
        unique_filename = generate_unique_filename(safe_filename)
        file_path = os.path.join(upload_dir, unique_filename)

        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)

        validate_pdf_file(file_path)

        doc_queries = DocumentQueries(session)
        metadata_extractor = MetadataExtractor()
        extractor = PDFExtractor()
        cleaner = TextCleaner()
        chunker = TextChunker()
        embedding_model = EmbeddingModel()

        doc = await doc_queries.create_document(
            user_id=user_id,
            filename=unique_filename,
            file_path=file_path,
            file_size=len(content),
            file_type="application/pdf",
            title=title or safe_filename,
            subject=subject or metadata_extractor.extract_subject_from_filename(safe_filename),
            status="processing",
        )

        extraction = extractor.extract(file_path)
        cleaned = cleaner.clean(extraction.text)
        chunks = chunker.chunk_text(cleaned, pages=extraction.pages)

        await doc_queries.update_document_status(
            document_id=doc.id,
            status="chunked",
            page_count=extraction.page_count,
            total_chunks=len(chunks),
        )

        from database.schema import DocumentChunk as DBSchema
        db_chunks = []
        for chunk in chunks:
            db_chunks.append(DBSchema(
                document_id=doc.id,
                chunk_index=chunk.chunk_index,
                chunk_text=chunk.text,
                chunk_size=len(chunk.text),
                page_number=chunk.page_number,
                heading=chunk.heading,
            ))

        session.add_all(db_chunks)
        await session.flush()

        texts = [c.text for c in chunks]
        embeddings = embedding_model.encode_batch(texts)

        vector_store = PgVectorStore(session)
        for i, (chunk, embedding) in enumerate(zip(db_chunks, embeddings)):
            embedding_list = embedding.tolist() if hasattr(embedding, "tolist") else list(embedding)
            await vector_store.store_embedding(
                document_id=doc.id,
                chunk_id=chunk.id,
                text=chunk.chunk_text,
                embedding=embedding_list,
            )

        await doc_queries.update_document_status(
            document_id=doc.id,
            status="ready",
        )

        return {
            "success": True,
            "document_id": doc.id,
            "filename": unique_filename,
            "status": "ready",
            "page_count": extraction.page_count,
            "total_chunks": len(chunks),
            "total_characters": len(cleaned),
            "message": "PDF processed successfully through full pipeline",
        }

    except ValidationError as e:
        if "file_path" in locals() and os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        if "file_path" in locals() and os.path.exists(file_path):
            os.remove(file_path)
        if "doc" in locals():
            await doc_queries.update_document_status(document_id=doc.id, status="error")
        logger.error(f"Pipeline processing failed: {e}")
        raise HTTPException(status_code=500, detail=f"Pipeline processing failed: {str(e)}")
