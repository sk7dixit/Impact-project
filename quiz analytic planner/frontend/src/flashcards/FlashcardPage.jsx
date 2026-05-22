import { useEffect, useState } from 'react';
import { api } from '../api/client';
import SubjectsGrid from '../components/SubjectsGrid';
import { SUBJECT_MAP } from '../data/subjects';
import Flashcard from './Flashcard';

export default function FlashcardPage() {
  const [topic, setTopic] = useState('');
  const [cards, setCards] = useState([]);
  const [index, setIndex] = useState(0);
  const [flipped, setFlipped] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    api
      .getFlashcards(topic || undefined)
      .then((data) => {
        setCards(data);
        setIndex(0);
        setFlipped(false);
      })
      .catch(() => setCards([]))
      .finally(() => setLoading(false));
  }, [topic]);

  const card = cards[index];
  const progress = cards.length ? ((index + 1) / cards.length) * 100 : 0;
  const subject = topic ? SUBJECT_MAP[topic] : null;

  const go = (delta) => {
    setFlipped(false);
    setIndex((i) => Math.min(Math.max(i + delta, 0), cards.length - 1));
  };

  const markKnown = () => {
    if (index < cards.length - 1) go(1);
    else setFlipped(false);
  };

  return (
    <div className="page flashcard-page">
      <header className="page-header">
        <h1>Flashcards</h1>
        <p>Revise concepts across all 10 subjects — tap a card to flip.</p>
      </header>

      <section className="card flashcard-controls">
        <h2>Filter by subject</h2>
        <SubjectsGrid selected={topic} onSelect={setTopic} compact />
        <div className="flashcard-progress">
          <div className="flashcard-progress__track">
            <div
              className="flashcard-progress__bar"
              style={{
                width: `${progress}%`,
                background: subject?.gradient || 'var(--accent-gradient)',
              }}
            />
          </div>
          <span>
            {subject && (
              <span className="flashcard-progress__subject" style={{ color: subject.color }}>
                {subject.icon} {subject.name} ·{' '}
              </span>
            )}
            Card {cards.length ? index + 1 : 0} of {cards.length}
          </span>
        </div>
      </section>

      {loading && <p className="loading">Loading flashcards…</p>}
      {!loading && !card && (
        <p className="empty card empty-state">No flashcards for this subject yet. Try another topic.</p>
      )}
      {!loading && card && (
        <>
          <Flashcard card={card} flipped={flipped} onFlip={() => setFlipped((f) => !f)} />
          <nav className="flashcard-nav">
            <button type="button" className="btn btn--ghost" onClick={() => go(-1)} disabled={index === 0}>
              ← Previous
            </button>
            <button type="button" className="btn btn--primary" onClick={markKnown}>
              {index < cards.length - 1 ? 'Next card →' : 'Finish deck'}
            </button>
            <button
              type="button"
              className="btn btn--ghost"
              onClick={() => go(1)}
              disabled={index === cards.length - 1}
            >
              Next →
            </button>
          </nav>
        </>
      )}
    </div>
  );
}
