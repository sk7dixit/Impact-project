import { SUBJECT_MAP } from '../data/subjects';

export default function ScheduleCard({ item, onToggle, onDelete }) {
  const subject = SUBJECT_MAP[item.subject];

  return (
    <article
      className={`schedule-card ${item.completed ? 'schedule-card--done' : ''}`}
      style={subject ? { borderLeftColor: subject.color } : undefined}
    >
      <div className="schedule-card__time">
        <span className="schedule-card__clock">{item.time}</span>
        <span className="schedule-card__duration">{item.duration} min</span>
      </div>
      <div className="schedule-card__body">
        <h3>
          {subject && <span className="schedule-card__icon">{subject.icon}</span>}
          {item.subject}
        </h3>
        {subject && <span className="schedule-card__full">{subject.fullName}</span>}
        <span className="schedule-card__date">{item.date}</span>
      </div>
      <div className="schedule-card__actions">
        <button
          type="button"
          className="btn btn--small"
          onClick={() => onToggle(item.id, !item.completed)}
          aria-pressed={item.completed}
        >
          {item.completed ? 'Undo' : 'Done'}
        </button>
        <button type="button" className="btn btn--small btn--danger" onClick={() => onDelete(item.id)}>
          Remove
        </button>
      </div>
    </article>
  );
}
