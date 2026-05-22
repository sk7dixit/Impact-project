import { Link } from "react-router-dom";

import { motion } from "framer-motion";

import {
  Brain,
  Upload,
  BookOpen,
  Trophy,
  Sparkles,
  ArrowRight,
  MessageSquare,
  BarChart3
} from "lucide-react";

function Home() {

  const features = [
    {
      icon: <Brain size={32} />,
      title: "AI Study Assistant",
      desc: "Ask doubts, summaries, definitions, explanations and get instant AI help."
    },

    {
      icon: <Upload size={32} />,
      title: "Upload Notes",
      desc: "Upload PDFs, notes and assignments for AI-powered analysis."
    },

    {
      icon: <Trophy size={32} />,
      title: "Mock Tests",
      desc: "Practice AI-generated quizzes and improve exam preparation."
    },

    {
      icon: <BarChart3 size={32} />,
      title: "Track Progress",
      desc: "Monitor learning analytics and subject-wise improvement."
    }
  ];

  return (

    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-950 to-slate-950 overflow-hidden">

      {/* HERO SECTION */}
      <div className="relative px-6 lg:px-20 pt-10 pb-24">

        {/* NAVBAR */}
        <div className="flex items-center justify-between mb-20">

          <motion.div
            initial={{
              opacity: 0,
              x: -20
            }}
            animate={{
              opacity: 1,
              x: 0
            }}
            className="flex items-center gap-3"
          >

            <div className="bg-gradient-to-r from-blue-500 to-purple-500 p-3 rounded-2xl shadow-xl">

              <Brain
                size={30}
                className="text-white"
              />

            </div>

            <h1 className="text-2xl font-bold text-white">
              AI Exam Assistant
            </h1>

          </motion.div>

          <div className="hidden md:flex items-center gap-8 text-gray-300">

            <a href="#features" className="hover:text-white transition">
              Features
            </a>

            <a href="#about" className="hover:text-white transition">
              About
            </a>

            <Link
              to="/dashboard"
              className="bg-gradient-to-r from-blue-500 to-purple-500 text-white px-6 py-3 rounded-2xl shadow-xl hover:scale-105 transition-all duration-300"
            >
              Get Started
            </Link>

          </div>

        </div>

        {/* HERO CONTENT */}
        <div className="grid lg:grid-cols-2 gap-16 items-center">

          {/* LEFT */}
          <motion.div
            initial={{
              opacity: 0,
              y: 30
            }}
            animate={{
              opacity: 1,
              y: 0
            }}
            transition={{
              duration: 0.8
            }}
          >

            <div className="inline-flex items-center gap-3 bg-white/10 border border-white/20 backdrop-blur-xl rounded-full px-5 py-3 mb-8">

              <Sparkles
                size={18}
                className="text-yellow-400"
              />

              <span className="text-gray-200">
                AI Powered Smart Learning Platform
              </span>

            </div>

            <h1 className="text-6xl lg:text-7xl font-bold text-white leading-tight">

              Study Smarter with{" "}

              <span className="bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                AI
              </span>

            </h1>

            <p className="text-gray-300 text-xl mt-8 leading-relaxed">

              Your intelligent exam preparation assistant for notes,
              quizzes, summaries, AI chat, mock tests, and progress tracking.

            </p>

            {/* BUTTONS */}
            <div className="flex flex-wrap gap-5 mt-10">

              <Link
                to="/dashboard"
                className="bg-gradient-to-r from-blue-500 to-purple-500 text-white px-8 py-4 rounded-2xl shadow-2xl hover:scale-105 transition-all duration-300 flex items-center gap-3"
              >

                Get Started

                <ArrowRight size={22} />

              </Link>

              <Link
                to="/chat"
                className="bg-white/10 border border-white/20 backdrop-blur-xl text-white px-8 py-4 rounded-2xl hover:bg-white/20 transition-all duration-300 flex items-center gap-3"
              >

                <MessageSquare size={22} />

                Try AI Chat

              </Link>

            </div>

          </motion.div>

          {/* RIGHT */}
          <motion.div
            initial={{
              opacity: 0,
              scale: 0.9
            }}
            animate={{
              opacity: 1,
              scale: 1
            }}
            transition={{
              duration: 1
            }}
            className="relative"
          >

            {/* MAIN CARD */}
            <div className="bg-white/10 backdrop-blur-xl border border-white/20 rounded-3xl p-8 shadow-2xl">

              {/* TOP */}
              <div className="flex items-center justify-between mb-8">

                <div>

                  <h2 className="text-white text-2xl font-bold">
                    AI Learning Dashboard
                  </h2>

                  <p className="text-gray-300 mt-2">
                    Personalized Study Analytics
                  </p>

                </div>

                <div className="bg-gradient-to-r from-blue-500 to-purple-500 p-4 rounded-2xl">

                  <Brain
                    size={30}
                    className="text-white"
                  />

                </div>

              </div>

              {/* STATS */}
              <div className="grid grid-cols-2 gap-5">

                <div className="bg-white/10 rounded-2xl p-5 border border-white/20">

                  <h3 className="text-gray-300">
                    Subjects
                  </h3>

                  <h1 className="text-4xl font-bold text-white mt-3">
                    12
                  </h1>

                </div>

                <div className="bg-white/10 rounded-2xl p-5 border border-white/20">

                  <h3 className="text-gray-300">
                    AI Queries
                  </h3>

                  <h1 className="text-4xl font-bold text-white mt-3">
                    240+
                  </h1>

                </div>

                <div className="bg-white/10 rounded-2xl p-5 border border-white/20">

                  <h3 className="text-gray-300">
                    Accuracy
                  </h3>

                  <h1 className="text-4xl font-bold text-white mt-3">
                    92%
                  </h1>

                </div>

                <div className="bg-white/10 rounded-2xl p-5 border border-white/20">

                  <h3 className="text-gray-300">
                    Mock Tests
                  </h3>

                  <h1 className="text-4xl font-bold text-white mt-3">
                    35
                  </h1>

                </div>

              </div>

            </div>

          </motion.div>

        </div>

      </div>

      {/* FEATURES */}
      <section
        id="features"
        className="px-6 lg:px-20 pb-24"
      >

        <motion.div
          initial={{
            opacity: 0,
            y: 20
          }}
          whileInView={{
            opacity: 1,
            y: 0
          }}
          viewport={{
            once: true
          }}
          className="text-center mb-16"
        >

          <h2 className="text-5xl font-bold text-white">
            Powerful Features 🚀
          </h2>

          <p className="text-gray-300 mt-5 text-xl">
            Everything you need for smarter exam preparation.
          </p>

        </motion.div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">

          {features.map((feature, index) => (

            <motion.div
              key={index}
              whileHover={{
                scale: 1.05
              }}
              className="bg-white/10 backdrop-blur-xl border border-white/20 rounded-3xl p-8 shadow-2xl"
            >

              <div className="bg-gradient-to-r from-blue-500 to-purple-500 w-fit p-4 rounded-2xl text-white mb-6">

                {feature.icon}

              </div>

              <h3 className="text-2xl font-bold text-white mb-4">

                {feature.title}

              </h3>

              <p className="text-gray-300 leading-relaxed">

                {feature.desc}

              </p>

            </motion.div>
          ))}

        </div>

      </section>

      {/* FOOTER */}
      <footer className="border-t border-white/10 py-10 text-center text-gray-400">

        <p>
          © 2026 AI Exam Preparation Assistant • Built with React + Tailwind CSS
        </p>

      </footer>

    </div>
  );
}

export default Home;