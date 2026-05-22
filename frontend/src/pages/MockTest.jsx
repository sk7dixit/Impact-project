import MainLayout from "../layouts/MainLayout";

import { useState } from "react";

import { motion } from "framer-motion";

import {
  Brain,
  Clock3,
  Trophy,
  CheckCircle2,
  XCircle,
  PlayCircle,
  RotateCcw
} from "lucide-react";

function MockTest() {

  const questions = [
    {
      question:
        "Which data structure uses FIFO principle?",
      options: [
        "Stack",
        "Queue",
        "Tree",
        "Graph"
      ],
      answer: "Queue"
    },

    {
      question:
        "Which language is mainly used for AI and ML?",
      options: [
        "Python",
        "HTML",
        "CSS",
        "PHP"
      ],
      answer: "Python"
    },

    {
      question:
        "What does DBMS stand for?",
      options: [
        "Database Management System",
        "Digital Base Management System",
        "Data Backup Management Service",
        "None"
      ],
      answer:
        "Database Management System"
    },

    {
      question:
        "Which traversal uses Queue?",
      options: [
        "DFS",
        "BFS",
        "Binary Search",
        "Recursion"
      ],
      answer: "BFS"
    }
  ];

  const [started, setStarted] =
    useState(false);

  const [currentQuestion, setCurrentQuestion] =
    useState(0);

  const [selected, setSelected] =
    useState("");

  const [score, setScore] =
    useState(0);

  const [showResult, setShowResult] =
    useState(false);

  const [feedback, setFeedback] =
    useState("");

  // START TEST
  const startTest = () => {

    setStarted(true);
  };

  // NEXT QUESTION
  const handleNext = () => {

    if (!selected) return;

    const correctAnswer =
      questions[currentQuestion].answer;

    if (selected === correctAnswer) {

      setScore(score + 1);

      setFeedback(
        "✅ Correct! Great job 🚀"
      );

    } else {

      setFeedback(
        `❌ Incorrect.\nCorrect Answer: ${correctAnswer}`
      );
    }

    setTimeout(() => {

      setFeedback("");

      if (
        currentQuestion + 1 <
        questions.length
      ) {

        setCurrentQuestion(
          currentQuestion + 1
        );

        setSelected("");

      } else {

        setShowResult(true);
      }

    }, 1500);
  };

  // RESTART
  const restartTest = () => {

    setStarted(false);

    setCurrentQuestion(0);

    setSelected("");

    setScore(0);

    setShowResult(false);
  };

  return (

    <MainLayout>

      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-950 to-slate-950 p-6">

        {/* HEADER */}
        <motion.div
          initial={{
            opacity: 0,
            y: -20
          }}
          animate={{
            opacity: 1,
            y: 0
          }}
          className="mb-10"
        >

          <h1 className="text-5xl font-bold text-white">
            AI Mock Test 🧠
          </h1>

          <p className="text-gray-300 mt-3 text-lg">
            Practice AI-generated quizzes and improve your exam preparation.
          </p>

        </motion.div>

        {/* START SCREEN */}
        {!started && !showResult && (

          <motion.div
            initial={{
              opacity: 0,
              scale: 0.95
            }}
            animate={{
              opacity: 1,
              scale: 1
            }}
            className="bg-white/10 backdrop-blur-xl border border-white/20 rounded-3xl p-10 shadow-2xl text-center"
          >

            <div className="flex justify-center mb-6">

              <div className="bg-gradient-to-r from-blue-500 to-purple-500 p-5 rounded-full shadow-xl">

                <Brain
                  size={60}
                  className="text-white"
                />

              </div>

            </div>

            <h2 className="text-4xl font-bold text-white mb-4">
              Ready for Your Mock Test?
            </h2>

            <p className="text-gray-300 mb-8 text-lg">
              Test your knowledge in Java, Python, DBMS, DSA, AI and more.
            </p>

            <button
              onClick={startTest}
              className="bg-gradient-to-r from-blue-500 to-purple-500 text-white px-10 py-4 rounded-2xl shadow-xl hover:scale-105 transition-all duration-300 flex items-center gap-3 mx-auto"
            >

              <PlayCircle size={24} />

              Start Test

            </button>

          </motion.div>
        )}

        {/* QUIZ SECTION */}
        {started && !showResult && (

          <motion.div
            initial={{
              opacity: 0
            }}
            animate={{
              opacity: 1
            }}
            className="bg-white/10 backdrop-blur-xl border border-white/20 rounded-3xl p-10 shadow-2xl"
          >

            {/* TOP BAR */}
            <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-5 mb-10">

              <div className="flex items-center gap-3">

                <div className="bg-blue-500 p-3 rounded-2xl">

                  <Clock3
                    size={24}
                    className="text-white"
                  />

                </div>

                <div>

                  <h3 className="text-white font-bold">
                    Question {currentQuestion + 1}
                  </h3>

                  <p className="text-gray-300">
                    Total Questions: {questions.length}
                  </p>

                </div>

              </div>

              <div className="bg-white/10 border border-white/20 px-5 py-3 rounded-2xl">

                <span className="text-white font-semibold">
                  Score: {score}
                </span>

              </div>

            </div>

            {/* QUESTION */}
            <h2 className="text-3xl font-bold text-white mb-8 leading-relaxed">

              {
                questions[currentQuestion]
                  .question
              }

            </h2>

            {/* OPTIONS */}
            <div className="space-y-5">

              {
                questions[
                  currentQuestion
                ].options.map(
                  (option, index) => (

                    <motion.div
                      whileHover={{
                        scale: 1.02
                      }}
                      key={index}
                      onClick={() =>
                        setSelected(option)
                      }
                      className={`p-5 rounded-2xl border cursor-pointer transition-all duration-300 ${
                        selected === option
                          ? "bg-blue-500 border-blue-400 text-white"
                          : "bg-white/10 border-white/20 text-gray-200 hover:bg-white/20"
                      }`}
                    >

                      {option}

                    </motion.div>
                  )
                )
              }

            </div>

            {/* FEEDBACK */}
            {feedback && (

              <motion.div
                initial={{
                  opacity: 0
                }}
                animate={{
                  opacity: 1
                }}
                className="mt-8 bg-white/10 border border-white/20 rounded-2xl p-5 text-white whitespace-pre-line"
              >

                {feedback}

              </motion.div>
            )}

            {/* NEXT BUTTON */}
            <div className="mt-10">

              <button
                onClick={handleNext}
                className="bg-gradient-to-r from-blue-500 to-purple-500 text-white px-8 py-4 rounded-2xl shadow-xl hover:scale-105 transition-all duration-300"
              >

                Next Question

              </button>

            </div>

          </motion.div>
        )}

        {/* RESULT SCREEN */}
        {showResult && (

          <motion.div
            initial={{
              opacity: 0,
              scale: 0.9
            }}
            animate={{
              opacity: 1,
              scale: 1
            }}
            className="bg-white/10 backdrop-blur-xl border border-white/20 rounded-3xl p-10 shadow-2xl text-center"
          >

            <div className="flex justify-center mb-6">

              <div className="bg-gradient-to-r from-green-500 to-emerald-500 p-5 rounded-full shadow-xl">

                <Trophy
                  size={60}
                  className="text-white"
                />

              </div>

            </div>

            <h1 className="text-5xl font-bold text-white mb-5">
              Test Completed 🎉
            </h1>

            <p className="text-gray-300 text-xl mb-8">

              You scored{" "}

              <span className="text-white font-bold">
                {score}
              </span>

              {" "}out of{" "}

              <span className="text-white font-bold">
                {questions.length}
              </span>

            </p>

            {/* RESULT STATUS */}
            <div className="mb-8">

              {score >= 3 ? (

                <div className="flex items-center justify-center gap-3 text-green-400 text-2xl font-bold">

                  <CheckCircle2 size={30} />

                  Excellent Performance 🚀

                </div>

              ) : (

                <div className="flex items-center justify-center gap-3 text-red-400 text-2xl font-bold">

                  <XCircle size={30} />

                  Keep Practicing 💪

                </div>
              )}

            </div>

            {/* RESTART BUTTON */}
            <button
              onClick={restartTest}
              className="bg-gradient-to-r from-blue-500 to-purple-500 text-white px-10 py-4 rounded-2xl shadow-xl hover:scale-105 transition-all duration-300 flex items-center gap-3 mx-auto"
            >

              <RotateCcw size={22} />

              Restart Test

            </button>

          </motion.div>
        )}

      </div>

    </MainLayout>
  );
}

export default MockTest;