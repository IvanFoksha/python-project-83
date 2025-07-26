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
            return cur.fetchone()


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
