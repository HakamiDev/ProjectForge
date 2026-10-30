#!/usr/bin/env python3
"""يبني «Project Forge 1.py»: ملف واحد مكتفٍ بنفسه (بايثون وحده، والقالب مضغوط بداخله).

    python3 -I tools/build-single.py [المخرج]
"""
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))
from forge import core  # noqa: E402

out = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "dist" / core.TOOL_NAME
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(core.single_source(), encoding="utf-8")
if len(sys.argv) == 1:
    (root / core.TOOL_NAME).write_text(out.read_text(encoding="utf-8"), encoding="utf-8")
print("Built", out, out.stat().st_size, "bytes")
