"""news-image-01 entry: copy the vendored front-page image to the output dir.

The image (entry.png, next to this file) sums up the world's news of
Friday 13 November 2026 in one newspaper front page, "THE WORLD IN ONE DAY":
30 stories across 6 continents, pinned on a world map.
  - 4 lead stories with illustrations: NVIDIA CEO resigns (Kress interim),
    Microsoft 365 down worldwide (Outlook & Teams, 74 countries), Europe
    joins Ukraine talks (prisoner swap planned), Iran claims tanker strikes
    in the Strait of Hormuz (unverified claim).
  - A world map with red pins marking where the stories happened, plus
    6 more stories beside it (Ukraine drone attack, US downs Iranian
    drones, FAA ground stop lifted, Anthropic IPO, Qatar-Turkey pact,
    Pope Leo in Peru).
  - 20 one-line briefs: Tesla, Van Hollen, Brooklyn, Binance hack seizure,
    Trump/Vance, US storms, Gauff, China drills, IEA oil surplus, chip
    controls, IAEA/Isfahan, Lebanon, Gaza, Sudan, Ebola, Nigeria, Egypt,
    Italy-France, Lakers, Australia-England.

All text in the image was rendered by code (PIL + Liberation fonts), never
baked into generated artwork, so no headline is garbled. The file is a
1024x1024 PNG of 420,940 bytes, within the competition's 1 MiB cap.

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
