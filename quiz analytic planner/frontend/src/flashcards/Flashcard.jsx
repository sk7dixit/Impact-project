import { SUBJECT_MAP } from '../data/subjects';

export default function Flashcard({ card, flipped, onFlip }) {
  const subject = SUBJECT_MAP[card.topic];

  return (
    <button
      type="button"
      className={`flashcard ${flipped ? 'flashcard--flipped' : ''}`}
      onClick={onFlip}
      aria-label={flipped ? 'Show question' : 'Show answer'}
    >
      <div className="flashcard__inner">
        <div className="flashcard__face flashcard__face--front">
          <span
            className="flashcard__topic topic-pill"
            style={subject ? { background: subject.gradient } : undefined}
          >
            {subject ? `${subject.icon} ${card.topic}` : card.topic}
          </span>
          <p className="flashcard__text">{card.front}</p>
          <span className="flashcard__hint">Tap to flip</span>
        </div>
        <div className="flashcard__face flashcard__face--back">
          <span
            className="flashcard__topic topic-pill"
            style={subject ? { background: subject.gradient } : undefined}
          >
            {subject ? `${subject.icon} ${card.topic}` : card.topic}
          </span>
          <p className="flashcard__text">{card.back}</p>
          <span className="flashcard__hint">Tap to flip back</span>
        </div>
      </div>
    </button>
  );
}
