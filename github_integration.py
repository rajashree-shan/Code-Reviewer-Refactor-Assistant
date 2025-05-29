import requests
from rag_pipeline import generate_review

GITHUB_API_BASE = "https://api.github.com"

def get_headers(token):
    return {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

def review_pull_request(repo: str, pr_number: int, token: str) -> dict:
    """
    Returns a dict of {filename: review_comments} for Python files in the PR.
    """
    url = f"{GITHUB_API_BASE}/repos/{repo}/pulls/{pr_number}/files"
    response = requests.get(url, headers=get_headers(token))
    response.raise_for_status()

    files = response.json()
    reviews = {}

    for file in files:
        filename = file["filename"]
        if filename.endswith(".py"):
            raw_url = file["raw_url"]
            raw_code = requests.get(raw_url, headers=get_headers(token)).text
            review = generate_review(raw_code)
            reviews[filename] = review

    return reviews

def post_pr_comment(repo: str, pr_number: int, comments: dict, token: str):
    """
    Posts a single comment summarizing the review per file.
    """
    if not comments:
        return

    comment_body = "### 🤖 AI Code Review Summary\n\n"
    for filename, review in comments.items():
        comment_body += f"**File:** `{filename}`\n```\n{review}\n```\n\n"

    url = f"{GITHUB_API_BASE}/repos/{repo}/issues/{pr_number}/comments"
    response = requests.post(url, json={"body": comment_body}, headers=get_headers(token))
    response.raise_for_status()
