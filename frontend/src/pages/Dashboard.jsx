import MainLayout from "../layouts/MainLayout";

import { motion } from "framer-motion";

import {
  BookOpen,
  Brain,
  FileText,
  Trophy,
  Clock3,
  BarChart3,
  Sparkles,
  Target,
  Flame,
  TrendingUp
} from "lucide-react";

function Dashboard() {

  const subjects = [
    "Java",
    "Python",
    "DBMS",
    "DSA",
    "AI",
    "ML",
    "Cyber Security",
    "Operating System"
  ];

  const recentActivities = [
    "Completed Java Quiz",
    "Uploaded DBMS Notes",
    "Generated AI Summary",
    "Practiced DSA Questions"
  ];

  return (

    <MainLayout>

      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-950 to-slate-950 p-6">

        {/* TOP HEADER */}
        <motion.div
          initial={{
            opacity: 0,
            y: -20
          }}
          animate={{
            opacity: 1,
            y: 0
          }}
          className="flex flex-col md:flex-row md:items-center md:justify-between gap-6 mb-10"
        >

          <div>

            <h1 className="text-5xl font-bold text-white">
              Dashboard 🚀
            </h1>

            <p className="text-gray-300 mt-3 text-lg">
              Welcome back! Continue your AI-powered learning journey.
            </p>

          </div>

          {/* AI Badge */}
          <div className="bg-white/10 backdrop-blur-xl border border-white/20 rounded-3xl px-6 py-4 shadow-xl flex items-center gap-4">

            <div className="bg-gradient-to-r from-blue-500 to-purple-500 p-3 rounded-2xl">

              <Sparkles
                size={28}
                className="text-white"
              />

            </div>

            <div>

              <h3 className="text-white font-bold">
                AI Learning Mode
              </h3>

              <p className="text-gray-300 text-sm">
                Smart recommendations enabled
              </p>

            </div>

          </div>

        </motion.div>

        {/* STATS */}
        <div className="grid md:grid-cols-4 gap-6 mb-10">

          {/* Card */}
          <motion.div
            whileHover={{
              scale: 1.03
            }}
            className="bg-white/10 backdrop-blur-xl border border-white/20 rounded-3xl p-6 shadow-2xl"
          >

            <div className="bg-blue-500 w-fit p-4 rounded-2xl mb-4">

              <BookOpen
                size={28}
                className="text-white"
              />

            </div>

            <h2 className="text-gray-300">
              Subjects
            </h2>

            <h1 className="text-4xl font-bold text-white mt-2">
              8
            </h1>

          </motion.div>

          {/* Card */}
          <motion.div
            whileHover={{
              scale: 1.03
            }}
            className="bg-white/10 backdrop-blur-xl border border-white/20 rounded-3xl p-6 shadow-2xl"
          >

            <div className="bg-purple-500 w-fit p-4 rounded-2xl mb-4">

              <Brain
                size={28}
                className="text-white"
              />

            </div>

            <h2 className="text-gray-300">
              AI Queries
            </h2>

            <h1 className="text-4xl font-bold text-white mt-2">
              124
            </h1>

          </motion.div>

          {/* Card */}
          <motion.div
            whileHover={{
              scale: 1.03
            }}
            className="bg-white/10 backdrop-blur-xl border border-white/20 rounded-3xl p-6 shadow-2xl"
          >

            <div className="bg-green-500 w-fit p-4 rounded-2xl mb-4">

              <Trophy
                size={28}
                className="text-white"
              />

            </div>

            <h2 className="text-gray-300">
              Quiz Score
            </h2>

            <h1 className="text-4xl font-bold text-white mt-2">
              92%
            </h1>

          </motion.div>

          {/* Card */}
          <motion.div
            whileHover={{
              scale: 1.03
            }}
            className="bg-white/10 backdrop-blur-xl border border-white/20 rounded-3xl p-6 shadow-2xl"
          >

            <div className="bg-orange-500 w-fit p-4 rounded-2xl mb-4">

              <Clock3
                size={28}
                className="text-white"
              />

            </div>

            <h2 className="text-gray-300">
              Study Hours
            </h2>

            <h1 className="text-4xl font-bold text-white mt-2">
              48h
            </h1>

          </motion.div>

        </div>

        {/* MAIN GRID */}
        <div className="grid lg:grid-cols-3 gap-8">

          {/* SUBJECTS */}
          <div className="lg:col-span-2 bg-white/10 backdrop-blur-xl border border-white/20 rounded-3xl p-8 shadow-2xl">

            <div className="flex items-center justify-between mb-8">

              <h2 className="text-3xl font-bold text-white">
                Subjects
              </h2>

              <div className="bg-blue-500/20 border border-blue-400 text-blue-200 px-4 py-2 rounded-full text-sm">
                Active Learning
              </div>

            </div>

            <div className="grid md:grid-cols-2 gap-5">

              {subjects.map((subject, index) => (

                <motion.div
                  key={index}
                  whileHover={{
                    scale: 1.03
                  }}
                  className="bg-white/10 border border-white/20 rounded-2xl p-5 shadow-lg cursor-pointer hover:bg-white/20 transition-all"
                >

                  <div className="flex items-center justify-between">

                    <div>

                      <h3 className="text-white text-xl font-bold">
                        {subject}
                      </h3>

                      <p className="text-gray-300 mt-2">
                        Smart AI assistance available
                      </p>

                    </div>

                    <div className="bg-gradient-to-r from-blue-500 to-purple-500 p-3 rounded-xl">

                      <Brain
                        size={22}
                        className="text-white"
                      />

                    </div>

                  </div>

                </motion.div>
              ))}

            </div>

          </div>

          {/* RIGHT PANEL */}
          <div className="space-y-8">

            {/* PROGRESS */}
            <motion.div
              whileHover={{
                scale: 1.02
              }}
              className="bg-white/10 backdrop-blur-xl border border-white/20 rounded-3xl p-6 shadow-2xl"
            >

              <div className="flex items-center gap-3 mb-6">

                <div className="bg-green-500 p-3 rounded-2xl">

                  <TrendingUp
                    size={24}
                    className="text-white"
                  />

                </div>

                <h2 className="text-2xl font-bold text-white">
                  Progress
                </h2>

              </div>

              <div className="space-y-5">

                <div>

                  <div className="flex justify-between mb-2">

                    <span className="text-gray-300">
                      Java
                    </span>

                    <span className="text-white">
                      85%
                    </span>

                  </div>

                  <div className="w-full bg-white/10 rounded-full h-3">

                    <div className="bg-blue-500 h-3 rounded-full w-[85%]"></div>

                  </div>

                </div>

                <div>

                  <div className="flex justify-between mb-2">

                    <span className="text-gray-300">
                      DSA
                    </span>

                    <span className="text-white">
                      72%
                    </span>

                  </div>

                  <div className="w-full bg-white/10 rounded-full h-3">

                    <div className="bg-purple-500 h-3 rounded-full w-[72%]"></div>

                  </div>

                </div>

                <div>

                  <div className="flex justify-between mb-2">

                    <span className="text-gray-300">
                      DBMS
                    </span>

                    <span className="text-white">
                      91%
                    </span>

                  </div>

                  <div className="w-full bg-white/10 rounded-full h-3">

                    <div className="bg-green-500 h-3 rounded-full w-[91%]"></div>

                  </div>

                </div>

              </div>

            </motion.div>

            {/* RECENT ACTIVITY */}
            <motion.div
              whileHover={{
                scale: 1.02
              }}
              className="bg-white/10 backdrop-blur-xl border border-white/20 rounded-3xl p-6 shadow-2xl"
            >

              <div className="flex items-center gap-3 mb-6">

                <div className="bg-orange-500 p-3 rounded-2xl">

                  <Flame
                    size={24}
                    className="text-white"
                  />

                </div>

                <h2 className="text-2xl font-bold text-white">
                  Recent Activity
                </h2>

              </div>

              <div className="space-y-4">

                {recentActivities.map(
                  (activity, index) => (

                    <div
                      key={index}
                      className="bg-white/10 border border-white/20 rounded-2xl p-4"
                    >

                      <p className="text-white">
                        {activity}
                      </p>

                    </div>
                  )
                )}

              </div>

            </motion.div>

          </div>

        </div>

        {/* BOTTOM CARDS */}
        <div className="grid md:grid-cols-3 gap-6 mt-10">

          <motion.div
            whileHover={{
              scale: 1.03
            }}
            className="bg-white/10 backdrop-blur-xl border border-white/20 rounded-3xl p-6 shadow-xl"
          >

            <BarChart3
              size={40}
              className="text-blue-400 mb-4"
            />

            <h3 className="text-white text-2xl font-bold mb-3">
              Analytics
            </h3>

            <p className="text-gray-300">
              Track performance and identify weak areas instantly.
            </p>

          </motion.div>

          <motion.div
            whileHover={{
              scale: 1.03
            }}
            className="bg-white/10 backdrop-blur-xl border border-white/20 rounded-3xl p-6 shadow-xl"
          >

            <Target
              size={40}
              className="text-purple-400 mb-4"
            />

            <h3 className="text-white text-2xl font-bold mb-3">
              Smart Goals
            </h3>

            <p className="text-gray-300">
              Set AI-generated targets for daily learning progress.
            </p>

          </motion.div>

          <motion.div
            whileHover={{
              scale: 1.03
            }}
            className="bg-white/10 backdrop-blur-xl border border-white/20 rounded-3xl p-6 shadow-xl"
          >

            <FileText
              size={40}
              className="text-green-400 mb-4"
            />

            <h3 className="text-white text-2xl font-bold mb-3">
              AI Notes
            </h3>

            <p className="text-gray-300">
              Generate summaries, quizzes, and explanations automatically.
            </p>

          </motion.div>

        </div>

      </div>

    </MainLayout>
  );
}

export default Dashboard;