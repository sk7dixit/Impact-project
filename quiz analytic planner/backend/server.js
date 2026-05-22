const express = require('express');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());

// --- Core placement / exam subjects ---
const topics = [
  'OOPS',
  'DAA',
  'Python',
  'DBMS',
  'DSA',
  'ML',
  'Aptitude',
  'Communication',
  'AI',
  'Cyber',
];

const sampleQuestions = [
  {
    id: 1,
    topic: 'OOPS',
    question: 'Which OOP principle hides internal details and exposes only necessary parts?',
    options: ['Inheritance', 'Encapsulation', 'Polymorphism', 'Abstraction'],
    correctIndex: 1,
  },
  {
    id: 2,
    topic: 'OOPS',
    question: 'In Java, which keyword is used to inherit a class?',
    options: ['implements', 'extends', 'inherits', 'super'],
    correctIndex: 1,
  },
  {
    id: 3,
    topic: 'DAA',
    question: 'What is the time complexity of binary search on a sorted array?',
    options: ['O(n)', 'O(log n)', 'O(n log n)', 'O(1)'],
    correctIndex: 1,
  },
  {
    id: 4,
    topic: 'DAA',
    question: 'Which algorithm design paradigm breaks a problem into overlapping subproblems?',
    options: ['Greedy', 'Divide and Conquer', 'Dynamic Programming', 'Backtracking'],
    correctIndex: 2,
  },
  {
    id: 5,
    topic: 'Python',
    question: 'Which data type in Python is immutable?',
    options: ['List', 'Dictionary', 'Set', 'Tuple'],
    correctIndex: 3,
  },
  {
    id: 6,
    topic: 'Python',
    question: 'What does len([1, 2, 3]) return?',
    options: ['2', '3', '4', 'Error'],
    correctIndex: 1,
  },
  {
    id: 7,
    topic: 'DBMS',
    question: 'Which normal form removes partial dependency?',
    options: ['1NF', '2NF', '3NF', 'BCNF'],
    correctIndex: 1,
  },
  {
    id: 8,
    topic: 'DBMS',
    question: 'SQL command to remove all rows but keep table structure?',
    options: ['DROP', 'DELETE', 'TRUNCATE', 'REMOVE'],
    correctIndex: 2,
  },
  {
    id: 9,
    topic: 'DSA',
    question: 'Which data structure uses FIFO order?',
    options: ['Stack', 'Queue', 'Tree', 'Graph'],
    correctIndex: 1,
  },
  {
    id: 10,
    topic: 'DSA',
    question: 'Worst-case time complexity of inserting into a balanced BST?',
    options: ['O(1)', 'O(log n)', 'O(n)', 'O(n²)'],
    correctIndex: 1,
  },
  {
    id: 11,
    topic: 'ML',
    question: 'Which metric is best for imbalanced classification?',
    options: ['Accuracy', 'F1-score', 'MSE', 'R²'],
    correctIndex: 1,
  },
  {
    id: 12,
    topic: 'ML',
    question: 'Overfitting means the model…',
    options: ['Underfits training data', 'Memorizes noise in training data', 'Has high bias', 'Uses too few features'],
    correctIndex: 1,
  },
  {
    id: 13,
    topic: 'Aptitude',
    question: 'If 20% of a number is 50, what is the number?',
    options: ['200', '250', '300', '400'],
    correctIndex: 1,
  },
  {
    id: 14,
    topic: 'Aptitude',
    question: 'Complete the series: 2, 6, 12, 20, ?',
    options: ['28', '30', '32', '36'],
    correctIndex: 1,
  },
  {
    id: 15,
    topic: 'Communication',
    question: 'In a professional email, the subject line should be…',
    options: ['Blank', 'Clear and specific', 'All caps only', 'Optional'],
    correctIndex: 1,
  },
  {
    id: 16,
    topic: 'Communication',
    question: 'Active listening primarily involves…',
    options: ['Interrupting often', 'Paraphrasing and feedback', 'Avoiding eye contact', 'Speaking more than listening'],
    correctIndex: 1,
  },
  {
    id: 17,
    topic: 'AI',
    question: 'A perceptron is a type of…',
    options: ['Search tree', 'Neural network unit', 'Database index', 'Sorting algorithm'],
    correctIndex: 1,
  },
  {
    id: 18,
    topic: 'AI',
    question: 'Which search algorithm uses a heuristic function?',
    options: ['BFS', 'DFS', 'A*', 'Dijkstra only'],
    correctIndex: 2,
  },
  {
    id: 19,
    topic: 'Cyber',
    question: 'Phishing attacks typically aim to…',
    options: ['Encrypt disks', 'Steal credentials via deception', 'Speed up networks', 'Patch vulnerabilities'],
    correctIndex: 1,
  },
  {
    id: 20,
    topic: 'Cyber',
    question: 'HTTPS primarily provides…',
    options: ['Anonymity only', 'Encryption and integrity', 'Faster DNS', 'MAC filtering'],
    correctIndex: 1,
  },
];

