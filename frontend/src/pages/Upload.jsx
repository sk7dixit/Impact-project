import MainLayout from "../layouts/MainLayout";

import { useState, useRef } from "react";

import { motion } from "framer-motion";

import {
  UploadCloud,
  FileText,
  FolderOpen,
  Trash2,
  CheckCircle2
} from "lucide-react";

function Upload() {

  const [files, setFiles] = useState([]);

  const [uploading, setUploading] =
    useState(false);

  const [uploaded, setUploaded] =
    useState(false);

  const fileInputRef = useRef(null);

  // FILE SELECT
  const handleFileChange = (e) => {

    const selectedFiles = Array.from(
      e.target.files
    );

    setFiles(selectedFiles);

    setUploaded(false);
  };

  // FAKE UPLOAD
  const handleUpload = () => {

    if (files.length === 0) return;

    setUploading(true);

    setTimeout(() => {

      setUploading(false);

      setUploaded(true);

    }, 2000);
  };

  // REMOVE FILE
  const removeFile = (index) => {

    const updatedFiles = [...files];

    updatedFiles.splice(index, 1);

    setFiles(updatedFiles);
  };

  return (

    <MainLayout>

      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-950 to-slate-950 p-6">

        {/* Header */}
        <motion.div
          initial={{
            opacity: 0,
            y: -20
          }}
          animate={{
            opacity: 1,
            y: 0
          }}
          className="mb-8"
        >

          <h1 className="text-5xl font-bold text-white">
            Upload Study Material 📚
          </h1>

          <p className="text-gray-300 mt-3 text-lg">
            Upload notes, PDFs, assignments, and study resources.
          </p>

        </motion.div>

        {/* Upload Box */}
        <motion.div
          initial={{
            opacity: 0,
            scale: 0.95
          }}
          animate={{
            opacity: 1,
            scale: 1
          }}
          className="bg-white/10 backdrop-blur-xl border border-white/20 rounded-3xl p-10 shadow-2xl"
        >

          {/* Upload Area */}
          <div
            onClick={() =>
              fileInputRef.current.click()
            }
            className="border-2 border-dashed border-blue-400 rounded-3xl p-14 text-center cursor-pointer hover:bg-white/10 transition-all duration-300"
          >

            <div className="flex justify-center mb-5">

              <div className="bg-gradient-to-r from-blue-500 to-purple-500 p-5 rounded-full shadow-xl">

                <UploadCloud
                  size={50}
                  className="text-white"
                />

              </div>

            </div>

            <h2 className="text-3xl font-bold text-white mb-3">
              Drag & Drop Files
            </h2>

            <p className="text-gray-300">
              or click to browse your study material
            </p>

            <input
              type="file"
              multiple
              ref={fileInputRef}
              onChange={handleFileChange}
              className="hidden"
            />

          </div>

          {/* File List */}
          {files.length > 0 && (

            <div className="mt-10">

              <div className="flex items-center justify-between mb-5">

                <h2 className="text-2xl font-bold text-white">
                  Selected Files
                </h2>

                <span className="bg-blue-500 text-white px-4 py-2 rounded-full text-sm">
                  {files.length} Files
                </span>

              </div>

              <div className="space-y-4">

                {files.map((file, index) => (

                  <motion.div
                    key={index}
                    initial={{
                      opacity: 0,
                      x: -20
                    }}
                    animate={{
                      opacity: 1,
                      x: 0
                    }}
                    className="bg-white/10 border border-white/20 backdrop-blur-xl rounded-2xl p-5 flex items-center justify-between shadow-lg"
                  >

                    <div className="flex items-center gap-4">

                      <div className="bg-blue-500 p-3 rounded-xl">

                        <FileText
                          size={24}
                          className="text-white"
                        />

                      </div>

                      <div>

                        <h3 className="text-white font-semibold">
                          {file.name}
                        </h3>

                        <p className="text-gray-300 text-sm">
                          {(file.size / 1024).toFixed(2)} KB
                        </p>

                      </div>

                    </div>

                    <button
                      onClick={() =>
                        removeFile(index)
                      }
                      className="bg-red-500 hover:bg-red-600 p-3 rounded-xl transition"
                    >

                      <Trash2
                        size={20}
                        className="text-white"
                      />

                    </button>

                  </motion.div>
                ))}

              </div>

              {/* Upload Button */}
              <div className="mt-8 flex gap-5">

                <button
                  onClick={handleUpload}
                  className="bg-gradient-to-r from-blue-500 to-purple-500 text-white px-8 py-4 rounded-2xl shadow-xl hover:scale-105 transition-all duration-300 font-semibold"
                >

                  {uploading
                    ? "Uploading..."
                    : "Upload Files"}

                </button>

                <button
                  onClick={() =>
                    setFiles([])
                  }
                  className="bg-white/10 border border-white/20 text-white px-8 py-4 rounded-2xl hover:bg-white/20 transition-all duration-300"
                >

                  Clear All

                </button>

              </div>

              {/* Success */}
              {uploaded && (

                <motion.div
                  initial={{
                    opacity: 0,
                    y: 20
                  }}
                  animate={{
                    opacity: 1,
                    y: 0
                  }}
                  className="mt-8 bg-green-500/20 border border-green-400 text-green-200 rounded-2xl p-5 flex items-center gap-3"
                >

                  <CheckCircle2 size={28} />

                  <div>

                    <h3 className="font-bold">
                      Upload Successful 🚀
                    </h3>

                    <p>
                      Your study materials are ready for AI analysis.
                    </p>

                  </div>

                </motion.div>
              )}

            </div>
          )}

        </motion.div>

        {/* Bottom Cards */}
        <div className="grid md:grid-cols-3 gap-6 mt-10">

          <motion.div
            whileHover={{
              scale: 1.03
            }}
            className="bg-white/10 backdrop-blur-xl border border-white/20 rounded-3xl p-6 shadow-xl"
          >

            <FolderOpen
              size={40}
              className="text-blue-400 mb-4"
            />

            <h3 className="text-white text-xl font-bold mb-2">
              Organize Notes
            </h3>

            <p className="text-gray-300">
              Keep your study materials organized subject-wise.
            </p>

          </motion.div>

          <motion.div
            whileHover={{
              scale: 1.03
            }}
            className="bg-white/10 backdrop-blur-xl border border-white/20 rounded-3xl p-6 shadow-xl"
          >

            <UploadCloud
              size={40}
              className="text-purple-400 mb-4"
            />

            <h3 className="text-white text-xl font-bold mb-2">
              Fast Uploads
            </h3>

            <p className="text-gray-300">
              Upload PDFs, docs, and notes instantly.
            </p>

          </motion.div>

          <motion.div
            whileHover={{
              scale: 1.03
            }}
            className="bg-white/10 backdrop-blur-xl border border-white/20 rounded-3xl p-6 shadow-xl"
          >

            <CheckCircle2
              size={40}
              className="text-green-400 mb-4"
            />

            <h3 className="text-white text-xl font-bold mb-2">
              AI Ready
            </h3>

            <p className="text-gray-300">
              Materials prepared for summaries, quizzes, and analysis.
            </p>

          </motion.div>

        </div>

      </div>

    </MainLayout>
  );
}

export default Upload;