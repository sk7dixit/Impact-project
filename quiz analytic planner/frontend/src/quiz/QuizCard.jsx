import { SUBJECT_MAP } from '../data/subjects';

export default function QuizCard({
  question,
  questionNumber,
  totalQuestions,
  selectedIndex,
  onSelect,
  disabled = false,
}) {
  const subject = question.topic ? SUBJECT_MAP[question.topic] : null;

  return (
    <article className="quiz-card card">
      <header className="quiz-card__header">
        <span className="quiz-card__badge">
          Question {questionNumber} / {totalQuestions}
        </span>
        {subject && (
          <span
            className="quiz-card__topic topic-pill"
            style={{ background: subject.gradient }}
          >
            {subject.icon} {question.topic}
          </span>
        )}
        {!subject && question.topic && (
          <span className="quiz-card__topic">{question.topic}</span>
        )}
      </header>
      <h2 className="quiz-card__question">{question.question}</h2>
      <ul className="quiz-card__options">
        {question.options.map((option, index) => {
          const selected = selectedIndex === index;
          return (
            <li key={index}>
              <button
                type="button"
                className={`quiz-card__option ${selected ? 'quiz-card__option--selected' : ''}`}
                onClick={() => onSelect(index)}
                disabled={disabled}
              >
                <span className="quiz-card__option-letter">
                  {String.fromCharCode(65 + index)}
                </span>
                <span>{option}</span>
              </button>
            </li>
          );
        })}
      </ul>
    </article>
  );
}
