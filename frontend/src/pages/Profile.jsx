import MainLayout from "../layouts/MainLayout";

import { motion } from "framer-motion";

import {
  User,
  Mail,
  GraduationCap,
  Brain,
  Trophy,
  Clock3,
  Edit3,
  Camera,
  BookOpen,
  Target,
  Sparkles,
  Flame,
  ShieldCheck
} from "lucide-react";

function Profile() {

  const skills = [
    "Java",
    "Python",
    "DBMS",
    "DSA",
    "AI",
    "ML",
    "Cyber Security"
  ];

  const achievements = [
    "Top Performer in AI Quiz",
    "Completed 100+ AI Chats",
    "7 Days Learning Streak",
    "Uploaded 50+ Study Notes"
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
          className="mb-10"
        >

          <h1 className="text-5xl font-bold text-white">
            My Profile 👤
          </h1>

          <p className="text-gray-300 mt-3 text-lg">
            Manage your learning profile and AI study journey.
          </p>

        </motion.div>

        {/* PROFILE CARD */}
        <motion.div
          initial={{
            opacity: 0,
            scale: 0.95
          }}
          animate={{
            opacity: 1,
            scale: 1
          }}
          className="bg-white/10 backdrop-blur-xl border border-white/20 rounded-3xl p-8 shadow-2xl"
        >

          <div className="flex flex-col lg:flex-row gap-10">

            {/* LEFT SIDE */}
            <div className="flex flex-col items-center lg:w-[30%]">

              {/* PROFILE IMAGE */}
              <div className="relative">

                <div className="w-40 h-40 rounded-full bg-gradient-to-r from-blue-500 to-purple-500 p-1 shadow-2xl">

                  <div className="w-full h-full rounded-full bg-slate-900 flex items-center justify-center">

                    <User
                      size={80}
                      className="text-white"
                    />

                  </div>

                </div>

                {/* CAMERA ICON */}
                <button className="absolute bottom-2 right-2 bg-blue-500 hover:bg-blue-600 p-3 rounded-full shadow-xl transition-all">

                  <Camera
                    size={20}
                    className="text-white"
                  />

                </button>

              </div>

              {/* NAME */}
              <h2 className="text-3xl font-bold text-white mt-6">
                Student Name
              </h2>

              <p className="text-gray-300 mt-2">
                AI Exam Preparation Assistant User
              </p>

              {/* EDIT BUTTON */}
              <button className="mt-6 bg-gradient-to-r from-blue-500 to-purple-500 text-white px-6 py-3 rounded-2xl shadow-xl hover:scale-105 transition-all duration-300 flex items-center gap-3">

                <Edit3 size={20} />

                Edit Profile

              </button>

            </div>

            {/* RIGHT SIDE */}
            <div className="flex-1">

              {/* USER DETAILS */}
              <div className="grid md:grid-cols-2 gap-6">

                <div className="bg-white/10 border border-white/20 rounded-2xl p-5">

                  <div className="flex items-center gap-3 mb-3">

                    <Mail
                      size={22}
                      className="text-blue-400"
                    />

                    <h3 className="text-white font-bold">
                      Email
                    </h3>

                  </div>

                  <p className="text-gray-300">
                    student@example.com
                  </p>

                </div>

                <div className="bg-white/10 border border-white/20 rounded-2xl p-5">

                  <div className="flex items-center gap-3 mb-3">

                    <GraduationCap
                      size={22}
                      className="text-purple-400"
                    />

                    <h3 className="text-white font-bold">
                      Department
                    </h3>

                  </div>

                  <p className="text-gray-300">
                    Computer Engineering
                  </p>

                </div>

                <div className="bg-white/10 border border-white/20 rounded-2xl p-5">

                  <div className="flex items-center gap-3 mb-3">

                    <BookOpen
                      size={22}
                      className="text-green-400"
                    />

                    <h3 className="text-white font-bold">
                      Semester
                    </h3>

                  </div>

                  <p className="text-gray-300">
                    6th Semester
                  </p>

                </div>

                <div className="bg-white/10 border border-white/20 rounded-2xl p-5">

                  <div className="flex items-center gap-3 mb-3">

                    <ShieldCheck
                      size={22}
                      className="text-cyan-400"
                    />

                    <h3 className="text-white font-bold">
                      Account Status
                    </h3>

                  </div>

                  <p className="text-green-300">
                    Verified ✅
                  </p>

                </div>

              </div>

              {/* AI STATS */}
              <div className="grid md:grid-cols-3 gap-5 mt-8">

                <motion.div
                  whileHover={{
                    scale: 1.03
                  }}
                  className="bg-white/10 border border-white/20 rounded-2xl p-5 shadow-xl"
                >

                  <div className="bg-blue-500 w-fit p-3 rounded-2xl mb-4">

                    <Brain
                      size={24}
                      className="text-white"
                    />

                  </div>

                  <h2 className="text-gray-300">
                    AI Chats
                  </h2>

                  <h1 className="text-4xl font-bold text-white mt-2">
                    128
                  </h1>

                </motion.div>

                <motion.div
                  whileHover={{
                    scale: 1.03
                  }}
                  className="bg-white/10 border border-white/20 rounded-2xl p-5 shadow-xl"
                >

                  <div className="bg-green-500 w-fit p-3 rounded-2xl mb-4">

                    <Trophy
                      size={24}
                      className="text-white"
                    />

                  </div>

                  <h2 className="text-gray-300">
                    Quiz Accuracy
                  </h2>

                  <h1 className="text-4xl font-bold text-white mt-2">
                    92%
                  </h1>

                </motion.div>

                <motion.div
                  whileHover={{
                    scale: 1.03
                  }}
                  className="bg-white/10 border border-white/20 rounded-2xl p-5 shadow-xl"
                >

                  <div className="bg-orange-500 w-fit p-3 rounded-2xl mb-4">

                    <Clock3
                      size={24}
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

            </div>

          </div>

        </motion.div>

        {/* SKILLS + ACHIEVEMENTS */}
        <div className="grid lg:grid-cols-2 gap-8 mt-10">

          {/* SKILLS */}
          <motion.div
            whileHover={{
              scale: 1.01
            }}
            className="bg-white/10 backdrop-blur-xl border border-white/20 rounded-3xl p-8 shadow-2xl"
          >

            <div className="flex items-center gap-3 mb-8">

              <div className="bg-gradient-to-r from-blue-500 to-purple-500 p-3 rounded-2xl">

                <Sparkles
                  size={24}
                  className="text-white"
                />

              </div>

              <h2 className="text-3xl font-bold text-white">
                Skills & Subjects
              </h2>

            </div>

            <div className="flex flex-wrap gap-4">

              {skills.map((skill, index) => (

                <motion.div
                  key={index}
                  whileHover={{
                    scale: 1.08
                  }}
                  className="bg-gradient-to-r from-blue-500 to-purple-500 text-white px-5 py-3 rounded-2xl shadow-lg cursor-pointer"
                >

                  {skill}

                </motion.div>
              ))}

            </div>

          </motion.div>

          {/* ACHIEVEMENTS */}
          <motion.div
            whileHover={{
              scale: 1.01
            }}
            className="bg-white/10 backdrop-blur-xl border border-white/20 rounded-3xl p-8 shadow-2xl"
          >

            <div className="flex items-center gap-3 mb-8">

              <div className="bg-gradient-to-r from-orange-500 to-red-500 p-3 rounded-2xl">

                <Flame
                  size={24}
                  className="text-white"
                />

              </div>

              <h2 className="text-3xl font-bold text-white">
                Achievements
              </h2>

            </div>

            <div className="space-y-5">

              {achievements.map(
                (achievement, index) => (

                  <motion.div
                    key={index}
                    whileHover={{
                      scale: 1.02
                    }}
                    className="bg-white/10 border border-white/20 rounded-2xl p-5 flex items-center gap-4"
                  >

                    <Target
                      size={22}
                      className="text-green-400"
                    />

                    <p className="text-white">
                      {achievement}
                    </p>

                  </motion.div>
                )
              )}

            </div>

          </motion.div>

        </div>

      </div>

    </MainLayout>
  );
}

export default Profile;