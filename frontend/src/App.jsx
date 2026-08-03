import { useState } from "react"
import axios from "axios"
import UploadForm from "./components/UploadForm"
import ResultCard from "./components/ResultCard"
import CareerGraph from "./components/CareerGraph"
import CareerCards from "./components/CareerCards"
import DownloadReport from "./components/DownloadReport"
import MultiJD from "./components/MultiJD"
import Navbar from "./components/Navbar"

export default function App() {
  const [result, setResult] = useState(null)
  const [careers, setCareers] = useState([])
  const [resumeText, setResumeText] = useState("")

  const handleResult = async (data) => {
    setResult(data)
    setResumeText(data.resume_text || "")
    const res = await axios.post("http://localhost:5000/careers", {
      resume_skills: data.resume_skills
    })
    setCareers(res.data)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />

      <div className="max-w-2xl mx-auto px-4 py-10">

        {/* Upload Form */}
        <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6 mb-6">
          <UploadForm onResult={handleResult} />
        </div>

        {/* Results */}
        {result && (
          <>
            <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6 mb-6">
              <ResultCard result={result} />
            </div>

            {careers.length > 0 && (
              <>
                <div className="mb-6">
                  <CareerGraph
                    resumeSkills={result.resume_skills}
                    careers={careers}
                  />
                </div>
                <CareerCards careers={careers} />
                <DownloadReport result={result} careers={careers} />
                <MultiJD resumeSkills={result.resume_skills} result={result} />
              </>
            )}
          </>
        )}

        {/* About Section */}
        <div id="about" className="bg-white rounded-2xl border border-gray-200 p-8 mt-10">
          <h2 className="text-lg font-bold text-gray-900 mb-1">About Elevora</h2>
          <p className="text-xs text-gray-400 mb-4">Resume Intelligence & Career Path Engine</p>
          <div className="flex flex-col gap-3 text-sm text-gray-600 leading-relaxed">
            <p>
              <b className="text-gray-800">Elevora</b> is a smart resume analyzer built for students and freshers entering the job market.
            </p>
            <p>
              Upload your resume, paste a job description, and instantly see how well you match — with a detailed breakdown of matched skills, missing skills, and your ATS keyword density.
            </p>
            <p>
              Elevora maps your current skills to real career paths — showing you exactly how ready you are for roles like Data Analyst, Full Stack Developer, ML Engineer, and more.
            </p>
            <p>
              Use the <b className="text-gray-800">Multi-JD Comparator</b> to compare up to 3 job descriptions at once and find out which role fits you best right now.
            </p>
            <p>
              Download a complete <b className="text-gray-800">PDF report</b> with your match score, skill gaps, career readiness table, and a personalized learning roadmap.
            </p>
          </div>
        </div>

        {/* Help Center Section */}
        <div id="help" className="bg-white rounded-2xl border border-gray-200 p-8 mt-6">
          <h2 className="text-lg font-bold text-gray-900 mb-1">Help Center</h2>
          <p className="text-xs text-gray-400 mb-5">We're here to help</p>

          <div className="flex flex-col gap-4">

            <div className="bg-gray-50 rounded-xl p-4">
              <p className="text-sm font-medium text-gray-800 mb-2">How to use Elevora</p>
              <ol className="list-decimal list-inside text-xs text-gray-500 flex flex-col gap-1 leading-relaxed">
                <li>Upload your resume as a PDF</li>
                <li>Paste a job description in the text box</li>
                <li>Click Analyze Match to see your score</li>
                <li>Scroll down to see your Career Path Map</li>
                <li>Use Multi-JD Comparator to compare jobs</li>
                <li>Download your PDF report</li>
              </ol>
            </div>

            <div className="bg-gray-50 rounded-xl p-4">
              <p className="text-sm font-medium text-gray-800 mb-2">Common Issues</p>
              <div className="flex flex-col gap-2 text-xs text-gray-500">
                <p><b className="text-gray-700">Resume not uploading?</b> Make sure the file is a PDF under 5MB.</p>
                <p><b className="text-gray-700">Score seems too low?</b> Try pasting more complete job description text.</p>
                <p><b className="text-gray-700">Graph not showing?</b> Scroll down after clicking Analyze Match.</p>
              </div>
            </div>

            <div className="bg-blue-50 border border-blue-100 rounded-xl p-4">
              <p className="text-sm font-medium text-gray-800 mb-1">Contact & Feedback</p>
              <p className="text-xs text-gray-500 mb-3">
                Have a complaint, suggestion, or found a bug? Reach out directly:
              </p>
              <a
                href="mailto:vj3.mekhana@gmail.com?subject=Elevora Feedback"
                className="inline-block bg-blue-600 hover:bg-blue-700 text-white text-xs px-4 py-2 rounded-lg transition"
              >
                vj3.mekhana@gmail.com
              </a>
            </div>

          </div>
        </div>

        {/* Footer */}
        <div className="text-center mt-10 pb-6 border-t border-gray-200 pt-6">
          <p className="text-xs text-gray-400">© Elevora | Developed by Mekh</p>
        </div>

      </div>
    </div>
  )
}
