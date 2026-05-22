export default function Statistics({ stats }) {
  if (!stats) return <p className="loading">Loading statistics…</p>;

  const cards = [
    { label: 'Total Quizzes', value: stats.totalQuizzes },
    { label: 'Average Score', value: `${stats.averageScore}%` },
    { label: 'Best Score', value: `${stats.bestScore}%` },
    { label: 'Accuracy', value: `${stats.accuracy}%` },
  ];

  return (
    <div className="statistics">
      <div className="stat-grid">
        {cards.map((c) => (
          <div key={c.label} className="stat-card">
            <span className="stat-card__value">{c.value}</span>
            <span className="stat-card__label">{c.label}</span>
          </div>
        ))}
      </div>
      {stats.recentAttempts?.length > 0 && (
        <div className="recent-attempts">
          <h3>Recent Attempts</h3>
          <table>
            <thead>
              <tr>
                <th>Date</th>
                <th>Topic</th>
                <th>Score</th>
              </tr>
            </thead>
            <tbody>
              {stats.recentAttempts.map((a, i) => (
                <tr key={`${a.date}-${i}`}>
                  <td>{a.date}</td>
                  <td>{a.topic}</td>
                  <td>{a.score}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
