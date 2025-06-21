from pathlib import Path
from git import Repo
from dataclasses import dataclass
from typing import List


@dataclass
class DiffChunk:
    file_path: Path
    hunk: str      # raw unified diff hunk


class DiffReader:
    """Reads the last commit and returns a list of DiffChunks."""

    def __init__(self, repo_dir: Path):
        self.repo = Repo(repo_dir)

    def run(self) -> List[DiffChunk]:

        # Check if .git exists
        if not self.repo.git_dir.exists():
            raise FileNotFoundError("No .git directory found")

        head = self.repo.head.commit
        parent = head.parents[0] if head.parents else None
        diff = head.diff(parent, create_patch=True)

        chunks: List[DiffChunk] = []
        for diff_item in diff:
            print(f"[DiffReader] diff_item: {diff_item}")
            for hunk in diff_item.diff.decode().split("\n@@"):
                if hunk.strip():
                    file_path = None
                    if diff_item.change_type != "D":
                        if diff_item.b_path is not None:
                            file_path = Path(diff_item.b_path)
                    else:
                        if diff_item.a_path is not None:
                            file_path = Path(diff_item.a_path)
                    
                    if file_path is not None:
                        chunks.append(
                            DiffChunk(
                                file_path=file_path,
                                hunk="@@".join(["", hunk]),
                            )
                        )

        print("----- DiffReader -----")
        print(f"[DiffReader] found {len(chunks)} chunks")
        print(f"[DiffReader] chunks: {chunks}")
        return chunks
