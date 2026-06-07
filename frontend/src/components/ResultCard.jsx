import ScoreGauge from "./ScoreGauge"
import SkillTags from "./SkillTags"

export default function ResultCard({ result }) {
  return (
    <div className="flex flex-col gap-6">
      <ScoreGauge score={result.match_score} />

      <div className="bg-white border border-gray-200 rounded-xl p-5">
        <h3 className="font-medium text-gray-800 mb-3">
          ✅ Matched Skills ({result.matched_skills.length})
        </h3>
        <SkillTags skills={result.matched_skills} type="matched" />
      </div>

      <div className="bg-white border border-gray-200 rounded-xl p-5">
        <h3 className="font-medium text-gray-800 mb-3">
          ❌ Missing Skills ({result.missing_skills.length})
        </h3>
        <SkillTags skills={result.missing_skills} type="missing" />
      </div>

      <div className="bg-white border border-gray-200 rounded-xl p-5">
        <h3 className="font-medium text-gray-800 mb-3">
          📄 All Skills in Your Resume
        </h3>
        <SkillTags skills={result.resume_skills} type="neutral" />
      </div>
    </div>
  )
}