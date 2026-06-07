export default function CareerCards({ careers }) {
  if (!careers || careers.length === 0) return null

  const top4 = careers.slice(0, 4)

  return (
    <div className="flex flex-col gap-4">
      <h3 className="font-medium text-gray-800">
        Career Readiness
      </h3>
      {top4.map((career, i) => (
        <div key={i} className="bg-white border border-gray-200 rounded-xl p-4">
          <div className="flex justify-between items-center mb-2">
            <span className="font-medium text-gray-800 text-sm">{career.role}</span>
            <span className={`text-sm font-bold ${
              career.score >= 70 ? "text-green-600" :
              career.score >= 40 ? "text-yellow-500" : "text-gray-400"
            }`}>{career.score}%</span>
          </div>

          <div className="h-2 bg-gray-100 rounded-full mb-3">
            <div
              className={`h-full rounded-full ${
                career.score >= 70 ? "bg-green-500" :
                career.score >= 40 ? "bg-yellow-400" : "bg-gray-300"
              }`}
              style={{ width: `${career.score}%` }}
            />
          </div>

          {career.roadmap.length > 0 && (
            <div>
              <p className="text-xs text-gray-500 mb-1">Learn to improve:</p>
              {career.roadmap.slice(0, 2).map((item, j) => (
                <p key={j} className="text-xs text-gray-600">
                  <span className="text-red-400">● </span>
                  <span className="font-medium">{item.skill}</span>
                  {" — "}{item.path}
                </p>
              ))}
            </div>
          )}
        </div>
      ))}
    </div>
  )
}