const sampleFlashcards = [
  { id: 1, topic: 'OOPS', front: 'Four pillars of OOP', back: 'Encapsulation, Abstraction, Inheritance, Polymorphism' },
  { id: 2, topic: 'OOPS', front: 'Constructor', back: 'Special method invoked when an object is created' },
  { id: 3, topic: 'DAA', front: 'Master Theorem', back: 'Solves recurrence T(n)=aT(n/b)+f(n) for divide-and-conquer' },
  { id: 4, topic: 'DAA', front: 'Big-O', back: 'Upper bound on growth rate of an algorithm' },
  { id: 5, topic: 'Python', front: 'List comprehension', back: '[expr for item in iterable if condition]' },
  { id: 6, topic: 'Python', front: 'GIL', back: 'Global Interpreter Lock — one thread executes Python bytecode at a time' },
  { id: 7, topic: 'DBMS', front: 'ACID', back: 'Atomicity, Consistency, Isolation, Durability' },
  { id: 8, topic: 'DBMS', front: 'Primary Key', back: 'Uniquely identifies each row in a table' },
  { id: 9, topic: 'DSA', front: 'Stack operations', back: 'push, pop, peek — LIFO structure' },
  { id: 10, topic: 'DSA', front: 'Hash collision', back: 'Two keys map to same index; resolved by chaining or open addressing' },
  { id: 11, topic: 'ML', front: 'Train/Test split', back: 'Hold out data to evaluate generalization' },
  { id: 12, topic: 'ML', front: 'Gradient Descent', back: 'Iteratively minimizes loss by moving opposite to gradient' },
  { id: 13, topic: 'Aptitude', front: 'Profit %', back: 'Profit% = (SP − CP) / CP × 100' },
  { id: 14, topic: 'Aptitude', front: 'Time-Speed-Distance', back: 'Distance = Speed × Time' },
  { id: 15, topic: 'Communication', front: 'STAR method', back: 'Situation, Task, Action, Result — for interviews' },
  { id: 16, topic: 'Communication', front: 'Barriers', back: 'Noise, language, cultural differences, poor feedback' },
  { id: 17, topic: 'AI', front: 'Turing Test', back: 'Machine indistinguishable from human in conversation' },
  { id: 18, topic: 'AI', front: 'Expert System', back: 'Rule-based AI using knowledge base and inference engine' },
  { id: 19, topic: 'Cyber', front: 'CIA Triad', back: 'Confidentiality, Integrity, Availability' },
  { id: 20, topic: 'Cyber', front: 'Firewall', back: 'Monitors and filters network traffic by security rules' },
];

