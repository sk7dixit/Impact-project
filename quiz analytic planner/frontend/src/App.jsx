import { NavLink, Route, Routes } from 'react-router-dom';
import AnalyticsPage from './analytics/AnalyticsPage';
import FlashcardPage from './flashcards/FlashcardPage';
import HomePage from './pages/HomePage';
import Planner from './planner/Planner';
import QuizPage from './quiz/QuizPage';
import './App.css';

const NAV_ITEMS = [
  { to: '/', label: 'Home', icon: '🏠', end: true },
  { to: '/quiz', label: 'Quiz', icon: '📝' },
  { to: '/flashcards', label: 'Flashcards', icon: '🃏' },
  { to: '/analytics', label: 'Analytics', icon: '📊' },
  { to: '/planner', label: 'Study Planner', icon: '📅' },
];

function App() {
  return (
    <div className="app">
      <nav className="sidebar">
        <div className="sidebar__brand">
          <span className="sidebar__logo">🎓</span>
          <div>
            <strong>Exam Prep AI</strong>
            <small>10 Core Subjects</small>
          </div>
        </div>
        <ul className="sidebar__nav">
          {NAV_ITEMS.map(({ to, label, icon, end }) => (
            <li key={to}>
              <NavLink
                to={to}
                end={end}
                className={({ isActive }) => (isActive ? 'active' : '')}
              >
                <span className="sidebar__nav-icon">{icon}</span>
                {label}
              </NavLink>
            </li>
          ))}
        </ul>
        <div className="sidebar__subjects">
          <p className="sidebar__subjects-label">Subjects</p>
          <div className="sidebar__tags">
            {['OOPS', 'DAA', 'Python', 'DBMS', 'DSA', 'ML', 'Aptitude', 'Comm', 'AI', 'Cyber'].map(
              (tag) => (
                <span key={tag} className="sidebar__tag">
                  {tag}
                </span>
              )
            )}
          </div>
        </div>
      </nav>
      <main className="main">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/quiz" element={<QuizPage />} />
          <Route path="/flashcards" element={<FlashcardPage />} />
          <Route path="/analytics" element={<AnalyticsPage />} />
          <Route path="/planner" element={<Planner />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
