from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename

from matcher import calculate_match

app = Flask(__name__)

RESUME_FOLDER = "resumes"
os.makedirs(RESUME_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


# =========================
# UPLOAD RESUME
# =========================
@app.route("/upload", methods=["POST"])
def upload_resume():

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()

    if "resume" not in request.files:
        return render_template(
            "index.html",
            error="Please select a resume."
        )

    resume = request.files["resume"]

    if resume.filename == "":
        return render_template(
            "index.html",
            error="Please select a resume."
        )

    filename = secure_filename(resume.filename)

    # Only TXT files for now
    if not filename.lower().endswith(".txt"):
        return render_template(
            "index.html",
            error="Please upload a .txt resume file."
        )

    # Save candidate information in filename
    # Example: Mrunali_Prakash_Badwaik__resume.txt
    safe_name = secure_filename(name.replace(" ", "_"))

    saved_filename = f"{safe_name}__{filename}"

    file_path = os.path.join(
        RESUME_FOLDER,
        saved_filename
    )

    resume.save(file_path)

    return render_template(
        "index.html",
        success="Resume uploaded successfully!"
    )


# =========================
# MATCH RESUMES
# =========================
@app.route("/match", methods=["POST"])
def match_resume():

    job_description = request.form.get(
        "job_description", ""
    ).strip()

    if not job_description:
        return render_template(
            "index.html",
            error="Please enter a job description."
        )

    results = []

    for filename in os.listdir(RESUME_FOLDER):

        file_path = os.path.join(
            RESUME_FOLDER,
            filename
        )

        # Currently process TXT resumes
        if filename.lower().endswith(".txt"):

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:

                resume_text = file.read()

            # Calculate matching
            match_data = calculate_match(
                resume_text,
                job_description
            )

            results.append({
                "name": "Uploaded Candidate",
                "email": "Uploaded Candidate",
                "filename": filename,

                "tfidf_score":
                    match_data["tfidf_score"],

                "semantic_score":
                    match_data["semantic_score"],

                "final_score":
                    match_data["final_score"],

                "matched_skills":
                    match_data["matched_skills"],

                "missing_skills":
                    match_data["missing_skills"],

                "match_level":
                    match_data["match_level"]
            })

    # Highest score first
    results.sort(
        key=lambda x: x["final_score"],
        reverse=True
    )

    return render_template(
        "results.html",
        results=results,
        job_description=job_description
    )


if __name__ == "__main__":
    app.run(debug=True)



















































