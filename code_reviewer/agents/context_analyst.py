# code_reviewer/agents/context_analyst.py
from pathlib import Path
from dataclasses import dataclass
from typing import List
import re

from .diff_reader import DiffChunk

# Regex that captures the “new-file” hunk header:
#   @@ -oldStart,oldCount +newStart,newCount @@
_HUNK_HEADER = re.compile(
    r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@"
)

@dataclass
class ContextBlock:
    file_path: Path
    diff_hunk: str         # unified diff hunk (unchanged)
    full_source: str       # **trimmed** source window around the hunk


class ContextAnalyst:
    """
    Builds a ContextBlock for each DiffChunk but limits the amount of
    surrounding source code by grabbing only `context_window` lines
    before and after the changed region.
    """

    def __init__(self, repo_dir: Path, context_window: int = 50):
        """
        :param repo_dir: path to the repository root
        :param context_window: #lines of context to include before *and* after
                               the diff hunk (default: 50)
        """
        self.repo_dir = Path(repo_dir)
        self.context_window = max(0, context_window)

    # --------------------------------------------------------------------- #
    # helpers
    # --------------------------------------------------------------------- #
    def _window_from_hunk_header(self, hunk_header: str) -> tuple[int, int]:
        """
        Return (start_line, end_line) for the context window in 1-based
        line numbers.  If parsing fails, fall back to entire file.
        """
        m = _HUNK_HEADER.match(hunk_header)
        if not m:
            return (1, float("inf"))  # safety: no header parsed → no trimming

        new_start = int(m.group(1))
        new_count = int(m.group(2) or 1)

        start_line = max(1, new_start - self.context_window)
        end_line   = new_start + new_count + self.context_window - 1
        return (start_line, end_line)

    def _read_window(self, file_path: Path, start: int, end: int) -> str:
        """
        Read only the requested lines (1-based inclusive) from file_path.
        """
        if not file_path.exists():
            return ""  # file was deleted or renamed away

        lines: list[str] = []
        with file_path.open(encoding="utf-8") as f:
            for idx, line in enumerate(f, 1):
                if idx < start:
                    continue
                if idx > end:
                    break
                lines.append(line.rstrip("\n"))
        return "\n".join(lines)

    # --------------------------------------------------------------------- #
    # main
    # --------------------------------------------------------------------- #
    def run(self, chunks: List[DiffChunk]) -> List[ContextBlock]:
        blocks: list[ContextBlock] = []

        for chunk in chunks:
            # 1) Parse header to know where the diff occurs
            first_line = chunk.hunk.splitlines()[0]
            window_start, window_end = self._window_from_hunk_header(first_line)

            # 2) Read only that slice of the file
            source_path = self.repo_dir / chunk.file_path
            trimmed_source = self._read_window(source_path, window_start, window_end)

            # 3) Build block
            blocks.append(
                ContextBlock(
                    file_path=chunk.file_path,
                    diff_hunk=chunk.hunk,
                    full_source=trimmed_source,
                )
            )

        # --- logging ------------------------------------------------------ #
        print("----- ContextAnalyst -----")
        print(f"[ContextAnalyst] found {len(blocks)} blocks")
        for b in blocks:
            print(
                f"[ContextAnalyst] {b.file_path}: "
                f"{len(b.full_source.splitlines())} source lines retained"
            )
        # ------------------------------------------------------------------ #
        return blocks
