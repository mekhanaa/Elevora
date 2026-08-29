import { useState } from "react"
import axios from "axios"

export default function MultiJD({ resumeSkills, resumeText }) {
  const [jds, setJds] = useState([
    { title: "Job 1", text: "" },
    { title: "Job 2", text: "" },
    { title: "Job 3", text: "" }
  ])
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  const updateJD = (index, field, value) => {
    const updated = [...jds]
    updated[index][field] = value
    setJds(updated)
  }

  const handleCompare = async () => {
    const filled = jds.filter(j => j.text.trim())
    if (filled.length < 2) {
      setError("Please fill at least 2 job descriptions")
      return
    }
    setError("")
    setLoading(true)
    try {
      const res = await axios.post("http://localhost:5000/compare", {
  resume_skills: resumeSkills,
  resume_text_lower: resumeText.toLowerCase(),
  jd_list: filled
})
      setResults(res.data)
    } catch {
      setError("Something went wrong")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-white border border-gray-200 rounded-2xl p-6 mt-6">
      <h2 className="font-semibold text-gray-800 mb-1">
    Multi-JD Comparator
      </h2>
      <p className="text-xs text-gray-400 mb-5">
        Paste up to 3 job descriptions — we'll tell you which fits you best
      </p>

      <div style={{display:"flex", flexDirection:"column", gap:"16px", marginBottom:"16px"}}>
  {jds.map((jd, i) => (
          <div key={i} className="border border-gray-200 rounded-xl p-4">
            <input
              type="text"
              placeholder={`Job title (e.g. Data Analyst at TCS)`}
              value={jd.title}
              onChange={e => updateJD(i, "title", e.target.value)}
              className="w-full text-sm border border-gray-200 rounded-lg px-3 py-2 mb-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
            />
            <textarea
              rows={3}
              placeholder={`Paste job description ${i + 1}...`}
              value={jd.text}
              onChange={e => updateJD(i, "text", e.target.value)}
              className="w-full text-sm border border-gray-200 rounded-lg px-3 py-2 resize-none focus:outline-none focus:ring-2 focus:ring-blue-400"
            />
          </div>
        ))}
      </div>

      {error && <p className="text-red-500 text-sm mb-3">{error}</p>}

      <button
        onClick={handleCompare}
        disabled={loading}
        className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 rounded-xl transition disabled:opacity-50"
      >
        {loading ? "Comparing..." : "Compare Jobs"}
      </button>

      {results.length > 0 && (
        <div className="mt-6 flex flex-col gap-4">
          <p className="text-sm font-medium text-gray-700">
            Best match for you right now:
          </p>

          {results.map((r, i) => (
            <div
              key={i}
              className={`rounded-xl border p-4 ${
                i === 0
                  ? "border-green-300 bg-green-50"
                  : "border-gray-200"
              }`}
            >
              <div className="flex justify-between items-center mb-2">
                <div className="flex items-center gap-2">
                  {i === 0 && (
                    <span className="text-xs bg-green-500 text-white px-2 py-0.5 rounded-full">
                      Best fit
                    </span>
                  )}
                  <span className="font-medium text-sm text-gray-800">
                    {r.title}
                  </span>
                </div>
                <span className={`font-bold text-sm ${
                  r.score >= 70 ? "text-green-600" :
                  r.score >= 40 ? "text-yellow-500" : "text-red-500"
                }`}>{r.score}%</span>
              </div>

              <div className="h-2 bg-gray-100 rounded-full mb-3">
                <div
                  className={`h-full rounded-full ${
                    r.score >= 70 ? "bg-green-500" :
                    r.score >= 40 ? "bg-yellow-400" : "bg-red-400"
                  }`}
                  style={{ width: `${r.score}%` }}
                />
              </div>

              <div className="flex gap-2 flex-wrap mb-3">
                {r.matched.slice(0, 5).map((s, j) => (
                  <span key={j} className="text-xs bg-green-100 text-green-700 border border-green-200 px-2 py-0.5 rounded-full">
                    {s}
                  </span>
                ))}
                {r.missing.slice(0, 3).map((s, j) => (
                  <span key={j} className="text-xs bg-red-100 text-red-600 border border-red-200 px-2 py-0.5 rounded-full">
                    -{s}
                  </span>
                ))}
              </div>

              {/* ATS Density */}
              {r.ats.length > 0 && (
                <div>
                  <p className="text-xs text-gray-400 mb-1">ATS keyword density:</p>
                  <div className="flex flex-col gap-1">
                    {r.ats.slice(0, 4).map((a, j) => (
                      <div key={j} className="flex items-center justify-between text-xs">
                        <span className="text-gray-600">{a.skill}</span>
                        <span className={`font-medium ${
                          a.status === "good" ? "text-green-600" :
                          a.status === "low" ? "text-yellow-500" : "text-red-500"
                        }`}>
                          JD: {a.jd_count}x · Resume: {a.resume_count}x
                          {a.status === "missing" ? " ❌" :
                           a.status === "low" ? " ⚠️" : " ✅"}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}