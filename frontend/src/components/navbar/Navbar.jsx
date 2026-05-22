import {
  Menu,
  Bell,
  Search,
  User
} from "lucide-react";

function Navbar({
  toggleSidebar
}) {

  return (

    <div className="flex items-center justify-between mb-8">

      {/* LEFT */}
      <div className="flex items-center gap-4">

        <button
          onClick={toggleSidebar}
          className="lg:hidden bg-white/10 border border-white/20 p-3 rounded-xl text-white"
        >

          <Menu size={24} />

        </button>

        <div>

          <h1 className="text-3xl font-bold text-white">
            Dashboard
          </h1>

          <p className="text-gray-300">
            Welcome back 👋
          </p>

        </div>

      </div>

      {/* RIGHT */}
      <div className="flex items-center gap-4">

        <div className="hidden md:flex items-center bg-white/10 border border-white/20 rounded-2xl px-4 py-3 w-[300px]">

          <Search
            size={20}
            className="text-gray-400"
          />

          <input
            type="text"
            placeholder="Search..."
            className="bg-transparent outline-none text-white ml-3 w-full"
          />

        </div>

        <button className="bg-white/10 border border-white/20 p-3 rounded-2xl text-white">

          <Bell size={22} />

        </button>

        <div className="bg-gradient-to-r from-blue-500 to-purple-500 p-3 rounded-2xl">

          <User
            size={22}
            className="text-white"
          />

        </div>

      </div>

    </div>
  );
}

export default Navbar;