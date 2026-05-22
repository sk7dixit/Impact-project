import { Link } from 'react-router-dom';
import SubjectsGrid from '../components/SubjectsGrid';
import { SUBJECTS } from '../data/subjects';

const QUICK_LINKS = [
  { to: '/quiz', label: 'Start Quiz', icon: '📝', desc: 'Timed MCQs by subject' },
  { to: '/flashcards', label: 'Flashcards', icon: '🃏', desc: 'Flip & revise key concepts' },
  { to: '/analytics', label: 'Analytics', icon: '📊', desc: 'Scores & weak topics' },
  { to: '/planner', label: 'Study Planner', icon: '📅', desc: 'Schedule daily sessions' },
];

export default function HomePage() {
  return (
    <div className="page home-page">
      <header className="hero">
        <div className="hero__badge">Placement & Exam Prep</div>
        <h1 className="hero__title">
          Master your <span className="hero__highlight">core subjects</span>
        </h1>
        <p className="hero__subtitle">
          Practice OOPS, DAA, Python, DBMS, DSA, ML, Aptitude, Communication, AI & Cyber —
          all in one smart study hub.
        </p>
      </header>

      <section className="home-section">
        <h2 className="home-section__title">
          <span>📚</span> Your subjects
        </h2>
        <p className="home-section__desc">{SUBJECTS.length} subjects ready for quiz, flashcards & planning</p>
        <SubjectsGrid showAllOption={false} />
      </section>

      <section className="home-section">
        <h2 className="home-section__title">
          <span>⚡</span> Quick actions
        </h2>
        <div className="quick-links">
          {QUICK_LINKS.map((link) => (
            <Link key={link.to} to={link.to} className="quick-link card">
              <span className="quick-link__icon">{link.icon}</span>
              <div>
                <strong>{link.label}</strong>
                <p>{link.desc}</p>
              </div>
              <span className="quick-link__arrow">→</span>
            </Link>
          ))}
        </div>
      </section>
    </div>
  );
}
