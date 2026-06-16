import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from database.connection import db_manager
from database.schema import create_tables
from utils.logger import get_logger

load_dotenv()

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    logger.info("Starting AI Exam Assistant Service...")
    await db_manager.initialize()
    await create_tables()
    logger.info("Service started successfully")
    yield
    logger.info("Shutting down AI Exam Assistant Service...")
    await db_manager.close()
    logger.info("Service shut down")


app = FastAPI(
    title="AI Exam Preparation Assistant",
    description="Production-ready AI service for exam preparation with PDF processing, RAG pipeline, semantic search, and AI-powered features",
    version="1.0.0",
    lifespan=lifespan,
)

origins_str = os.getenv("CORS_ORIGINS", '["http://localhost:5173","http://localhost:3000"]')
try:
    import json
    origins = json.loads(origins_str)
except (json.JSONDecodeError, TypeError):
    origins = ["http://localhost:5173", "http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"success": False, "detail": "Internal server error", "error": str(exc)},
    )


from api.routes import router as main_router
from api.chat_routes import router as chat_router
from api.quiz_routes import router as quiz_router
from api.flashcard_routes import router as flashcard_router
from api.summary_routes import router as summary_router

app.include_router(main_router)
app.include_router(chat_router)
app.include_router(quiz_router)
app.include_router(flashcard_router)
app.include_router(summary_router)


@app.get("/")
async def root():
    return {
        "service": "AI Exam Preparation Assistant",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "GET /api/health",
            "upload_pdf": "POST /api/upload-pdf",
            "extract_text": "POST /api/extract-text",
            "generate_embeddings": "POST /api/generate-embeddings",
            "process_pdf": "POST /api/process-pdf",
            "documents": "GET /api/documents",
            "document_status": "GET /api/document-status/{id}",
            "chat": "POST /api/chat",
            "chat_history": "GET /api/chat/history",
            "chat_sessions": "GET /api/chat/sessions",
            "generate_quiz": "POST /api/quiz/generate",
            "list_quizzes": "GET /api/quiz/list",
            "generate_flashcards": "POST /api/flashcards/generate",
            "list_flashcards": "GET /api/flashcards/list",
            "flashcard_sets": "GET /api/flashcards/sets",
            "generate_summary": "POST /api/summaries/generate",
            "list_summaries": "GET /api/summaries/list",
        },
    }


if __name__ == "__main__":
    import uvicorn

    host = os.getenv("AI_SERVICE_HOST", "0.0.0.0")
    port = int(os.getenv("AI_SERVICE_PORT", "8000"))
    debug = os.getenv("DEBUG", "true").lower() == "true"

    logger.info(f"Starting server on {host}:{port} (debug={debug})")
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info",
    )
