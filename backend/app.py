from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import json

from parser import extract_text_from_pdf
from skill_engine.engine import analyze_resume
from database import init_db, get_db
from report import generate_report


app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

init_db()

@app.route("/")
def home():
    return jsonify({
        "message": "Elevora API running"
    })

@app.route("/analyze", methods=["POST"])
def analyze():

    # Check resume
    if "resume" not in request.files:
        return jsonify({
            "error": "No resume uploaded"
        }), 400

    resume_file = request.files["resume"]

    # Get job description
    jd_text = request.form.get("jd_text", "")

    if not jd_text.strip():
        return jsonify({
            "error": "Job description is empty"
        }), 400

    file_path = os.path.join(
        UPLOAD_FOLDER,
        resume_file.filename
    )

    resume_file.save(file_path)

    resume_text = extract_text_from_pdf(file_path)

    result = analyze_resume(
        resume_text,
        jd_text
    )

    matched = result["matched_skills"]
    missing = result["missing_skills"]

    total_jd_skills = len(
        result["jd_skills"]
    )

    score = (
        round(
            (len(matched) / total_jd_skills) * 100,
            1
        )
        if total_jd_skills
        else 0
    )

    conn = get_db()

    conn.execute(
        """
        INSERT INTO analyses
        (
            resume_filename,
            jd_text,
            match_score,
            matched_skills,
            missing_skills
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            resume_file.filename,
            jd_text,
            score,
            json.dumps(matched),
            json.dumps(missing)
        )
    )

    conn.commit()
    conn.close()

    return jsonify({

        "match_score": score,

        "matched_skills": matched,

        "missing_skills": missing,

        "resume_skills": result[
            "resume_skills"
        ],

        "jd_skills": result[
            "jd_skills"
        ],

        "experience": result[
            "experience"
        ],

        "education": result[
            "education"
        ],

        "metadata": result[
            "metadata"
        ],

        "resume_filename":
            resume_file.filename,

        "resume_text":
            resume_text
    })

with open("careers.json", "r") as f:
    CAREERS = json.load(f)


@app.route("/careers", methods=["POST"])
def match_careers():

    data = request.get_json()

    resume_skills_raw = data.get(
        "resume_skills",
        []
    )

    resume_set = set(
    (
        s["skill"]
        if isinstance(s, dict)
        else s
    ).lower()
    for s in resume_skills_raw
)

    results = []

    for career in CAREERS:

        required = career[
            "required_skills"
        ]

        matched = [
            s
            for s in required
            if s.lower() in resume_set
        ]

        missing = [
            s
            for s in required
            if s.lower() not in resume_set
        ]

        score = (
            round(
                (len(matched) / len(required)) * 100,
                1
            )
            if required
            else 0
        )

        roadmap = []

        for skill in missing:

            if skill in career["learn_path"]:

                roadmap.append({
                    "skill": skill,
                    "path": career[
                        "learn_path"
                    ][skill]
                })

        results.append({

            "role":
                career["role"],

            "category":
                career["category"],

            "score":
                score,

            "matched":
                matched,

            "missing":
                missing,

            "roadmap":
                roadmap
        })

    # Highest score first
    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return jsonify(results)


@app.route("/compare", methods=["POST"])
def compare_jobs():

    data = request.get_json()

    resume_skills_raw = data.get(
        "resume_skills",
        []
    )

    jd_list = data.get(
        "jd_list",
        []
    )

    if len(jd_list) < 2:

        return jsonify({
            "error":
                "Paste at least 2 job descriptions"
        }), 400

    resume_set = set(
    (
        s["skill"]
        if isinstance(s, dict)
        else s
    ).lower()
    for s in resume_skills_raw
)

    results = []

    for jd in jd_list:

        # Extract JD skills using
        # the new skill engine
        jd_result = analyze_resume(
            "",
            jd["text"]
        )

        jd_skills = jd_result[
            "jd_skills"
        ]

        jd_skill_names = [
            item["skill"]
            for item in jd_skills
        ]

        jd_set = set(
            s.lower()
            for s in jd_skill_names
        )

        matched = [
            s
            for s in jd_skill_names
            if s.lower() in resume_set
        ]

        missing = [
            s
            for s in jd_skill_names
            if s.lower() not in resume_set
        ]

        score = (
            round(
                (len(matched) / len(jd_set)) * 100,
                1
            )
            if jd_set
            else 0
        )

        # ----------------------------------
        # ATS keyword density
        # ----------------------------------

        ats = []

        resume_text_lower = data.get(
            "resume_text_lower",
            ""
        )

        for skill in jd_skill_names:

            count_in_jd = len([
                w
                for w in jd["text"]
                .lower()
                .split()
                if skill.lower() in w
            ])

            count_in_resume = (
                resume_text_lower.count(
                    skill.lower()
                )
            )

            if count_in_resume >= count_in_jd:
                status = "good"

            elif count_in_resume > 0:
                status = "low"

            else:
                status = "missing"

            ats.append({

                "skill":
                    skill,

                "jd_count":
                    count_in_jd,

                "resume_count":
                    count_in_resume,

                "status":
                    status
            })

        results.append({

            "title":
                jd["title"],

            "score":
                score,

            "matched":
                matched,

            "missing":
                missing,

            "ats":
                ats
        })

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return jsonify(results)

@app.route("/report", methods=["POST"])
def download_report():

    data = request.get_json()

    buffer = generate_report(data)

    return send_file(

        buffer,

        mimetype="application/pdf",

        as_attachment=True,

        download_name="Elevora_Report.pdf"
    )

if __name__ == "__main__":

    app.run(
        debug=True
    )