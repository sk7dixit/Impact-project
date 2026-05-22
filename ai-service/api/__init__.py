from api.routes import router as main_router
from api.chat_routes import router as chat_router
from api.quiz_routes import router as quiz_router
from api.flashcard_routes import router as flashcard_router
from api.summary_routes import router as summary_router

__all__ = [
    "main_router",
    "chat_router",
    "quiz_router",
    "flashcard_router",
    "summary_router",
]
