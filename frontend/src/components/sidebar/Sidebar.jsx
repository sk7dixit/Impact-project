import { NavLink } from "react-router-dom";

import { motion } from "framer-motion";

import {
  LayoutDashboard,
  Upload,
  MessageSquare,
  Trophy,
  BarChart3,
  User,
  Brain
} from "lucide-react";

function Sidebar({
  mobileOpen,
  setMobileOpen
}) {
  const navLinks = [
    {
      name: "Dashboard",
      path: "/dashboard",
      icon: <LayoutDashboard size={22} />
    },

    {
      name: "Upload",
      path: "/upload",
      icon: <Upload size={22} />
    },

    {
      name: "AI Chat",
      path: "/chat",
      icon: <MessageSquare size={22} />
    },

    {
      name: "Mock Test",
      path: "/mocktest",
      icon: <Trophy size={22} />
    },

    {
      name: "Progress",
      path: "/progress",
      icon: <BarChart3 size={22} />
    },

    {
      name: "Profile",
      path: "/profile",
      icon: <User size={22} />
    }
  ];

  return (

    <motion.div
      initial={{
        x: -100,
        opacity: 0
      }}
      animate={{
        x: 0,
        opacity: 1
      }}
       className={`
    fixed top-0 left-0 z-50 h-screen w-[280px]
    bg-white/10 backdrop-blur-xl border-r border-white/20
    p-6 flex flex-col transition-transform duration-300
    ${
      mobileOpen
        ? "translate-x-0"
        : "-translate-x-full"
    }
    lg:translate-x-0
  `}
    >

      {/* LOGO */}
      <div className="flex items-center gap-4 mb-14">

        <div className="bg-gradient-to-r from-blue-500 to-purple-500 p-3 rounded-2xl shadow-xl">

          <Brain
            size={30}
            className="text-white"
          />

        </div>

        <div>

          <h1 className="text-2xl font-bold text-white">
            AI Assistant
          </h1>

          <p className="text-gray-300 text-sm">
            Smart Learning
          </p>

        </div>

      </div>

      {/* NAVIGATION */}
      <div className="flex flex-col gap-4">

  {navLinks.map((link, index) => (

    <NavLink
      key={index}
      to={link.path}

      onClick={() =>
        setMobileOpen(false)
      }

      className={({ isActive }) =>
        `flex items-center gap-4 px-5 py-4 rounded-2xl transition-all duration-300 ${
          isActive
            ? "bg-gradient-to-r from-blue-500 to-purple-500 text-white shadow-xl"
            : "text-gray-300 hover:bg-white/10 hover:text-white"
        }`
      }
    >

      {link.icon}

      <span className="font-medium text-lg">
        {link.name}
      </span>

    </NavLink>

  ))}

</div>

      {/* BOTTOM CARD */}
      <div className="mt-auto bg-gradient-to-r from-blue-500 to-purple-500 rounded-3xl p-6 shadow-2xl">

        <h2 className="text-white text-2xl font-bold">
          AI Powered 🚀
        </h2>

        <p className="text-blue-100 mt-3 leading-relaxed">
          Smart exam preparation with AI assistance and analytics.
        </p>

      </div>

    </motion.div>
  );
}

export default Sidebar;