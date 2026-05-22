/** Subject catalog — shared across Quiz, Flashcards, Planner, and Home */
export const SUBJECTS = [
  {
    id: 'OOPS',
    name: 'OOPS',
    fullName: 'Object-Oriented Programming',
    icon: '🧩',
    color: '#8b5cf6',
    gradient: 'linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%)',
  },
  {
    id: 'DAA',
    name: 'DAA',
    fullName: 'Design & Analysis of Algorithms',
    icon: '📐',
    color: '#06b6d4',
    gradient: 'linear-gradient(135deg, #06b6d4 0%, #0891b2 100%)',
  },
  {
    id: 'Python',
    name: 'Python',
    fullName: 'Python Programming',
    icon: '🐍',
    color: '#22c55e',
    gradient: 'linear-gradient(135deg, #22c55e 0%, #16a34a 100%)',
  },
  {
    id: 'DBMS',
    name: 'DBMS',
    fullName: 'Database Management Systems',
    icon: '🗄️',
    color: '#f59e0b',
    gradient: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)',
  },
  {
    id: 'DSA',
    name: 'DSA',
    fullName: 'Data Structures & Algorithms',
    icon: '🔗',
    color: '#3b82f6',
    gradient: 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)',
  },
  {
    id: 'ML',
    name: 'ML',
    fullName: 'Machine Learning',
    icon: '🤖',
    color: '#ec4899',
    gradient: 'linear-gradient(135deg, #ec4899 0%, #db2777 100%)',
  },
  {
    id: 'Aptitude',
    name: 'Aptitude',
    fullName: 'Quantitative & Logical Aptitude',
    icon: '🎯',
    color: '#f97316',
    gradient: 'linear-gradient(135deg, #f97316 0%, #ea580c 100%)',
  },
  {
    id: 'Communication',
    name: 'Communication',
    fullName: 'Soft Skills & Communication',
    icon: '💬',
    color: '#14b8a6',
    gradient: 'linear-gradient(135deg, #14b8a6 0%, #0d9488 100%)',
  },
  {
    id: 'AI',
    name: 'AI',
    fullName: 'Artificial Intelligence',
    icon: '🧠',
    color: '#a855f7',
    gradient: 'linear-gradient(135deg, #a855f7 0%, #9333ea 100%)',
  },
  {
    id: 'Cyber',
    name: 'Cyber',
    fullName: 'Cybersecurity',
    icon: '🛡️',
    color: '#ef4444',
    gradient: 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)',
  },
];

export const SUBJECT_MAP = Object.fromEntries(SUBJECTS.map((s) => [s.id, s]));

export function getSubjectStyle(topic) {
  const s = SUBJECT_MAP[topic];
  return s ? { '--subject-color': s.color, '--subject-gradient': s.gradient } : {};
}