let quizAttempts = [
  { date: '2026-05-10', score: 80, total: 5, topic: 'OOPS', correct: 4 },
  { date: '2026-05-11', score: 65, total: 5, topic: 'DAA', correct: 3 },
  { date: '2026-05-12', score: 90, total: 5, topic: 'Python', correct: 5 },
  { date: '2026-05-13', score: 70, total: 5, topic: 'DBMS', correct: 4 },
  { date: '2026-05-14', score: 55, total: 5, topic: 'DSA', correct: 3 },
  { date: '2026-05-15', score: 75, total: 5, topic: 'ML', correct: 4 },
  { date: '2026-05-16', score: 85, total: 5, topic: 'Aptitude', correct: 4 },
  { date: '2026-05-17', score: 88, total: 5, topic: 'Communication', correct: 4 },
  { date: '2026-05-18', score: 60, total: 5, topic: 'AI', correct: 3 },
  { date: '2026-05-19', score: 72, total: 5, topic: 'Cyber', correct: 4 },
];

let studySchedule = [
  { id: 1, date: '2026-05-20', time: '09:00', subject: 'OOPS', duration: 45, completed: false },
  { id: 2, date: '2026-05-20', time: '11:00', subject: 'DSA', duration: 60, completed: true },
  { id: 3, date: '2026-05-20', time: '14:00', subject: 'Python', duration: 50, completed: false },
  { id: 4, date: '2026-05-21', time: '10:00', subject: 'DBMS', duration: 45, completed: false },
  { id: 5, date: '2026-05-21', time: '15:00', subject: 'Aptitude', duration: 40, completed: false },
  { id: 6, date: '2026-05-21', time: '17:00', subject: 'Cyber', duration: 55, completed: false },
];

// --- Quiz APIs ---
app.get('/api/quiz/questions', (req, res) => {
  const { topic, count = 5 } = req.query;
  let pool = [...sampleQuestions];
  if (topic) pool = pool.filter((q) => q.topic === topic);
  const shuffled = pool.sort(() => Math.random() - 0.5).slice(0, Number(count));
  const safe = shuffled.map(({ correctIndex, ...q }) => q);
  res.json(safe);
});

app.post('/api/quiz/generate', (req, res) => {
  const { topic, count = 5, difficulty = 'medium' } = req.body;
  let pool = [...sampleQuestions];
  if (topic) pool = pool.filter((q) => q.topic === topic);
  const selected = pool.sort(() => Math.random() - 0.5).slice(0, Math.min(count, pool.length));
  res.json({
    quizId: Date.now(),
    topic: topic || 'Mixed',
    difficulty,
    timeLimit: difficulty === 'hard' ? 300 : difficulty === 'easy' ? 600 : 450,
    questions: selected.map(({ correctIndex, ...q }) => q),
    answerKey: selected.map((q) => ({ id: q.id, correctIndex: q.correctIndex })),
  });
});

app.post('/api/quiz/submit', (req, res) => {
  const { answers, answerKey, topic = 'Mixed', timeTaken } = req.body;
  let correct = 0;
  const breakdown = (answerKey || []).map((key) => {
    const userAnswer = answers?.[key.id];
    const isCorrect = userAnswer === key.correctIndex;
    if (isCorrect) correct += 1;
    return { questionId: key.id, correct: isCorrect, userAnswer, correctAnswer: key.correctIndex };
  });
  const total = answerKey?.length || 0;
  const score = total ? Math.round((correct / total) * 100) : 0;
  const attempt = {
    date: new Date().toISOString().split('T')[0],
    score,
    total,
    topic,
    timeTaken,
    correct,
  };
  quizAttempts.push(attempt);
  res.json({ score, correct, total, breakdown, attempt });
});

// --- Flashcard APIs ---
app.get('/api/flashcards', (req, res) => {
  const { topic } = req.query;
  let cards = [...sampleFlashcards];
  if (topic) cards = cards.filter((c) => c.topic === topic);
  res.json(cards);
});

app.get('/api/flashcards/topics', (_req, res) => {
  res.json([...new Set(sampleFlashcards.map((c) => c.topic))]);
});

