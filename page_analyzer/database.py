import os
import psycopg2
from datetime import datetime
from urllib.parse import urlparse
import validators


def get_db_connection():
    return psycopg2.connect(os.getenv('DATABASE_URL'))
