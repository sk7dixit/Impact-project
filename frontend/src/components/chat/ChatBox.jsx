import { useState } from "react";

import { motion } from "framer-motion";

import {
  Send,
  Bot,
  User,
  Sparkles
} from "lucide-react";

import ChatLoader from "../loaders/ChatLoader";

function ChatBox() {

  const [messages, setMessages] = useState([
    {
      sender: "ai",
      text:
        "Hello 👋 I am your AI Exam Preparation Assistant.\n\nAsk me to:\n• Explain topics\n• Summarize concepts\n• Create quizzes\n• Check answers\n• Help with Java, Python, DBMS, DSA, AI, ML, OS, CN, Cyber Security and more 🚀"
    }
  ]);

  const [input, setInput] = useState("");

  const [loading, setLoading] =
    useState(false);

  const [currentQuizAnswer, setCurrentQuizAnswer] =
    useState("");

  // AI LOGIC
  const getAIResponse = (
    question
  ) => {

    const q =
      question.toLowerCase();

    // SUBJECTS

    if (q.includes("java")) {

      return "☕ Java is an object-oriented programming language used for web, enterprise, and Android development.\n\nKey Features:\n• Platform Independent\n• Secure\n• Multithreaded\n• Robust\n• OOP Based";
    }

    if (q.includes("python")) {

      return "🐍 Python is a high-level programming language widely used in AI, Machine Learning, Data Science, and Web Development.\n\nAdvantages:\n• Easy Syntax\n• Huge Libraries\n• Beginner Friendly\n• AI & ML Support";
    }

    if (q.includes("dbms")) {

      return "🗄️ DBMS stands for Database Management System.\n\nIt helps:\n• Store Data\n• Retrieve Data\n• Manage Databases\n• Reduce Redundancy\n\nExamples:\nMySQL, PostgreSQL, MongoDB";
    }

    if (q.includes("dsa")) {

      return "📚 DSA stands for Data Structures and Algorithms.\n\nImportant Topics:\n• Arrays\n• Linked Lists\n• Trees\n• Graphs\n• Sorting\n• Searching";
    }

    if (q.includes("ai")) {

      return "🤖 Artificial Intelligence enables machines to mimic human intelligence.\n\nApplications:\n• Chatbots\n• Self Driving Cars\n• Recommendation Systems\n• Image Recognition";
    }

    if (q.includes("ml")) {

      return "📈 Machine Learning is a subset of AI where systems learn from data.\n\nTypes:\n• Supervised Learning\n• Unsupervised Learning\n• Reinforcement Learning";
    }

    if (q.includes("os")) {

      return "💻 Operating System manages hardware and software resources.\n\nFunctions:\n• Process Management\n• Memory Management\n• File Handling\n• Security";
    }

    if (q.includes("cn")) {

      return "🌐 Computer Networks connect computers for communication.\n\nConcepts:\n• TCP/IP\n• Routing\n• Switching\n• OSI Model";
    }

    if (q.includes("cyber")) {

      return "🔐 Cyber Security protects systems and networks from attacks.\n\nConcepts:\n• Encryption\n• Firewalls\n• Authentication\n• Malware Protection";
    }

    if (q.includes("daa")) {

      return "⚡ DAA stands for Design and Analysis of Algorithms.\n\nTopics:\n• Greedy Algorithms\n• Divide & Conquer\n• Dynamic Programming\n• Backtracking";
    }

    // SUMMARY

    if (
      q.includes("summarize") ||
      q.includes("summary")
    ) {

      return "📄 Summary:\n\nThis topic mainly focuses on understanding the core concepts, applications, advantages, and real-world uses. Important points are simplified for quick revision and exam preparation.";
    }

    // QUIZ

    if (
      q.includes("quiz") ||
      q.includes("mcq")
    ) {

      setCurrentQuizAnswer(
        "bfs"
      );

      return "📝 Quiz Time!\n\nQuestion:\nWhich traversal technique uses Queue data structure?\n\nA) DFS\nB) BFS\nC) Binary Search\nD) Stack";
    }

    // ANSWER CHECKING

    if (
      currentQuizAnswer &&
      (
        q === "b" ||
        q === "bfs"
      )
    ) {

      setCurrentQuizAnswer("");

      return "✅ Correct Answer!\n\nExcellent work 🎉\nYou are improving your problem-solving skills.";
    }

    if (
      currentQuizAnswer &&
      (
        q === "a" ||
        q === "dfs" ||
        q === "c" ||
        q === "d"
      )
    ) {

      setCurrentQuizAnswer("");

      return "❌ Incorrect Answer.\n\nCorrect Answer: BFS\n\nExplanation:\nBreadth First Search (BFS) uses Queue data structure for level-order traversal.";
    }

    // DEFAULT

    return "🤖 I can help you with:\n• Definitions\n• Summaries\n• Quiz Generation\n• Answer Checking\n• AI/ML\n• Java\n• Python\n• DBMS\n• DSA\n• Cyber Security\n• Operating Systems\nand more 🚀";
  };

  // SEND MESSAGE
  const sendMessage = () => {

    if (!input.trim()) return;

    const userMessage = {
      sender: "user",
      text: input
    };

    setMessages((prev) => [
      ...prev,
      userMessage
    ]);

    const currentInput = input;

    setInput("");

    setLoading(true);

    setTimeout(() => {

      const aiReply =
        getAIResponse(
          currentInput
        );

      setMessages((prev) => [
        ...prev,
        {
          sender: "ai",
          text: aiReply
        }
      ]);

      setLoading(false);

    }, 1200);
  };

  return (

    <div className="relative h-[85vh] overflow-hidden rounded-3xl border border-white/20 bg-white/10 backdrop-blur-xl shadow-2xl">

      {/* Background Glow */}
      <div className="absolute inset-0 bg-gradient-to-br from-blue-500/20 via-purple-500/10 to-cyan-500/20"></div>

      {/* Header */}
      <div className="relative z-10 flex items-center gap-4 p-6 border-b border-white/20 bg-white/10 backdrop-blur-lg">

        <div className="p-3 rounded-2xl bg-gradient-to-r from-blue-500 to-purple-500 text-white shadow-lg">

          <Bot size={28} />

        </div>

        <div>

          <h1 className="text-2xl font-bold text-white">
            AI Exam Assistant
          </h1>

          <p className="text-gray-200 text-sm">
            Smart Study Companion 🚀
          </p>

        </div>

      </div>

      {/* Messages */}
      <div className="relative z-10 h-[68vh] overflow-y-auto p-6 space-y-4">

        {messages.map((msg, index) => (

          <motion.div
            key={index}
            initial={{
              opacity: 0,
              y: 20
            }}
            animate={{
              opacity: 1,
              y: 0
            }}
            transition={{
              duration: 0.3
            }}
            className={`flex ${
              msg.sender === "user"
                ? "justify-end"
                : "justify-start"
            }`}
          >

            <div
              className={`max-w-[75%] rounded-3xl p-5 shadow-xl border ${
                msg.sender === "user"
                  ? "bg-blue-600 text-white border-blue-400"
                  : "bg-white/20 text-white backdrop-blur-xl border-white/20"
              }`}
            >

              <div className="flex items-center gap-2 mb-2">

                {msg.sender === "user" ? (
                  <User size={18} />
                ) : (
                  <Sparkles size={18} />
                )}

                <span className="font-semibold">
                  {msg.sender === "user"
                    ? "You"
                    : "AI Assistant"}
                </span>

              </div>

              <p className="whitespace-pre-line leading-relaxed">
                {msg.text}
              </p>

            </div>

          </motion.div>
        ))}

        {loading && (
          <ChatLoader />
        )}

      </div>

      {/* Input */}
      <div className="absolute bottom-0 left-0 right-0 z-10 p-5 pt-10 border-t border-white/20 bg-white/10 backdrop-blur-xl">

        <div className="flex gap-4">

          <input
            type="text"
            placeholder="Ask anything about your studies..."
            value={input}
            onChange={(e) =>
              setInput(e.target.value)
            }
            onKeyDown={(e) => {

              if (
                e.key === "Enter"
              ) {

                sendMessage();
              }
            }}
            className="flex-1 px-5 py-4 rounded-2xl bg-white/20 backdrop-blur-lg border border-white/20 text-white placeholder:text-gray-300 outline-none focus:ring-2 focus:ring-blue-400"
          />

          <button
            onClick={sendMessage}
            className="px-6 mt-4 rounded-2xl bg-gradient-to-r from-blue-500 to-purple-500 text-white shadow-xl hover:scale-105 transition-all duration-300"
          >

            <Send size={22} />

          </button>

        </div>

      </div>

    </div>
  );
}

export default ChatBox;