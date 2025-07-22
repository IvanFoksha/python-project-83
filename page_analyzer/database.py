import os
import psycopg2
from datetime import datetime
from urllib.parse import urlparse
import validators


def get_db_connection():
    return psycopg2.connect(os.getenv('DATABASE_URL'))


def add_url(url):
    parser = urlparse(url)
    normalized_url = f'{parser.scheme}://{parser.netloc}'

    if not validators.url(normalized_url):
        return None, 'Некоректный URL'
    if len(normalized_url) > 255:
        return None, 'URL превышает 255 символов'
    
    with get_db_connection as conn:
        with conn.cursor() as cur:
            cur.execute(
                'SELECT id FROM urls WHERE name = %s',
                (normalized_url,)
            )
            existing = cur.fetchone()
            if existing:
                return existing[0], None

            cur.execute(
                """
                INSERT INTO urls (name, created_at)
                VALUES (%s, %s)
                RETURING id
                """,
                (normalized_url, datetime.now())
            )
            url_id = cur.fetchone()[0]
            conn.commit()
            return url_id, None
        

