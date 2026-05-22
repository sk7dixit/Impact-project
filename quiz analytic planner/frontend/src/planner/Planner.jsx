import { useCallback, useEffect, useState } from 'react';
import { api } from '../api/client';
import { SUBJECTS } from '../data/subjects';
import ScheduleCard from './ScheduleCard';

export default function Planner() {
  const today = new Date().toISOString().split('T')[0];
  const [selectedDate, setSelectedDate] = useState(today);
  const [schedule, setSchedule] = useState([]);
  const [progress, setProgress] = useState(null);
  const [form, setForm] = useState({ time: '09:00', subject: 'OOPS', duration: 45 });
  const [loading, setLoading] = useState(true);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const [items, prog] = await Promise.all([
        api.getSchedule(selectedDate),
        api.getPlannerProgress(),
      ]);
      setSchedule(items);
      setProgress(prog);
    } catch {
      setSchedule([]);
    } finally {
      setLoading(false);
    }
  }, [selectedDate]);

  useEffect(() => {
    load();
  }, [load]);

  const handleAdd = async (e) => {
    e.preventDefault();
    if (!form.subject.trim()) return;
    await api.addSchedule({
      date: selectedDate,
      time: form.time,
      subject: form.subject,
      duration: Number(form.duration),
    });
    setForm((f) => ({ ...f, time: '09:00', duration: 45 }));
    load();
  };

  const handleToggle = async (id, completed) => {
    await api.updateSchedule(id, { completed });
    load();
  };

  const handleDelete = async (id) => {
    await api.deleteSchedule(id);
    load();
  };

  return (
    <div className="page planner-page">
      <header className="page-header">
        <h1>Study Planner</h1>
        <p>Schedule sessions for OOPS, DAA, Python, DBMS, DSA, ML, Aptitude, Communication, AI & Cyber.</p>
      </header>

      {progress && (
        <div className="planner-progress card">
          <div className="planner-progress__stat">
            <span className="value">{progress.completionRate}%</span>
            <span className="label">Overall completion</span>
          </div>
          <div className="planner-progress__stat">
            <span className="value">
              {progress.todayCompleted}/{progress.todayTotal}
            </span>
            <span className="label">Today&apos;s sessions</span>
          </div>
          <div className="planner-progress__stat">
            <span className="value">{progress.completedSessions}</span>
            <span className="label">Sessions completed</span>
          </div>
        </div>
      )}

      <div className="planner-layout">
        <section className="card planner-form-section">
          <label className="planner-date-label">
            Select day
            <input
              type="date"
              value={selectedDate}
              onChange={(e) => setSelectedDate(e.target.value)}
            />
          </label>
          <h2>Add session</h2>
          <form className="planner-form" onSubmit={handleAdd}>
            <label>
              Time
              <input
                type="time"
                value={form.time}
                onChange={(e) => setForm((f) => ({ ...f, time: e.target.value }))}
              />
            </label>
            <label>
              Subject
              <select
                value={form.subject}
                onChange={(e) => setForm((f) => ({ ...f, subject: e.target.value }))}
              >
                {SUBJECTS.map((s) => (
                  <option key={s.id} value={s.id}>
                    {s.icon} {s.name} — {s.fullName}
                  </option>
                ))}
              </select>
            </label>
            <label>
              Duration (minutes)
              <input
                type="number"
                min={15}
                max={180}
                value={form.duration}
                onChange={(e) => setForm((f) => ({ ...f, duration: e.target.value }))}
              />
            </label>
            <button type="submit" className="btn btn--primary">
              Add to schedule
            </button>
          </form>
        </section>

        <section className="card planner-schedule-section">
          <h2>Schedule — {selectedDate}</h2>
          {loading && <p className="loading">Loading schedule…</p>}
          {!loading && schedule.length === 0 && (
            <p className="empty">No sessions planned for this day.</p>
          )}
          <ul className="schedule-list">
            {schedule.map((item) => (
              <li key={item.id}>
                <ScheduleCard item={item} onToggle={handleToggle} onDelete={handleDelete} />
              </li>
            ))}
          </ul>
        </section>
      </div>
    </div>
  );
}
