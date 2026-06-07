export default function ScoreGauge({ score }) {
  const color =
    score >= 70 ? "text-green-600" :
    score >= 40 ? "text-yellow-500" :
    "text-red-500"

  const bar =
    score >= 70 ? "bg-green-500" :
    score >= 40 ? "bg-yellow-400" :
    "bg-red-500"

  return (
    <div className="text-center py-6">
      <p className="text-gray-500 text-sm mb-2">Match Score</p>
      <p className={`text-6xl font-bold ${color}`}>{score}%</p>
      <div className="mt-4 h-3 bg-gray-200 rounded-full overflow-hidden">
        <div
          className={`h-full ${bar} rounded-full transition-all duration-700`}
          style={{ width: `${score}%` }}
        />
      </div>
      <p className="text-xs text-gray-400 mt-2">
        {score >= 70 ? "Strong match" : score >= 40 ? "Partial match" : "Weak match"}
      </p>
    </div>
  )
}