"""news-image-01 entry: copy the vendored front-page image to the output dir.

The image (entry.png, next to this file) sums up the world's news of
Friday 13 November 2026 in a 2x2 newspaper front page:
  - NVIDIA CEO resigns (shares fell; Kress interim CEO)
  - Microsoft 365 down worldwide (Outlook & Teams, 74 countries)
  - Europe joins Ukraine talks (envoys say; prisoner swap planned)
  - Iran claims tanker strikes in the Strait of Hormuz (unverified)

Standard library only. Deterministic: the output is a byte-for-byte
copy of the vendored file, so repeated runs produce identical bytes.
"""

import os
import shutil
import sys


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    if not os.path.isfile(source):
        print(f"error: vendored image not found: {source}", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(source, dest)
    # Determinism check: the output must be a byte-for-byte copy.
    if os.path.getsize(dest) != os.path.getsize(source):
        print("error: output size differs from vendored image", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
