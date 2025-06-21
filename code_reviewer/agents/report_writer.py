# code_reviewer/agents/report_writer.py
import os
import requests
from typing import List
from .change_critic import ReviewItem
from pathlib import Path


class ReportWriter:
    def __init__(self, repo_dir: Path, filename: str = "LastCommitReview.md"):
        self.report_path = Path(repo_dir) / filename

    def run(self, reviews: List[ReviewItem]) -> None:
        markdown = "# 🧠 AI Last Commit Review\n\n"
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

        # Write report.md
        self.report_path.write_text(markdown, encoding='utf-8')
        print(f"[CodeReviewerAgent] wrote report to {self.report_path}")

        # Optional: comment on PR
        github_token = os.getenv("GITHUB_TOKEN")
        pr_number = os.getenv("PR_NUMBER")
        repo_slug = os.getenv("GITHUB_REPOSITORY")

        if github_token and pr_number and repo_slug:
            print("[CodeReviewerAgent] posting comment to PR...")
            url = f"https://api.github.com/repos/{repo_slug}/issues/{pr_number}/comments"
            response = requests.post(
                url,
                json={"body": markdown},
                headers={"Authorization": f"Bearer {github_token}"}
            )
            if response.status_code != 201:
                print(f"[CodeReviewerAgent] failed to comment on PR: {response.text}")

        # Optional: fail the run if critical issues
        if has_critical:
            raise SystemExit("🚨 Code review found critical issues.")
