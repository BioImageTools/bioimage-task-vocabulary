"""Run a SPARQL query against the generated vocabulary.

Usage: python scripts/query.py queries/next_operations.rq
"""

import sys
from pathlib import Path

from rdflib import Graph

ROOT = Path(__file__).resolve().parent.parent
TTL = ROOT / "vocabulary" / "bioimage_task_vocabulary.ttl"


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    graph = Graph().parse(TTL)
    result = graph.query(Path(sys.argv[1]).read_text())
    for row in result:
        print("\t".join("" if v is None else graph.namespace_manager.normalizeUri(v) if hasattr(v, "n3") and v.startswith("http") else str(v) for v in row))


if __name__ == "__main__":
    main()
