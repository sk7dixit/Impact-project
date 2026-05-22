import { Brain } from "lucide-react";

function PageLoader() {

  return (

    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-blue-950 to-slate-950">

      <div className="text-center">

        <div className="bg-gradient-to-r from-blue-500 to-purple-500 p-6 rounded-3xl shadow-2xl w-fit mx-auto animate-pulse">

          <Brain
            size={50}
            className="text-white"
          />

        </div>

        <h1 className="text-white text-3xl font-bold mt-6">
          AI Exam Assistant
        </h1>

        <p className="text-gray-300 mt-3">
          Loading your dashboard...
        </p>

      </div>

    </div>
  );
}

export default PageLoader;