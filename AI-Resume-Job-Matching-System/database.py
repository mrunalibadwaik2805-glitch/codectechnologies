import psycopg2
from config import DB_CONFIG


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def initialize_database():

    connection = get_connection()
    cursor = connection.cursor()

    with open(
        "models/database_schema.sql",
        "r",
        encoding="utf-8"
    ) as file:

        schema = file.read()

    cursor.execute(schema)

    connection.commit()

    cursor.close()
    connection.close()


def add_candidate(name, email, filename, resume_text):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO candidates
        (name, email, resume_filename, resume_text)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
    """

    cursor.execute(
        query,
        (name, email, filename, resume_text)
    )

    candidate_id = cursor.fetchone()[0]

    connection.commit()

    cursor.close()
    connection.close()

    return candidate_id


def get_candidates():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, email, resume_filename, resume_text
        FROM candidates
        ORDER BY created_at DESC;
    """)

    candidates = cursor.fetchall()

    cursor.close()
    connection.close()

    return candidates


def save_matching_result(
    candidate_id,
    job_description,
    tfidf_score,
    semantic_score,
    final_score
):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO matching_results
        (
            candidate_id,
            job_description,
            tfidf_score,
            semantic_score,
            final_score
        )
        VALUES (%s, %s, %s, %s, %s);
    """

    cursor.execute(
        query,
        (
            candidate_id,
            job_description,
            tfidf_score,
            semantic_score,
            final_score
        )
    )

    connection.commit()

    cursor.close()
    connection.close()
























