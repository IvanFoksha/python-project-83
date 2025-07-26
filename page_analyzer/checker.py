import re
import requests


class CheckError(Exception):
    pass


def check_url(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        status_code = response.status_code
        html_content = response.text

        h1_match = re.search(
            r'<h1[^>]*>(.*?)</h1>',
            html_content,
            re.DOTALL | re.IGNORECASE
        )
        h1 = h1_match.group(1).strip() if h1_match else ''

        title_match = re.search(
            r'<title[^>]*>(.*?)</title>',
            html_content,
            re.DOTALL | re.IGNORECASE
        )
        title = title_match.group(1).strip() if title_match else ''

        description_match = re.search(
            r'''
            <meta[^>]*name=[\"']description[\"'][^>]
            *content=[\"'](.*?)[\"']''',
            html_content,
            re.IGNORECASE
        )
        description = description_match.group(1) if description_match else ''

        return status_code, h1, title, description
    except requests.RequestException:
        raise CheckError
