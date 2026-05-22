function SubjectCard({ subject, tests, progress }) {
  return (
    <div className="bg-white p-6 rounded-2xl shadow">

      <h2 className="text-xl font-semibold mb-3">
        {subject}
      </h2>

      <p className="text-gray-600">
        Tests: {tests}
      </p>

      <p className="text-blue-600 font-medium mt-2">
        Progress: {progress}
      </p>

    </div>
  );
}

export default SubjectCard;