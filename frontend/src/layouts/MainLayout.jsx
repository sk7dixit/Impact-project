import { useState } from "react";

import Sidebar from "../components/sidebar/Sidebar";

import Navbar from "../components/navbar/Navbar";

function MainLayout({ children }) {

  const [mobileOpen, setMobileOpen] =
    useState(false);

  return (

    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-950 to-slate-950 flex">

      {/* SIDEBAR */}
      <Sidebar
        mobileOpen={mobileOpen}
        setMobileOpen={setMobileOpen}
      />

      {/* MOBILE OVERLAY */}
      {mobileOpen && (

        <div
          onClick={() =>
            setMobileOpen(false)
          }
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
        />

      )}

      {/* MAIN CONTENT */}
      <div className="flex-1 lg:ml-[280px] p-4 md:p-6">

        {/* NAVBAR */}
        <Navbar
          toggleSidebar={() =>
            setMobileOpen(true)
          }
        />

        {/* PAGE CONTENT */}
        {children}

      </div>

    </div>
  );
}

export default MainLayout;