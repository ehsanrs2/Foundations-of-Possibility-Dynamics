"""Local-link checks and ten-chapter structure; not scientific validation."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "book"

def check():
    chapters = sorted(p for p in BOOK.glob("*.md") if p.name != "index.md")
    assert len(chapters) == 10, f"Expected 10 chapters, found {len(chapters)}"
    for n in range(1, 11):
        assert len([p for p in chapters if p.name.startswith(f"{n:02d}-")]) == 1
    for p in [*chapters, BOOK / "index.md"]:
        data = p.read_text(encoding="utf8")
        assert data.startswith("# ") and len(data) > 200, f"Missing chapter content: {p}"
        for link in re.findall(r"\]\(([^)]+)\)", data):
            target = link.split("#")[0]
            if not target or target.startswith(("http://","https://","mailto:")):
                continue
            assert (p.parent / target).exists(), f"Broken local link {p}: {target}"
    for path in ("research/protocol.md","research/claims.md",
                 "research/scientific-review-v0.2.md","references/references.md"):
        assert (ROOT / path).exists(), f"Missing: {path}"

if __name__ == "__main__":
    check()
    print("10 chapters and local references OK")
