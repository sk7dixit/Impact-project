import os
from datetime import datetime

from dotenv import load_dotenv
from pgvector.sqlalchemy import Vector
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Float,
    JSON,
    Boolean,
    ForeignKey,
    Index,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs

load_dotenv()

VECTOR_DIMENSION = int(os.getenv("VECTOR_DIMENSION", "768"))


class Base(AsyncAttrs, DeclarativeBase):
    pass


class UploadedDocument(Base):
    __tablename__ = "uploaded_documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    filename: Mapped[str] = mapped_column(String(500), nullable=False)
    file_path: Mapped[str] = mapped_column(String(1000), nullable=False)
    file_size: Mapped[int] = mapped_column(Integer, nullable=False)
    file_type: Mapped[str] = mapped_column(String(100), nullable=False)
    page_count: Mapped[int] = mapped_column(Integer, default=0)
    total_chunks: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(
        String(50), default="uploaded", index=True
    )
    title: Mapped[str] = mapped_column(String(500), nullable=True)
    subject: Mapped[str] = mapped_column(String(255), nullable=True)
    raw_text: mapped_column = Column(Text, nullable=True)
    cleaned_text: mapped_column = Column(Text, nullable=True)
    metadata_json: mapped_column = Column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    chunks = relationship(
        "DocumentChunk", back_populates="document", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("idx_documents_user_status", "user_id", "status"),
        Index("idx_documents_created", "created_at"),
    )

    def __repr__(self) -> str:
        return f"<UploadedDocument(id={self.id}, filename='{self.filename}', status='{self.status}')>"


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    document_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("uploaded_documents.id", ondelete="CASCADE"), nullable=False
    )
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    chunk_text: mapped_column = Column(Text, nullable=False)
    chunk_size: Mapped[int] = mapped_column(Integer, default=0)
    page_number: Mapped[int] = mapped_column(Integer, nullable=True)
    heading: Mapped[str] = mapped_column(String(500), nullable=True)
    embedding: mapped_column = Column(Vector(VECTOR_DIMENSION), nullable=True)
    metadata_json: mapped_column = Column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    document = relationship("UploadedDocument", back_populates="chunks")

    __table_args__ = (
        Index("idx_chunks_document", "document_id"),
        Index(
            "idx_chunks_embedding",
            "embedding",
            postgresql_using="ivfflat",
            postgresql_with={"lists": 100},
        ),
        UniqueConstraint("document_id", "chunk_index", name="uq_document_chunk"),
    )

    def __repr__(self) -> str:
        return f"<DocumentChunk(id={self.id}, document_id={self.document_id}, index={self.chunk_index})>"


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    session_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    subject: Mapped[str] = mapped_column(String(255), nullable=True)
    document_ids: mapped_column = Column(JSON, default=list)
    role: Mapped[str] = mapped_column(String(50), nullable=False)
    content: mapped_column = Column(Text, nullable=False)
    source_chunks: mapped_column = Column(JSON, nullable=True)
    metadata_json: mapped_column = Column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    __table_args__ = (
        Index("idx_chat_user_session", "user_id", "session_id"),
        Index("idx_chat_created", "created_at"),
    )

    def __repr__(self) -> str:
        return f"<ChatHistory(id={self.id}, role='{self.role}', session='{self.session_id}')>"


class GeneratedQuiz(Base):
    __tablename__ = "generated_quizzes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    document_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("uploaded_documents.id", ondelete="SET NULL"), nullable=True
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    subject: Mapped[str] = mapped_column(String(255), nullable=True)
    quiz_type: Mapped[str] = mapped_column(
        String(50), nullable=False, default="multiple_choice"
    )
    difficulty: Mapped[str] = mapped_column(
        String(50), nullable=False, default="medium"
    )
    quiz_data: mapped_column = Column(JSON, nullable=False)
    total_questions: Mapped[int] = mapped_column(Integer, default=0)
    metadata_json: mapped_column = Column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    __table_args__ = (Index("idx_quiz_user", "user_id"),)

    def __repr__(self) -> str:
        return f"<GeneratedQuiz(id={self.id}, title='{self.title}', type='{self.quiz_type}')>"


class Flashcard(Base):
    __tablename__ = "flashcards"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    document_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("uploaded_documents.id", ondelete="SET NULL"), nullable=True
    )
    set_name: Mapped[str] = mapped_column(String(500), nullable=False)
    subject: Mapped[str] = mapped_column(String(255), nullable=True)
    question: mapped_column = Column(Text, nullable=False)
    answer: mapped_column = Column(Text, nullable=False)
    explanation: mapped_column = Column(Text, nullable=True)
    difficulty: Mapped[str] = mapped_column(
        String(50), nullable=False, default="medium"
    )
    metadata_json: mapped_column = Column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    __table_args__ = (Index("idx_flashcard_user", "user_id"),)

    def __repr__(self) -> str:
        return f"<Flashcard(id={self.id}, set='{self.set_name}')>"


class GeneratedSummary(Base):
    __tablename__ = "generated_summaries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    document_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("uploaded_documents.id", ondelete="SET NULL"), nullable=True
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    subject: Mapped[str] = mapped_column(String(255), nullable=True)
    summary_type: Mapped[str] = mapped_column(String(50), nullable=False, default="chapter")
    summary_text: mapped_column = Column(Text, nullable=False)
    key_points: mapped_column = Column(JSON, default=list)
    word_count: Mapped[int] = mapped_column(Integer, default=0)
    metadata_json: mapped_column = Column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    __table_args__ = (Index("idx_summary_user", "user_id"),)

    def __repr__(self) -> str:
        return f"<GeneratedSummary(id={self.id}, title='{self.title}')>"


metadata = Base.metadata


async def create_tables():
    from database.connection import db_manager

    async with db_manager.async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    from utils.logger import get_logger
    logger = get_logger(__name__)
    logger.info("All database tables created successfully")


async def drop_tables():
    from database.connection import db_manager

    async with db_manager.async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    from utils.logger import get_logger
    logger = get_logger(__name__)
    logger.warning("All database tables dropped")
