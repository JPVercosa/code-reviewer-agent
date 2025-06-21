from typing import List
from .agents.change_critic import ChangeCritic, ReviewItem
from .agents.context_analyst import ContextAnalyst
from .agents.diff_reader import DiffReader
from .agents.report_writer import ReportWriter

from pathlib import Path

def run_pipeline(repo_dir: str | Path) -> None:
    repo_dir = Path(repo_dir)

    chunks = DiffReader(repo_dir).run()
    blocks = ContextAnalyst(repo_dir).run(chunks)
    reviews: List[ReviewItem] = ChangeCritic().run(blocks)
    ReportWriter(repo_dir).run(reviews)
