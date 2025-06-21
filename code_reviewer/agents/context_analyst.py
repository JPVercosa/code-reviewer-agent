# code_reviewer/agents/context_analyst.py
from pathlib import Path
from dataclasses import dataclass
from typing import List

from .diff_reader import DiffChunk

@dataclass
class ContextBlock:
    file_path: Path
    diff_hunk: str
    full_source: str            # raw file contents

class ContextAnalyst:
    def __init__(self, repo_dir: Path):
        self.repo_dir = Path(repo_dir)

    def run(self, chunks: List[DiffChunk]) -> List[ContextBlock]:
        blocks = []
        for chunk in chunks:
            source_path = self.repo_dir / chunk.file_path
            full_source = source_path.read_text(encoding="utf-8") if source_path.exists() else ""
            blocks.append(ContextBlock(chunk.file_path, chunk.hunk, full_source))

        print("----- ContextAnalyst -----")
        print(f"[ContextAnalyst] found {len(blocks)} blocks")
        print(f"[ContextAnalyst] blocks: {blocks}")
        return blocks
