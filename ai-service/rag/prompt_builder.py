from typing import Dict, List, Optional

from utils.logger import get_logger

logger = get_logger(__name__)


class PromptBuilder:
    SYSTEM_PROMPTS = {
        "qa": (
            "You are an AI exam preparation assistant. Your role is to help students "
            "understand concepts, answer questions, and prepare for exams based on "
            "their study materials.\n\n"
            "Guidelines:\n"
            "- Answer based ONLY on the provided context\n"
            "- If the context doesn't contain enough information, say so clearly\n"
            "- Be concise but thorough in your explanations\n"
            "- Use examples where helpful\n"
            "- Structure your answers for easy understanding\n"
            "- Cite the source document and page when referencing material\n"
            "- Do NOT make up information or hallucinate"
        ),
        "summary": (
            "You are an AI study assistant specializing in creating clear, "
            "concise summaries of educational content.\n\n"
            "Guidelines:\n"
            "- Extract the most important concepts and key points\n"
            "- Organize information logically\n"
            "- Use bullet points and headings for clarity\n"
            "- Keep summaries focused on exam-relevant content\n"
            "- Include important definitions, formulas, and dates\n"
            "- Highlight key terms and concepts"
        ),
        "quiz": (
            "You are an AI quiz generator for educational content. Create "
            "high-quality assessment questions based on the provided study material.\n\n"
            "Guidelines:\n"
            "- Questions should test understanding, not just recall\n"
            "- Distractors should be plausible but incorrect\n"
            "- Include clear correct answers\n"
            "- Provide explanations for each answer\n"
            "- Match difficulty level as requested\n"
            "- Cover diverse topics from the material"
        ),
        "flashcard": (
            "You are an AI flashcard creator for exam preparation. Create "
            "effective question-answer pairs that help with memorization.\n\n"
            "Guidelines:\n"
            "- Each card should cover ONE concept\n"
            "- Questions should be clear and specific\n"
            "- Answers should be concise but complete\n"
            "- Include brief explanations where helpful\n"
            "- Focus on important exam-relevant content\n"
            "- Use simple language for easy recall"
        ),
    }

    QA_TEMPLATE = """Context Information:
{context}

---
User Question: {question}

Please answer the question based on the provided context. If the context doesn't contain enough information to answer the question fully, acknowledge this and provide what you can from the context.
"""

    SUMMARY_TEMPLATE = """Content to Summarize:
{context}

---
Summary Type: {summary_type}
Focus Area: {focus_area}

Please generate a {summary_type} summary covering the key points from the content above. Focus on exam-relevant information.
"""

    QUIZ_TEMPLATE = """Study Material:
{context}

---
Quiz Configuration:
- Type: {quiz_type}
- Difficulty: {difficulty}
- Number of Questions: {num_questions}
- Topics: {topics}

Generate {num_questions} {quiz_type} questions at {difficulty} difficulty level based on the study material above.
"""

    FLASHCARD_TEMPLATE = """Study Material:
{context}

---
Flashcard Configuration:
- Number of Cards: {num_cards}
- Focus Topics: {topics}
- Difficulty: {difficulty}

Generate {num_cards} flashcards in question-answer format based on the study material above.
"""

    def __init__(self):
        self.system_prompts = self.SYSTEM_PROMPTS

    def build_qa_prompt(
        self,
        context: str,
        question: str,
        system_override: Optional[str] = None,
    ) -> List[Dict[str, str]]:
        messages = [
            {"role": "system", "content": system_override or self.system_prompts["qa"]},
            {"role": "user", "content": self.QA_TEMPLATE.format(
                context=context, question=question
            )},
        ]
        return messages

    def build_summary_prompt(
        self,
        context: str,
        summary_type: str = "chapter",
        focus_area: str = "general",
        system_override: Optional[str] = None,
    ) -> List[Dict[str, str]]:
        messages = [
            {
                "role": "system",
                "content": system_override or self.system_prompts["summary"],
            },
            {
                "role": "user",
                "content": self.SUMMARY_TEMPLATE.format(
                    context=context,
                    summary_type=summary_type,
                    focus_area=focus_area,
                ),
            },
        ]
        return messages

    def build_quiz_prompt(
        self,
        context: str,
        quiz_type: str = "multiple_choice",
        difficulty: str = "medium",
        num_questions: int = 10,
        topics: str = "general",
        system_override: Optional[str] = None,
    ) -> List[Dict[str, str]]:
        messages = [
            {
                "role": "system",
                "content": system_override or self.system_prompts["quiz"],
            },
            {
                "role": "user",
                "content": self.QUIZ_TEMPLATE.format(
                    context=context,
                    quiz_type=quiz_type,
                    difficulty=difficulty,
                    num_questions=num_questions,
                    topics=topics,
                ),
            },
        ]
        return messages

    def build_flashcard_prompt(
        self,
        context: str,
        num_cards: int = 10,
        topics: str = "general",
        difficulty: str = "medium",
        system_override: Optional[str] = None,
    ) -> List[Dict[str, str]]:
        messages = [
            {
                "role": "system",
                "content": system_override or self.system_prompts["flashcard"],
            },
            {
                "role": "user",
                "content": self.FLASHCARD_TEMPLATE.format(
                    context=context,
                    num_cards=num_cards,
                    topics=topics,
                    difficulty=difficulty,
                ),
            },
        ]
        return messages

    def build_chat_prompt(
        self,
        context: str,
        question: str,
        chat_history: Optional[List[Dict[str, str]]] = None,
    ) -> List[Dict[str, str]]:
        messages = [
            {"role": "system", "content": self.system_prompts["qa"]},
        ]

        if chat_history:
            for msg in chat_history[-10:]:
                messages.append(msg)

        context_message = f"Relevant Context:\n{context}\n\n---\n\nUser Question: {question}"
        messages.append({"role": "user", "content": context_message})

        return messages
