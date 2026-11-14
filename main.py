"""news-image-01 -- front page generator (round 2).

Builds the 1024x1024 front page for Friday 13 November 2026, carrying
six stories:

1. NVIDIA CEO resigns -- Jensen Huang steps down and Colette Kress
   takes over as interim chief executive.
2. Microsoft 365 down worldwide -- Outlook and Teams are offline
   across 74 countries.
3. Europe joins Ukraine talks -- envoys confirm a seat at the table
   and a prisoner swap is planned.
4. Iran claims tanker strikes in the Strait of Hormuz -- the claim
   is unverified.
5. Anthropic IPO oversubscribed on its first day of book building.
6. Tesla cuts the Cybertruck line to a single model, the Cyberbeast.

The artwork itself lives in ``entry.png`` next to this script. This
program simply places an exact, byte-identical copy of it at the
output location, so every run reproduces the same file. Verified
SHA-256 of ``entry.png``:
``becf46fd5c55df8d199b363b0441895ec622edddaedb0ecdce8c8f2af7fa1e04``.
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
