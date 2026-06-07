import { useState } from "react"
import axios from "axios"

export default function UploadForm({ onResult }) {
  const [resume, setResume] = useState(null)
  const [jdText, setJdText] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  const handleSubmit = async () => {
    if (!resume || !jdText.trim()) {
      setError("Please upload a resume and paste a job description.")
      return
    }
    setError("")
    setLoading(true)

    const formData = new FormData()
    formData.append("resume", resume)
    formData.append("jd_text", jdText)

    try {
      const res = await axios.post("http://localhost:5000/analyze", formData)
      onResult(res.data)
    } catch (err) {
      setError("Something went wrong. Check if the backend is running.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex flex-col gap-6">
      <div className="border-2 border-dashed border-gray-300 rounded-xl p-6 text-center">
        <p className="text-gray-500 mb-3 text-sm">Upload your resume (PDF)</p>
        <input
          type="file"
          accept=".pdf"
          onChange={e => setResume(e.target.files[0])}
          className="text-sm"
        />
        {resume && (
          <p className="text-green-600 text-sm mt-2">✓ {resume.name}</p>
        )}
      </div>

      <textarea
        rows={6}
        placeholder="Paste job description here..."
        value={jdText}
        onChange={e => setJdText(e.target.value)}
        className="border border-gray-300 rounded-xl p-4 text-sm resize-none focus:outline-none focus:ring-2 focus:ring-blue-400"
      />

      {error && <p className="text-red-500 text-sm">{error}</p>}

      <button
        onClick={handleSubmit}
        disabled={loading}
        className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 rounded-xl transition disabled:opacity-50"
      >
        {loading ? "Analyzing..." : "Analyze Match"}
      </button>
    </div>
  )
}