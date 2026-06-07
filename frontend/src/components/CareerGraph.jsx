import { useEffect, useRef } from "react"
import * as d3 from "d3"

export default function CareerGraph({ resumeSkills, careers }) {
  const svgRef = useRef()

  useEffect(() => {
    if (!careers || careers.length === 0) return

    const width = 600
    const height = 420
    const cx = width / 2
    const cy = height / 2

    d3.select(svgRef.current).selectAll("*").remove()

    const svg = d3.select(svgRef.current)
      .attr("viewBox", `0 0 ${width} ${height}`)
      .attr("width", "100%")

    // Center node — YOU
    const centerNode = { id: "You", x: cx, y: cy, type: "center" }

    // Career nodes in a circle
    const top5 = careers.slice(0, 6)
    const angleStep = (2 * Math.PI) / top5.length
    const radius = 160

    const careerNodes = top5.map((c, i) => ({
      id: c.role,
      x: cx + radius * Math.cos(i * angleStep - Math.PI / 2),
      y: cy + radius * Math.sin(i * angleStep - Math.PI / 2),
      score: c.score,
      type: "career"
    }))

    // Draw edges
    careerNodes.forEach(node => {
      svg.append("line")
        .attr("x1", centerNode.x).attr("y1", centerNode.y)
        .attr("x2", node.x).attr("y2", node.y)
        .attr("stroke", node.score >= 70 ? "#22c55e" : node.score >= 40 ? "#f59e0b" : "#e5e7eb")
        .attr("stroke-width", Math.max(1, node.score / 25))
        .attr("opacity", 0.6)
    })

    // Draw career nodes
    careerNodes.forEach(node => {
      const color = node.score >= 70 ? "#22c55e" : node.score >= 40 ? "#f59e0b" : "#94a3b8"
      const g = svg.append("g")
        .style("cursor", "pointer")

      g.append("circle")
        .attr("cx", node.x).attr("cy", node.y)
        .attr("r", 38)
        .attr("fill", color)
        .attr("opacity", 0.15)

      g.append("circle")
        .attr("cx", node.x).attr("cy", node.y)
        .attr("r", 28)
        .attr("fill", color)
        .attr("opacity", 0.9)

      g.append("text")
        .attr("x", node.x).attr("y", node.y - 4)
        .attr("text-anchor", "middle")
        .attr("fill", "white")
        .attr("font-size", "11px")
        .attr("font-weight", "600")
        .text(node.score + "%")

      g.append("text")
        .attr("x", node.x).attr("y", node.y + 50)
        .attr("text-anchor", "middle")
        .attr("fill", "#374151")
        .attr("font-size", "10px")
        .attr("font-weight", "500")
        .text(node.id)
    })

    // Draw center node
    svg.append("circle")
      .attr("cx", cx).attr("cy", cy)
      .attr("r", 36)
      .attr("fill", "#3b82f6")

    svg.append("text")
      .attr("x", cx).attr("y", cy + 5)
      .attr("text-anchor", "middle")
      .attr("fill", "white")
      .attr("font-size", "13px")
      .attr("font-weight", "700")
      .text("You")

  }, [careers, resumeSkills])

  return (
    <div className="bg-white border border-gray-200 rounded-xl p-5">
      <h3 className="font-medium text-gray-800 mb-4">
        Career Path Map
      </h3>
      <svg ref={svgRef} />
      <div className="flex gap-4 mt-3 text-xs text-gray-500">
        <span><span className="text-green-500">●</span> 70%+ Strong</span>
        <span><span className="text-yellow-500">●</span> 40–70% Partial</span>
        <span><span className="text-gray-400">●</span> Below 40%</span>
      </div>
    </div>
  )
}