import os
import requests
from typing import List
from .change_critic import ReviewItem
from pathlib import Path


class ReportWriter:
    def __init__(self, repo_dir: Path, filename: str = "LastCommitReview.md"):
        self.report_path = Path(repo_dir) / filename

    def run(self, reviews: List[ReviewItem]) -> None:
        markdown = "# 🧠 AI Code Review\n\n"
        has_critical = False

        for item in reviews:
            emoji = {
                "info": "🟢",
                "warning": "🟠",
                "critical": "🔴"
            }.get(item.severity, "🟢")

            markdown += f"## {emoji} `{item.file_path}`\n\n{item.comment}\n\n"
            if item.severity == "critical":
                has_critical = True

        # Save to markdown file
        self.report_path.write_text(markdown, encoding='utf-8')
        print(f"[CodeReviewerAgent] wrote report to {self.report_path}")

        # --- GitHub Comment Logic ---
        github_token = os.getenv("GITHUB_TOKEN")
        repo_slug = os.getenv("GITHUB_REPOSITORY")
        pr_number = os.getenv("PR_NUMBER")
        commit_sha = os.getenv("GITHUB_SHA")

        if not github_token or not repo_slug:
            print("[CodeReviewerAgent] Missing GITHUB_TOKEN or GITHUB_REPOSITORY — skipping comment")
            return

        headers = {
            "Authorization": f"Bearer {github_token}",
            "Accept": "application/vnd.github+json"
        }

        comment_url = None
        context = None

        if pr_number:
            comment_url = f"https://api.github.com/repos/{repo_slug}/issues/{pr_number}/comments"
            context = f"PR #{pr_number}"
        elif commit_sha:
            comment_url = f"https://api.github.com/repos/{repo_slug}/commits/{commit_sha}/comments"
            context = f"Commit {commit_sha[:7]}"

        if comment_url:
            print(f"[CodeReviewerAgent] Posting comment to {context}...")
            response = requests.post(
                comment_url,
                json={"body": markdown},
                headers=headers
            )
            if response.status_code == 201:
                print(f"[CodeReviewerAgent] Comment successfully posted to {context}")
            else:
                print(f"[CodeReviewerAgent] Failed to comment on {context}: {response.status_code} → {response.text}")

        # Fail CI if necessary
        if has_critical:
            raise SystemExit("🚨 Code review found critical issues.")
