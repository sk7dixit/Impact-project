import { useEffect, useState } from 'react';
import { api } from '../api/client';
import { SUBJECTS } from '../data/subjects';
import ProgressChart from './ProgressChart';
import Statistics from './Statistics';
import WeakTopics from './WeakTopics';

export default function AnalyticsPage() {
  const [progress, setProgress] = useState([]);
  const [weakTopics, setWeakTopics] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([api.getProgress(), api.getWeakTopics(), api.getStatistics()])
      .then(([p, w, s]) => {
        setProgress(p);
        setWeakTopics(w);
        setStats(s);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p className="loading page">Loading analytics…</p>;

  return (
    <div className="page analytics-page">
      <header className="page-header">
        <h1>Analytics</h1>
        <p>Track scores across OOPS, DAA, Python, DBMS, DSA, ML, Aptitude, Communication, AI & Cyber.</p>
      </header>

      <section className="card analytics-subjects-banner">
        <p className="analytics-subjects-banner__label">Tracked subjects</p>
        <div className="analytics-subjects-banner__chips">
          {SUBJECTS.map((s) => (
            <span key={s.id} className="analytics-chip" style={{ borderColor: s.color }}>
              {s.icon} {s.name}
            </span>
          ))}
        </div>
      </section>

      <section className="card">
        <h2>Progress Over Time</h2>
        <ProgressChart data={progress} />
      </section>

      <div className="analytics-grid">
        <section className="card">
          <h2>Weak Subject Analysis</h2>
          <WeakTopics topics={weakTopics} />
        </section>
        <section className="card">
          <h2>Quiz Statistics</h2>
          <Statistics stats={stats} />
        </section>
      </div>
    </div>
  );
}
