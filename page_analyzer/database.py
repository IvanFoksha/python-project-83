import os
import psycopg2
from datetime import datetime


def get_db_connection():
    return psycopg2.connect(os.getenv('DATABASE_URL'))


def add_url(url):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                'SELECT id FROM urls WHERE name = %s',
                (url,)
            )
            existing = cur.fetchone()
            if existing:
                return existing[0], None

            cur.execute(
                """
                    INSERT INTO urls (name, created_at)
                    VALUES (%s, %s)
                    RETURNING id
                """,
                (url, datetime.now())
            )
            url_id = cur.fetchone()[0]
            conn.commit()
            return url_id, None


def get_url_by_id(url_id):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                    SELECT id, name, created_at FROM urls
                    WHERE id = %s
                """,
                (url_id,)
            )
            result = cur.fetchone()
            if result:
                url_id, name, created_at = result
                cur.execute(
                    """
                        SELECT
                            id, status_code, h1, title, description, created_at
                        FROM checks WHERE url_id = %s
                    """,
                    (url_id,)
                )
                checks = [{
                    'id': row[0],
                    'status_code': row[1],
                    'h1': row[2],
                    'title': row[3],
                    'description': row[4],
                    'created_at': row[5]} for row
                    in cur.fetchall()]
                return {
                    'id': url_id,
                    'name': name,
                    'created_at': created_at,
                    'checks': checks
                }
            return None


def get_all_urls():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                    SELECT id, name, created_at FROM urls
                    ORDER BY created_at DESC
                """
            )
            return cur.fetchall()


def add_check(url_id, status_code, h1, title, description):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                        INSERT INTO checks (url_id, status_code, h1, title
                        description, created_at)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (url_id, status_code, h1,
                     title, description, datetime.now())
                )
                conn.commit()
    except psycopg2.Error:
        raise
