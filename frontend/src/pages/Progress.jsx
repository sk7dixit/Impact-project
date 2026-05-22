import MainLayout from "../layouts/MainLayout";

import { motion } from "framer-motion";

import {
  TrendingUp,
  Trophy,
  Brain,
  Clock3,
  Target,
  Flame,
  CheckCircle2,
  BarChart3,
  Award,
  BookOpen
} from "lucide-react";

function Progress() {

  const subjects = [
    {
      name: "Java",
      progress: 85
    },
    {
      name: "Python",
      progress: 92
    },
    {
      name: "DBMS",
      progress: 78
    },
    {
      name: "DSA",
      progress: 70
    },
    {
      name: "AI",
      progress: 88
    },
    {
      name: "Cyber Security",
      progress: 65
    }
  ];

  const achievements = [
    "Completed 50 AI Queries",
    "Finished Java Quiz",
    "Uploaded 20 Study Materials",
    "7 Day Learning Streak"
  ];

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
          className="flex flex-col md:flex-row md:items-center md:justify-between gap-6 mb-10"
        >

          <div>

            <h1 className="text-5xl font-bold text-white">
              Learning Progress 📈
            </h1>

            <p className="text-gray-300 mt-3 text-lg">
              Track your study performance and AI learning analytics.
            </p>

          </div>

          <div className="bg-white/10 backdrop-blur-xl border border-white/20 rounded-3xl px-6 py-4 shadow-xl flex items-center gap-4">

            <div className="bg-gradient-to-r from-green-500 to-emerald-500 p-3 rounded-2xl">

              <TrendingUp
                size={28}
                className="text-white"
              />

            </div>

            <div>

              <h3 className="text-white font-bold">
                Overall Growth
              </h3>

              <p className="text-green-300 text-sm">
                +18% This Week 🚀
              </p>

            </div>

          </div>

        </motion.div>

        {/* TOP STATS */}
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
              Subjects Completed
            </h2>

            <h1 className="text-4xl font-bold text-white mt-2">
              6
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
              AI Sessions
            </h2>

            <h1 className="text-4xl font-bold text-white mt-2">
              148
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
              Quiz Accuracy
            </h2>

            <h1 className="text-4xl font-bold text-white mt-2">
              91%
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
              72h
            </h1>

          </motion.div>

        </div>

        {/* MAIN GRID */}
        <div className="grid lg:grid-cols-3 gap-8">

          {/* SUBJECT PROGRESS */}
          <div className="lg:col-span-2 bg-white/10 backdrop-blur-xl border border-white/20 rounded-3xl p-8 shadow-2xl">

            <div className="flex items-center justify-between mb-8">

              <h2 className="text-3xl font-bold text-white">
                Subject Progress
              </h2>

              <div className="bg-blue-500/20 border border-blue-400 text-blue-200 px-4 py-2 rounded-full text-sm">
                AI Tracking Enabled
              </div>

            </div>

            <div className="space-y-8">

              {subjects.map((subject, index) => (

                <motion.div
                  key={index}
                  initial={{
                    opacity: 0,
                    x: -20
                  }}
                  animate={{
                    opacity: 1,
                    x: 0
                  }}
                  transition={{
                    delay: index * 0.1
                  }}
                >

                  <div className="flex justify-between mb-3">

                    <span className="text-white text-lg font-semibold">
                      {subject.name}
                    </span>

                    <span className="text-gray-300">
                      {subject.progress}%
                    </span>

                  </div>

                  <div className="w-full bg-white/10 rounded-full h-4 overflow-hidden">

                    <motion.div
                      initial={{
                        width: 0
                      }}
                      animate={{
                        width: `${subject.progress}%`
                      }}
                      transition={{
                        duration: 1
                      }}
                      className="h-4 rounded-full bg-gradient-to-r from-blue-500 via-purple-500 to-cyan-400"
                    ></motion.div>

                  </div>

                </motion.div>
              ))}

            </div>

          </div>

          {/* RIGHT PANEL */}
          <div className="space-y-8">

            {/* ACHIEVEMENTS */}
            <motion.div
              whileHover={{
                scale: 1.02
              }}
              className="bg-white/10 backdrop-blur-xl border border-white/20 rounded-3xl p-6 shadow-2xl"
            >

              <div className="flex items-center gap-3 mb-6">

                <div className="bg-yellow-500 p-3 rounded-2xl">

                  <Award
                    size={24}
                    className="text-white"
                  />

                </div>

                <h2 className="text-2xl font-bold text-white">
                  Achievements
                </h2>

              </div>

              <div className="space-y-4">

                {achievements.map(
                  (achievement, index) => (

                    <div
                      key={index}
                      className="bg-white/10 border border-white/20 rounded-2xl p-4 flex items-center gap-3"
                    >

                      <CheckCircle2
                        size={20}
                        className="text-green-400"
                      />

                      <p className="text-white">
                        {achievement}
                      </p>

                    </div>
                  )
                )}

              </div>

            </motion.div>

            {/* DAILY STREAK */}
            <motion.div
              whileHover={{
                scale: 1.02
              }}
              className="bg-white/10 backdrop-blur-xl border border-white/20 rounded-3xl p-6 shadow-2xl"
            >

              <div className="flex items-center gap-3 mb-6">

                <div className="bg-red-500 p-3 rounded-2xl">

                  <Flame
                    size={24}
                    className="text-white"
                  />

                </div>

                <h2 className="text-2xl font-bold text-white">
                  Learning Streak
                </h2>

              </div>

              <div className="text-center">

                <h1 className="text-6xl font-bold text-white mb-4">
                  7🔥
                </h1>

                <p className="text-gray-300">
                  Days Continuous Learning
                </p>

              </div>

            </motion.div>

          </div>

        </div>

        {/* BOTTOM ANALYTICS */}
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
              Performance Analytics
            </h3>

            <p className="text-gray-300">
              Analyze strengths and identify weak areas for improvement.
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
              Smart Study Goals
            </h3>

            <p className="text-gray-300">
              AI-generated goals to improve consistency and productivity.
            </p>

          </motion.div>

          <motion.div
            whileHover={{
              scale: 1.03
            }}
            className="bg-white/10 backdrop-blur-xl border border-white/20 rounded-3xl p-6 shadow-xl"
          >

            <TrendingUp
              size={40}
              className="text-green-400 mb-4"
            />

            <h3 className="text-white text-2xl font-bold mb-3">
              Growth Tracking
            </h3>

            <p className="text-gray-300">
              Monitor your weekly and monthly academic progress visually.
            </p>

          </motion.div>

        </div>

      </div>

    </MainLayout>
  );
}

export default Progress;