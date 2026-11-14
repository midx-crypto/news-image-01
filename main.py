"""news-image-01 -- front page generator (round 3).

Builds the 1024x1024 front page for Friday 13 November 2026, carrying
four stories in a 2x2 grid with a headline and a subhead each:

1. NVIDIA CEO resigns -- Jensen Huang steps down and Colette Kress
   takes over as interim chief executive.
2. Microsoft 365 down worldwide -- Outlook and Teams are offline
   across 74 countries.
3. Europe joins Ukraine talks -- envoys confirm a seat at the table
   and a prisoner swap is planned.
4. Anthropic IPO oversubscribed -- the book is about six times
   covered at $70-78 a share, a roughly $61B raise.

Round 3 keeps round 1's proven 2x2 format (which scored 945936) and
swaps only its weakest story -- the unverified Iran tanker-strikes
claim -- for the Anthropic IPO, the day's second-biggest story.

The artwork itself lives in ``entry.png`` next to this script. This
program simply places an exact, byte-identical copy of it at the
output location, so every run reproduces the same file. Verified
SHA-256 of ``entry.png``:
``886cabb519f6002a7d287eb2f5bfa9f2a348e59e0243c0b034c42ffb79f8e648``.
"""

import hashlib
import os
import shutil
import sys

SOURCE_NAME = "entry.png"
OUTPUT_NAME = "entry.png"
DEFAULT_OUTPUT_DIR = "/output"


def find_source() -> str:
    """Return the path of the artwork sitting beside this script."""
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, SOURCE_NAME)


def destination() -> str:
    """Return where the finished page should be written."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or DEFAULT_OUTPUT_DIR
    return os.path.join(out_dir, OUTPUT_NAME)


def main() -> int:
    source = find_source()
    if not os.path.isfile(source):
        print(f"error: source image not found: {source}", file=sys.stderr)
        return 1

    target = destination()
    os.makedirs(os.path.dirname(target) or ".", exist_ok=True)

    shutil.copyfile(source, target)

    def _sha256(path: str) -> str:
        digest = hashlib.sha256()
        with open(path, "rb") as fh:
            for chunk in iter(lambda: fh.read(8192), b""):
                digest.update(chunk)
        return digest.hexdigest()

    if _sha256(target) != _sha256(source):
        print("error: output sha256 does not match source", file=sys.stderr)
        return 1

    print(f"wrote {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
