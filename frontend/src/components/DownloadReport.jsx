import axios from "axios"

export default function DownloadReport({ result, careers }) {
  const handleDownload = async () => {
    try {
      const res = await axios.post(
        "http://localhost:5000/report",
        {
          match_score: result.match_score,
          matched_skills: result.matched_skills,
          missing_skills: result.missing_skills,
          resume_skills: result.resume_skills,
          resume_filename: result.resume_filename,
          careers: careers
        },
        { responseType: "blob" }
      )

      const url = window.URL.createObjectURL(new Blob([res.data]))
      const link = document.createElement("a")
      link.href = url
      link.setAttribute("download", "SkillMap_Report.pdf")
      document.body.appendChild(link)
      link.click()
      link.remove()
    } catch {
      alert("Failed to generate report. Check backend.")
    }
  }

  return (
    <div className="text-center mt-6">
      <button
        onClick={handleDownload}
        className="bg-green-600 hover:bg-green-700 text-white font-medium px-8 py-3 rounded-xl transition"
      >
        Download PDF Report
      </button>
    </div>
  )
}