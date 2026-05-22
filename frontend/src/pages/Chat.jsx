import MainLayout from "../layouts/MainLayout";

import ChatBox from "../components/chat/ChatBox";

function Chat() {

  return (

    <MainLayout>

      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-950 to-slate-950 p-6">

        <ChatBox />

      </div>

    </MainLayout>
  );
}

export default Chat;