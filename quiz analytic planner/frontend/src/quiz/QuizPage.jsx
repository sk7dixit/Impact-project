import { useCallback, useEffect, useState } from 'react';
import { api } from '../api/client';
import SubjectsGrid from '../components/SubjectsGrid';
import { SUBJECT_MAP } from '../data/subjects';
import QuizCard from './QuizCard';
import QuizResult from './QuizResult';
import Timer from './Timer';

const STEPS = { setup: 'setup', quiz: 'quiz', result: 'result' };

export default function QuizPage() {
  const [step, setStep] = useState(STEPS.setup);
  const [form, setForm] = useState({ topic: '', count: 5, difficulty: 'medium' });
  const [quiz, setQuiz] = useState(null);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [startTime, setStartTime] = useState(null);
  const [timerRunning, setTimerRunning] = useState(false);

  const handleGenerate = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const data = await api.generateQuiz({
        topic: form.topic || undefined,
        count: Number(form.count),
        difficulty: form.difficulty,
      });
      setQuiz(data);
      setAnswers({});
      setCurrentIndex(0);
      setStartTime(Date.now());
      setTimerRunning(true);
      setStep(STEPS.quiz);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSelect = (optionIndex) => {
    const q = quiz.questions[currentIndex];
    setAnswers((prev) => ({ ...prev, [q.id]: optionIndex }));
  };

  const handleNext = () => {
    if (currentIndex < quiz.questions.length - 1) {
      setCurrentIndex((i) => i + 1);
    }
  };

  const handlePrev = () => {
    if (currentIndex > 0) setCurrentIndex((i) => i - 1);
  };

  const submitQuiz = useCallback(async () => {
    setTimerRunning(false);
    setLoading(true);
    const timeTaken = startTime ? Math.round((Date.now() - startTime) / 1000) : 0;
    try {
      const data = await api.submitQuiz({
        answers,
        answerKey: quiz.answerKey,
        topic: quiz.topic,
        timeTaken,
      });
      setResult(data);
      setStep(STEPS.result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [answers, quiz, startTime]);

  const handleTimeExpire = useCallback(() => {
    if (step === STEPS.quiz) submitQuiz();
  }, [step, submitQuiz]);

  const reset = () => {
    setStep(STEPS.setup);
    setQuiz(null);
    setResult(null);
    setAnswers({});
    setCurrentIndex(0);
    setTimerRunning(false);
  };

  const currentQuestion = quiz?.questions[currentIndex];
  const selected = currentQuestion ? answers[currentQuestion.id] : undefined;
  const allAnswered = quiz?.questions.every((q) => answers[q.id] !== undefined);
  const selectedSubject = form.topic ? SUBJECT_MAP[form.topic] : null;

  return (
    <div className="page quiz-page">
      <header className="page-header">
        <h1>Quiz</h1>
        <p>Pick a subject, generate MCQs, and test yourself with a timer.</p>
      </header>

      {error && <p className="error-banner">{error}</p>}

      {step === STEPS.setup && (
        <form className="quiz-setup" onSubmit={handleGenerate}>
          <section className="card quiz-setup__subjects">
            <h2>Choose subject</h2>
            <p className="quiz-setup__hint">OOPS · DAA · Python · DBMS · DSA · ML · Aptitude · Communication · AI · Cyber</p>
            <SubjectsGrid
              selected={form.topic}
              onSelect={(topic) => setForm((f) => ({ ...f, topic }))}
              compact
            />
          </section>

          <section className="card quiz-setup__options">
            <h2>Quiz settings</h2>
            <div className="form-row">
              <label>
                Questions
                <input
                  type="number"
                  min={1}
                  max={20}
                  value={form.count}
                  onChange={(e) => setForm((f) => ({ ...f, count: e.target.value }))}
                />
              </label>
              <label>
                Difficulty
                <select
                  value={form.difficulty}
                  onChange={(e) => setForm((f) => ({ ...f, difficulty: e.target.value }))}
                >
                  <option value="easy">Easy — 10 min</option>
                  <option value="medium">Medium — 7.5 min</option>
                  <option value="hard">Hard — 5 min</option>
                </select>
              </label>
            </div>
            {selectedSubject && (
              <p className="quiz-setup__selected" style={{ color: selectedSubject.color }}>
                Selected: <strong>{selectedSubject.icon} {selectedSubject.fullName}</strong>
              </p>
            )}
            <button type="submit" className="btn btn--primary btn--large" disabled={loading}>
              {loading ? 'Generating…' : 'Start Quiz →'}
            </button>
          </section>
        </form>
      )}

      {step === STEPS.quiz && quiz && currentQuestion && (
        <div className="quiz-active">
          <div className="quiz-active__toolbar">
            <div className="quiz-active__meta">
              {quiz.topic !== 'Mixed' && SUBJECT_MAP[quiz.topic] && (
                <span
                  className="topic-pill"
                  style={{ background: SUBJECT_MAP[quiz.topic].gradient }}
                >
                  {SUBJECT_MAP[quiz.topic].icon} {quiz.topic}
                </span>
              )}
              <span className="quiz-active__difficulty">{quiz.difficulty} mode</span>
            </div>
            <Timer seconds={quiz.timeLimit} running={timerRunning} onExpire={handleTimeExpire} />
            <button
              type="button"
              className="btn btn--primary"
              onClick={submitQuiz}
              disabled={loading || !allAnswered}
            >
              {loading ? 'Submitting…' : 'Submit Quiz'}
            </button>
          </div>
          <QuizCard
            question={currentQuestion}
            questionNumber={currentIndex + 1}
            totalQuestions={quiz.questions.length}
            selectedIndex={selected}
            onSelect={handleSelect}
          />
          <nav className="quiz-nav">
            <button type="button" className="btn btn--ghost" onClick={handlePrev} disabled={currentIndex === 0}>
              Previous
            </button>
            <div className="quiz-dots">
              {quiz.questions.map((q, i) => (
                <button
                  key={q.id}
                  type="button"
                  className={`quiz-dot ${i === currentIndex ? 'active' : ''} ${answers[q.id] !== undefined ? 'answered' : ''}`}
                  onClick={() => setCurrentIndex(i)}
                  aria-label={`Go to question ${i + 1}`}
                />
              ))}
            </div>
            <button
              type="button"
              className="btn btn--ghost"
              onClick={handleNext}
              disabled={currentIndex === quiz.questions.length - 1}
            >
              Next
            </button>
          </nav>
        </div>
      )}

      {step === STEPS.result && result && (
        <QuizResult
          score={result.score}
          correct={result.correct}
          total={result.total}
          breakdown={result.breakdown}
          onRetry={() => {
            setStep(STEPS.quiz);
            setCurrentIndex(0);
            setAnswers({});
            setResult(null);
            setStartTime(Date.now());
            setTimerRunning(true);
          }}
          onHome={reset}
        />
      )}
    </div>
  );
}
