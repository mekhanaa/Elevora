from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from parser import extract_text_from_pdf
from extractor import extract_skills, calculate_match
from database import init_db, get_db
from flask import send_file
from report import generate_report
import json

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

init_db()

@app.route("/")
def home():
    return jsonify({"message": "SkillMap API running"})

@app.route("/analyze", methods=["POST"])
def analyze():
    if "resume" not in request.files:
        return jsonify({"error": "No resume uploaded"}), 400

    resume_file = request.files["resume"]
    jd_text = request.form.get("jd_text", "")

    if not jd_text.strip():
        return jsonify({"error": "Job description is empty"}), 400

    # Save resume
    file_path = os.path.join(UPLOAD_FOLDER, resume_file.filename)
    resume_file.save(file_path)

    # Extract text
    resume_text = extract_text_from_pdf(file_path)

    # Extract skills
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    # Calculate match
    result = calculate_match(resume_skills, jd_skills)

    # Save to DB
    conn = get_db()
    conn.execute(
        "INSERT INTO analyses (resume_filename, jd_text, match_score, matched_skills, missing_skills) VALUES (?, ?, ?, ?, ?)",
        (resume_file.filename, jd_text, result["score"],
         json.dumps(result["matched"]), json.dumps(result["missing"]))
    )
    conn.commit()
    conn.close()

    return jsonify({
        "match_score": result["score"],
        "matched_skills": result["matched"],
        "missing_skills": result["missing"],
        "resume_skills": list(resume_skills.keys()),
        "jd_skills": list(jd_skills.keys()),
        "resume_filename": resume_file.filename
    })

# Load careers data once at startup
with open("careers.json", "r") as f:
    CAREERS = json.load(f)

@app.route("/careers", methods=["POST"])
def match_careers():
    data = request.get_json()
    resume_skills_raw = data.get("resume_skills", [])
    resume_set = set([s.lower() for s in resume_skills_raw])

    results = []
    for career in CAREERS:
        required = career["required_skills"]

        matched = [s for s in required if s.lower() in resume_set]
        missing = [s for s in required if s.lower() not in resume_set]

        score = round((len(matched) / len(required)) * 100, 1)

        # Get learn paths for missing skills
        roadmap = []
        for skill in missing:
            if skill in career["learn_path"]:
                roadmap.append({
                    "skill": skill,
                    "path": career["learn_path"][skill]
                })

        results.append({
            "role": career["role"],
            "category": career["category"],
            "score": score,
            "matched": matched,
            "missing": missing,
            "roadmap": roadmap
        })

    # Sort by score descending
    results.sort(key=lambda x: x["score"], reverse=True)
    return jsonify(results)


@app.route("/compare", methods=["POST"])
def compare_jobs():
    data = request.get_json()
    resume_skills_raw = data.get("resume_skills", [])
    jd_list = data.get("jd_list", [])  # list of {title, text}

    if len(jd_list) < 2:
        return jsonify({"error": "Paste at least 2 job descriptions"}), 400

    resume_set = set([s.lower() for s in resume_skills_raw])
    results = []

    for jd in jd_list:
        jd_skills = extract_skills(jd["text"])
        jd_set = set([s.lower() for s in jd_skills.keys()])

        matched = [s for s in jd_skills.keys() if s.lower() in resume_set]
        missing = [s for s in jd_skills.keys() if s.lower() not in resume_set]
        score = round((len(matched) / len(jd_set)) * 100, 1) if jd_set else 0

        # ATS keyword density
        ats = []
        for skill in jd_skills.keys():
            count_in_jd = len([w for w in jd["text"].lower().split()
                               if skill.lower() in w])
            count_in_resume = data.get("resume_text_lower", "").count(skill.lower())
            ats.append({
                "skill": skill,
                "jd_count": count_in_jd,
                "resume_count": count_in_resume,
                "status": "good" if count_in_resume >= count_in_jd else
                          "low" if count_in_resume > 0 else "missing"
            })

        results.append({
            "title": jd["title"],
            "score": score,
            "matched": matched,
            "missing": missing,
            "ats": ats
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return jsonify(results)


@app.route("/report", methods=["POST"])
def download_report():
    data = request.get_json()
    buffer = generate_report(data)
    return send_file(
        buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="SkillMap_Report.pdf"
    )


if __name__ == "__main__":
    app.run(debug=True)