function ChatLoader() {

  return (

    <div className="flex justify-start mb-4 animate-pulse">

      <div className="bg-white/10 backdrop-blur-xl border border-white/20 px-5 py-4 rounded-3xl max-w-[250px]">

        <div className="flex gap-2">

          <div className="w-3 h-3 bg-blue-400 rounded-full animate-bounce"></div>

          <div className="w-3 h-3 bg-purple-400 rounded-full animate-bounce delay-150"></div>

          <div className="w-3 h-3 bg-pink-400 rounded-full animate-bounce delay-300"></div>

        </div>

      </div>

    </div>
  );
}

export default ChatLoader;