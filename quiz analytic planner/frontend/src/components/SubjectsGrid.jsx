import { SUBJECTS } from '../data/subjects';

export default function SubjectsGrid({
  selected = '',
  onSelect,
  compact = false,
  showAllOption = true,
}) {
  return (
    <div className={`subjects-grid ${compact ? 'subjects-grid--compact' : ''}`}>
      {showAllOption && onSelect && (
        <button
          type="button"
          className={`subject-card subject-card--all ${selected === '' ? 'subject-card--active' : ''}`}
          onClick={() => onSelect('')}
        >
          <span className="subject-card__icon">✨</span>
          <span className="subject-card__name">All Subjects</span>
          {!compact && <span className="subject-card__desc">Mixed practice quiz</span>}
        </button>
      )}
      {SUBJECTS.map((subject) => (
        <button
          key={subject.id}
          type="button"
          className={`subject-card ${selected === subject.id ? 'subject-card--active' : ''}`}
          style={{ '--subject-accent': subject.color, '--subject-gradient': subject.gradient }}
          onClick={() => onSelect?.(subject.id)}
          disabled={!onSelect}
        >
          <span className="subject-card__icon">{subject.icon}</span>
          <span className="subject-card__name">{subject.name}</span>
          {!compact && <span className="subject-card__desc">{subject.fullName}</span>}
        </button>
      ))}
    </div>
  );
}
