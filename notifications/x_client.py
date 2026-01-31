"""
Integration client for X (Twitter) platform.
Handles the API interactions required to post news updates to social media.
"""
import requests


def post_to_x(message):
    """
    Send a post to X (Twitter) platform when a new article is published.
    """

    url = "https://api.x.com/2/tweets"  # placeholder URL

    payload = {
        "text": message[:280]
    }

    headers = {
        "Authorization": "Bearer YOUR_API_TOKEN_HERE"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        return response.status_code in (200, 201)
    except Exception:
        return False
