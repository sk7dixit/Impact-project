import { SUBJECT_MAP } from '../data/subjects';

export default function WeakTopics({ topics }) {
  if (!topics?.length) {
    return <p className="empty">Take more quizzes to identify weak subjects.</p>;
  }

  return (
    <ul className="weak-topics">
      {topics.map((item) => {
        const level =
          item.avgScore < 50 ? 'critical' : item.avgScore < 70 ? 'moderate' : 'ok';
        const subject = SUBJECT_MAP[item.topic];
        return (
          <li key={item.topic} className={`weak-topics__item weak-topics__item--${level}`}>
            <div className="weak-topics__header">
              <span className="weak-topics__name">
                {subject && <span className="weak-topics__icon">{subject.icon}</span>}
                {item.topic}
              </span>
              <span className="weak-topics__score">{item.avgScore}% avg</span>
            </div>
            <div className="weak-topics__bar-track">
              <div
                className="weak-topics__bar-fill"
                style={{
                  width: `${item.avgScore}%`,
                  background: subject?.gradient || undefined,
                }}
              />
            </div>
            <span className="weak-topics__meta">{item.attempts} attempt(s)</span>
          </li>
        );
      })}
    </ul>
  );
}
