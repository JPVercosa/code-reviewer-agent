from pathlib import Path
from git import Repo
from dataclasses import dataclass
from typing import List, Set


@dataclass
class DiffChunk:
    file_path: Path
    hunk: str      # raw unified diff hunk


class DiffReader:
    """
    Reads the last commit and returns a list of DiffChunks,
    but only for files considered “code” (by extension).
    """

    # Adjust this set to taste
    CODE_EXTENSIONS: Set[str] = {
        ".py", ".ipynb",
        ".js", ".jsx", ".ts", ".tsx",
        ".java", ".kt", ".kts",
        ".c", ".cpp", ".cc", ".h", ".hpp",
        ".cs", ".go", ".rb", ".rs", ".swift",
        ".php", ".pl", ".sh", ".bash",
        ".dart", ".lua",
        ".html", ".css", ".scss",
        ".json", ".yaml", ".yml",
    }

    def __init__(self, repo_dir: Path):
        self.repo = Repo(repo_dir.resolve())

    @classmethod
    def _is_code_file(cls, path: Path) -> bool:
        """
        Returns True if the file’s suffix matches one of the
        configured code-type extensions.
        """
        return path.suffix.lower() in cls.CODE_EXTENSIONS

    def run(self) -> List[DiffChunk]:
        # Check if .git exists
        if not Path(self.repo.git_dir).exists():
            raise FileNotFoundError("No .git directory found")

        head = self.repo.head.commit
        parent = head.parents[0] if head.parents else None
        diff_index = head.diff(parent, create_patch=True)

        chunks: List[DiffChunk] = []

        for diff_item in diff_index:
            # Determine the relevant path depending on change type
            if diff_item.change_type == "D":
                file_path = Path(diff_item.a_path) if diff_item.a_path else None
            else:
                file_path = Path(diff_item.b_path) if diff_item.b_path else None

            # Skip anything that isn’t a recognised code file
            if file_path is None or not self._is_code_file(file_path):
                continue

            # Split unified diff output into hunks and store
            for hunk in diff_item.diff.decode().split("\n@@"):
                if hunk.strip():  # ignore empty segments
                    chunks.append(
                        DiffChunk(
                            file_path=file_path,
                            hunk="@@".join(["", hunk]),
                        )
                    )

        print("----- DiffReader -----")
        print(f"[DiffReader] found {len(chunks)} chunks")
        for c in chunks:
            print(f"[DiffReader] {c.file_path}: {len(c.hunk.splitlines())} lines")

        return chunks