// --- Analytics APIs ---
app.get('/api/analytics/progress', (_req, res) => {
  const progress = quizAttempts.map((a) => ({
    date: a.date,
    score: a.score,
    topic: a.topic,
  }));
  res.json(progress);
});

app.get('/api/analytics/weak-topics', (_req, res) => {
  const byTopic = {};
  quizAttempts.forEach((a) => {
    if (!byTopic[a.topic]) byTopic[a.topic] = { total: 0, sum: 0 };
    byTopic[a.topic].total += 1;
    byTopic[a.topic].sum += a.score;
  });
  const weak = Object.entries(byTopic)
    .map(([topic, { total, sum }]) => ({
      topic,
      avgScore: Math.round(sum / total),
      attempts: total,
    }))
    .sort((a, b) => a.avgScore - b.avgScore);
  res.json(weak);
});

app.get('/api/analytics/statistics', (_req, res) => {
  const scores = quizAttempts.map((a) => a.score);
  const avg = scores.length ? Math.round(scores.reduce((s, v) => s + v, 0) / scores.length) : 0;
  const best = scores.length ? Math.max(...scores) : 0;
  const totalQuizzes = quizAttempts.length;
  const totalCorrect = quizAttempts.reduce((s, a) => s + (a.correct || 0), 0);
  const totalQuestions = quizAttempts.reduce((s, a) => s + (a.total || 0), 0);
  res.json({
    totalQuizzes,
    averageScore: avg,
    bestScore: best,
    accuracy: totalQuestions ? Math.round((totalCorrect / totalQuestions) * 100) : 0,
    recentAttempts: quizAttempts.slice(-5).reverse(),
  });
});

// --- Planner APIs ---
app.get('/api/planner/schedule', (req, res) => {
  const { date } = req.query;
  let items = [...studySchedule];
  if (date) items = items.filter((s) => s.date === date);
  res.json(items);
});

app.post('/api/planner/schedule', (req, res) => {
  const { date, time, subject, duration } = req.body;
  const item = {
    id: Date.now(),
    date,
    time,
    subject,
    duration: duration || 30,
    completed: false,
  };
  studySchedule.push(item);
  res.status(201).json(item);
});

app.patch('/api/planner/schedule/:id', (req, res) => {
  const id = Number(req.params.id);
  const idx = studySchedule.findIndex((s) => s.id === id);
  if (idx === -1) return res.status(404).json({ error: 'Not found' });
  studySchedule[idx] = { ...studySchedule[idx], ...req.body };
  res.json(studySchedule[idx]);
});

app.delete('/api/planner/schedule/:id', (req, res) => {
  const id = Number(req.params.id);
  studySchedule = studySchedule.filter((s) => s.id !== id);
  res.json({ success: true });
});

app.get('/api/planner/progress', (_req, res) => {
  const total = studySchedule.length;
  const completed = studySchedule.filter((s) => s.completed).length;
  const today = new Date().toISOString().split('T')[0];
  const todayItems = studySchedule.filter((s) => s.date === today);
  res.json({
    totalSessions: total,
    completedSessions: completed,
    completionRate: total ? Math.round((completed / total) * 100) : 0,
    todayTotal: todayItems.length,
    todayCompleted: todayItems.filter((s) => s.completed).length,
  });
});

app.get('/api/topics', (_req, res) => res.json(topics));

const server = app.listen(PORT);

server.on('listening', () => {
  console.log(`\nAPI server running on http://localhost:${PORT}`);
  console.log('Keep this terminal open. Start frontend in another terminal.\n');
});

server.on('error', (err) => {
  if (err.code === 'EADDRINUSE') {
    console.error(`\nPort ${PORT} is already in use — backend may ALREADY be running.`);
    console.error('Option 1: Skip backend. In a new terminal run frontend only:');
    console.error('  cd frontend');
    console.error('  npm run dev');
    console.error('Option 2: Stop old server, then run npm start again:');
    console.error('  .\\STOP_SERVERS.bat\n');
  } else {
    console.error('Server error:', err.message);
  }
  process.exit(1);
});
