export default function SkillTags({ skills, type }) {
  const styles = {
    matched: "bg-green-100 text-green-800 border border-green-200",
    missing: "bg-red-100 text-red-800 border border-red-200",
    neutral: "bg-gray-100 text-gray-700 border border-gray-200"
  }

  return (
    <div className="flex flex-wrap gap-2">
      {skills.length === 0 ? (
        <p className="text-gray-400 text-sm">None found</p>
      ) : (
        skills.map((skill, i) => (
          <span
            key={i}
            className={`text-xs px-3 py-1 rounded-full font-medium ${styles[type]}`}
          >
            {typeof skill === "object" ? skill.skill : skill}
          </span>
        ))
      )}
    </div>
  )
}