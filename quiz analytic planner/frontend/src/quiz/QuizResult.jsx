export default function QuizResult({ score, correct, total, breakdown, onRetry, onHome }) {
  const passed = score >= 60;
  const grade =
    score >= 90 ? 'A' : score >= 80 ? 'B' : score >= 70 ? 'C' : score >= 60 ? 'D' : 'F';

  return (
    <section className="quiz-result">
      <div className={`quiz-result__circle ${passed ? 'quiz-result__circle--pass' : 'quiz-result__circle--fail'}`}>
        <span className="quiz-result__score">{score}%</span>
        <span className="quiz-result__grade">Grade {grade}</span>
      </div>
      <p className="quiz-result__summary">
        You answered <strong>{correct}</strong> out of <strong>{total}</strong> correctly.
      </p>
      {breakdown?.length > 0 && (
        <ul className="quiz-result__breakdown">
          {breakdown.map((item, i) => (
            <li key={item.questionId} className={item.correct ? 'correct' : 'incorrect'}>
              Q{i + 1}: {item.correct ? 'Correct' : 'Incorrect'}
            </li>
          ))}
        </ul>
      )}
      <div className="quiz-result__actions">
        <button type="button" className="btn btn--primary" onClick={onRetry}>
          Try Again
        </button>
        <button type="button" className="btn btn--ghost" onClick={onHome}>
          Back to Quiz Setup
        </button>
      </div>
    </section>
  );
}
