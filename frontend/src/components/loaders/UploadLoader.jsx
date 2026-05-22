import { UploadCloud } from "lucide-react";

function UploadLoader() {

  return (

    <div className="flex flex-col items-center justify-center py-10">

      <div className="bg-gradient-to-r from-blue-500 to-purple-500 p-5 rounded-3xl animate-bounce">

        <UploadCloud
          size={40}
          className="text-white"
        />

      </div>

      <p className="text-white mt-5 text-lg">
        Uploading files...
      </p>

    </div>
  );
}

export default UploadLoader;