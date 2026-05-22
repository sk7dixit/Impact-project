function MessageBubble({
  sender,
  text
}) {

  return (

    <div
      className={`mb-4 flex ${
        sender === "user"
          ? "justify-end"
          : "justify-start"
      }`}
    >

      <div
        className={`px-4 py-3 rounded-2xl max-w-[75%] ${
          sender === "user"
            ? "bg-blue-600 text-white"
            : "bg-white text-black shadow"
        }`}
      >

        {text}

      </div>

    </div>
  );
}

export default MessageBubble;