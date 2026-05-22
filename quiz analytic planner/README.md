# AI Exam Preparation Assistant — Member 4 Modules

Quiz, Flashcards, Analytics, and Study Planner for the team project.

## Structure

```
frontend/src/
├── quiz/          QuizPage, QuizCard, QuizResult, Timer
├── flashcards/    Flashcard, FlashcardPage
├── analytics/     ProgressChart, WeakTopics, Statistics, AnalyticsPage
└── planner/       Planner, ScheduleCard

backend/
└── server.js      Express APIs
```

## Run locally

**Terminal 1 — API (port 5000):**
```bash
cd backend
npm start
```

**Terminal 2 — Frontend (port 5173):**
```bash
cd frontend
npm run dev
```

Open http://localhost:5173

## API endpoints

| Module | Endpoint | Method |
|--------|----------|--------|
| Quiz | `/api/quiz/generate` | POST |
| Quiz | `/api/quiz/submit` | POST |
| Flashcards | `/api/flashcards` | GET |
| Analytics | `/api/analytics/progress` | GET |
| Analytics | `/api/analytics/weak-topics` | GET |
| Analytics | `/api/analytics/statistics` | GET |
| Planner | `/api/planner/schedule` | GET, POST |
| Planner | `/api/planner/schedule/:id` | PATCH, DELETE |
| Planner | `/api/planner/progress` | GET |

## Features (Member 4)

- **Quiz:** MCQ generation UI, timed attempts, navigation dots, score calculation
- **Flashcards:** 3D flip animation, topic filter, prev/next revision navigation
- **Analytics:** Recharts progress line chart, weak topic bars, quiz statistics table
- **Planner:** Daily schedule UI, add/complete/delete sessions, progress tracking
