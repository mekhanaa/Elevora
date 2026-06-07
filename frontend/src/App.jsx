import { useState } from "react"
import axios from "axios"
import UploadForm from "./components/UploadForm"
import ResultCard from "./components/ResultCard"
import CareerGraph from "./components/CareerGraph"
import CareerCards from "./components/CareerCards"
import MultiJD from "./components/MultiJD"
import DownloadReport from "./components/DownloadReport"

export default function App() {
  const [result, setResult] = useState(null)
  const [careers, setCareers] = useState([])

  const handleResult = async (data) => {
    setResult(data)
    const res = await axios.post("http://localhost:5000/careers", {
      resume_skills: data.resume_skills
    })
    setCareers(res.data)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-2xl mx-auto px-4 py-10">

        <div className="text-center mb-10">
          <h1 className="text-3xl font-bold text-gray-900">SkillMap</h1>
          <p className="text-gray-500 mt-2 text-sm">
            Resume intelligence & career path engine
          </p>
        </div>

        <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6 mb-6">
          <UploadForm onResult={handleResult} />
        </div>

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
                {careers.length > 0 && (
                  <DownloadReport result={result} careers={careers} />
                  )}
                <MultiJD resumeSkills={result.resume_skills} />
              </>
            )}
          </>
        )}

      </div>
<div className="text-center mt-12 pb-6 border-t border-gray-200 pt-6">
  <p className="text-xs text-gray-400">© SkillMap | Developed by Mekh</p>
</div>
    </div>
  )
}