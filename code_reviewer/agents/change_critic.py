import json
from typing import List
from dataclasses import dataclass

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from .context_analyst import ContextBlock
from ..llm_interface import get_llm


@dataclass
class ReviewItem:
    file_path: str
    comment: str
    severity: str  # info | warning | critical


class ChangeCritic:
    """
    Sends <diff + full source> to an LLM, expects JSON with 'comment' & 'severity'.
    Falls back gracefully if the model returns plain text.
    """

    def __init__(self):
        self.llm = get_llm()
        self.parser = StrOutputParser()
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    (
                        "You are a senior software engineer doing code review.\n"
                        "Return *JSON ONLY* with keys 'comment' (string) and 'severity' "
                        "(one of: info, warning, critical)."
                    ),
                ),
                (
                    "human",
                    (
                        "FILE: {file_path}\n"
                        "DIFF:\n{diff}\n"
                        "FULL_CONTEXT:\n{context}\n\n"
                        "Respond now."
                    ),
                ),
            ]
        )

    def run(self, blocks: List[ContextBlock]) -> List[ReviewItem]:
        reviews: List[ReviewItem] = []

        for blk in blocks:
            chain = self.prompt | self.llm | self.parser
            raw = chain.invoke(
                {
                    "file_path": str(blk.file_path),
                    "diff": blk.diff_hunk,
                    "context": blk.full_source,
                }
            )

            # Try to parse the JSON; if it fails, treat output as 'info'
            try:
                if "<think>" in raw:
                    raw = raw.split("</think>")[1]
                data = json.loads(raw)
                comment = data.get("comment", "").strip() or raw
                severity = data.get("severity", "info").lower()
                if severity not in {"info", "warning", "critical"}:
                    severity = "info"
            except json.JSONDecodeError:
                comment, severity = raw, "info"

            reviews.append(
                ReviewItem(
                    file_path=str(blk.file_path),
                    comment=comment,
                    severity=severity,
                )
            )

        print("----- ChangeCritic -----")
        print(f"[ChangeCritic] found {len(reviews)} reviews")
        print(f"[ChangeCritic] reviews: {reviews}")

        return reviews
