import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Skills that the system will check
SKILLS = [
    "python",
    "django",
    "flask",
    "html",
    "css",
    "javascript",
    "react",
    "react.js",
    "sql",
    "rest api",
    "rest apis",
    "git",
    "github",
    "machine learning",
    "ml",
    "nlp",
    "numpy",
    "pandas",
    "scikit-learn",
    "tensorflow",
    "bootstrap",
    "database",
]


def clean_text(text):
    """Clean text before matching."""
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def get_skills(text):
    """Find skills present in text."""
    text = clean_text(text)

    found = []

    for skill in SKILLS:
        if skill in text:
            found.append(skill)

    return sorted(set(found))


def calculate_match(resume_text, job_description):
    """
    Calculate TF-IDF, semantic/keyword similarity,
    matched skills and missing skills.
    """

    resume_text = clean_text(resume_text)
    job_description = clean_text(job_description)

    # -----------------------------
    # TF-IDF SCORE
    # -----------------------------
    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    vectors = vectorizer.fit_transform(
        [resume_text, job_description]
    )

    tfidf_score = cosine_similarity(
        vectors[0:1],
        vectors[1:2]
    )[0][0] * 100

    # -----------------------------
    # SKILL MATCHING
    # -----------------------------
    resume_skills = set(get_skills(resume_text))
    job_skills = set(get_skills(job_description))

    matched_skills = sorted(
        resume_skills.intersection(job_skills)
    )

    missing_skills = sorted(
        job_skills - resume_skills
    )

    if job_skills:
        skill_score = (
            len(matched_skills) /
            len(job_skills)
        ) * 100
    else:
        skill_score = 0

    # -----------------------------
    # FINAL SCORE
    # -----------------------------
    final_score = (
        (tfidf_score * 0.40) +
        (skill_score * 0.60)
    )

    # -----------------------------
    # MATCH LEVEL
    # -----------------------------
    if final_score >= 75:
        match_level = "Strong Match 🟢"
    elif final_score >= 50:
        match_level = "Moderate Match 🟡"
    else:
        match_level = "Low Match 🔴"

    return {
        "tfidf_score": round(float(tfidf_score), 2),
        "semantic_score": round(float(skill_score), 2),
        "final_score": round(float(final_score), 2),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "match_level": match_level
    }




























