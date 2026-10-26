#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python scripts/check_book.py
command -v pandoc >/dev/null || { echo "Install Pandoc" >&2; exit 2; }
mkdir -p dist
set -- book/01-scope.md book/02-prior-work.md book/03-formal-foundations.md \
 book/04-measures.md book/05-toy-case.md book/06-experimental-design.md \
 book/07-validity-threats.md book/08-research-agenda.md \
 book/09-interpretation.md book/10-conclusion.md \
 research/claims.md research/protocol.md references/references.md
pandoc -f markdown+tex_math_dollars -s --toc \
 --metadata=title:"Foundations of Possibility Dynamics" \
 --metadata=subtitle:"Working scientific monograph v0.2" \
 --mathjax -t html5 -o dist/Foundations-of-Possibility-Dynamics.html "$@"
pandoc -f markdown+tex_math_dollars -s --toc \
 --metadata=title:"Foundations of Possibility Dynamics" \
 --metadata=subtitle:"Working scientific monograph v0.2" \
 -t epub3 -o dist/Foundations-of-Possibility-Dynamics.epub "$@"
echo "Built dist HTML and EPUB"
