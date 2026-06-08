import { useState } from "react"
import axios from "axios"

export default function DownloadReport({ result, careers }) {
  const [showModal, setShowModal] = useState(false)
  const [name, setName] = useState("")
  const [email, setEmail] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  const handleDownload = async () => {
    if (!name.trim()) {
      setError("Please enter your name")
      return
    }
    setError("")
    setLoading(true)

    try {
      const res = await axios.post(
        "http://localhost:5000/report",
        {
          match_score: result.match_score,
          matched_skills: result.matched_skills,
          missing_skills: result.missing_skills,
          resume_skills: result.resume_skills,
          resume_filename: result.resume_filename,
          candidate_name: name,
          candidate_email: email,
          careers: careers
        },
        { responseType: "blob" }
      )

      const url = window.URL.createObjectURL(new Blob([res.data]))
      const link = document.createElement("a")
      link.href = url
      link.setAttribute("download", `SkillMap_${name.replace(" ", "_")}_Report.pdf`)
      document.body.appendChild(link)
      link.click()
      link.remove()
      setShowModal(false)
      setName("")
      setEmail("")
    } catch {
      setError("Failed to generate report. Check backend.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      {/* Download Button */}
      <div className="text-center mt-6">
        <button
          onClick={() => setShowModal(true)}
          className="bg-green-600 hover:bg-green-700 text-white font-medium px-8 py-3 rounded-xl transition"
        >
          Download PDF Report
        </button>
      </div>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
          <div className="bg-white rounded-2xl shadow-xl p-8 w-full max-w-sm mx-4">

            <h2 className="text-lg font-semibold text-gray-800 mb-1">
              Almost there!
            </h2>
            <p className="text-xs text-gray-400 mb-6">
              Your details will appear on the report
            </p>

            <div className="flex flex-col gap-4">
              <div>
                <label className="text-xs font-medium text-gray-600 mb-1 block">
                  Full Name *
                </label>
                <input
                  type="text"
                  value={name}
                  onChange={e => setName(e.target.value)}
                  className="w-full text-sm border border-gray-200 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
                />
              </div>

              <div>
                <label className="text-xs font-medium text-gray-600 mb-1 block">
                  Email (optional)
                </label>
                <input
                  type="email"
                  value={email}
                  onChange={e => setEmail(e.target.value)}
                  className="w-full text-sm border border-gray-200 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
                />
              </div>

              {error && (
                <p className="text-red-500 text-xs">{error}</p>
              )}

              <div className="flex gap-3 mt-2">
                <button
                  onClick={() => setShowModal(false)}
                  className="flex-1 border border-gray-200 text-gray-600 text-sm py-2 rounded-xl hover:bg-gray-50 transition"
                >
                  Cancel
                </button>
                <button
                  onClick={handleDownload}
                  disabled={loading}
                  className="flex-1 bg-green-600 hover:bg-green-700 text-white text-sm py-2 rounded-xl transition disabled:opacity-50"
                >
                  {loading ? "Generating..." : "Download"}
                </button>
              </div>
            </div>

          </div>
        </div>
      )}
    </>
  )
}