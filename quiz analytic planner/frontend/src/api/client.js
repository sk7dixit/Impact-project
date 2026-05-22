const API_BASE = import.meta.env.VITE_API_URL || '/api';

async function request(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...options.headers },
    ...options,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.error || `Request failed: ${res.status}`);
  }
  return res.json();
}

export const api = {
  getTopics: () => request('/topics'),
  generateQuiz: (body) => request('/quiz/generate', { method: 'POST', body: JSON.stringify(body) }),
  submitQuiz: (body) => request('/quiz/submit', { method: 'POST', body: JSON.stringify(body) }),
  getFlashcards: (topic) => request(`/flashcards${topic ? `?topic=${encodeURIComponent(topic)}` : ''}`),
  getFlashcardTopics: () => request('/flashcards/topics'),
  getProgress: () => request('/analytics/progress'),
  getWeakTopics: () => request('/analytics/weak-topics'),
  getStatistics: () => request('/analytics/statistics'),
  getSchedule: (date) => request(`/planner/schedule${date ? `?date=${date}` : ''}`),
  addSchedule: (body) => request('/planner/schedule', { method: 'POST', body: JSON.stringify(body) }),
  updateSchedule: (id, body) =>
    request(`/planner/schedule/${id}`, { method: 'PATCH', body: JSON.stringify(body) }),
  deleteSchedule: (id) => request(`/planner/schedule/${id}`, { method: 'DELETE' }),
  getPlannerProgress: () => request('/planner/progress'),
};
