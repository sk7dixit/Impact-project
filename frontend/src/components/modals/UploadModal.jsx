function UploadModal({
  files,
  handleUpload,
  closeModal,
  uploading,
  uploadProgress
}) {

  return (

    <div className="fixed inset-0 bg-black/50 flex justify-center items-center z-50 px-4">

      <div className="bg-white w-full max-w-2xl rounded-2xl p-8 max-h-[90vh] overflow-y-auto">

        {/* Title */}
        <h2 className="text-3xl font-bold mb-6">
          Selected Files
        </h2>

        {/* File List */}
        <div className="space-y-4 mb-6">

          {files.map((file, index) => (

            <div
              key={index}
              className="border rounded-xl p-4"
            >

              <h3 className="font-semibold truncate">
                {file.name}
              </h3>

              <p className="text-sm text-gray-500 mt-1">
                {(file.size / 1024).toFixed(2)} KB
              </p>

            </div>
          ))}

        </div>

        {/* Progress Bar */}
        {uploading && (

          <div className="mb-6">

            <div className="w-full bg-gray-300 rounded-full h-4 overflow-hidden">

              <div
                className="bg-blue-600 h-4 transition-all duration-300"
                style={{
                  width: `${uploadProgress}%`
                }}
              ></div>

            </div>

            <p className="text-sm mt-2">
              Uploading... {uploadProgress}%
            </p>

          </div>
        )}

        {/* Buttons */}
        <div className="flex justify-end gap-4">

          {/* Cancel */}
          <button
            onClick={closeModal}
            disabled={uploading}
            className="bg-gray-300 hover:bg-gray-400 px-5 py-2 rounded-lg transition"
          >
            Cancel
          </button>

          {/* Upload */}
          <button
            onClick={handleUpload}
            disabled={uploading || files.length === 0}
            className={`px-5 py-2 rounded-lg text-white transition ${
              uploading || files.length === 0
                ? "bg-gray-400"
                : "bg-blue-600 hover:bg-blue-700"
            }`}
          >
            {uploading ? "Uploading..." : "Upload"}
          </button>

        </div>

      </div>

    </div>
  );
}

export default UploadModal;