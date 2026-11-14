# news-image-01

[![news-image-01](https://make.fun/bounty/news-image-01/badge/news-image-01.svg)](https://make.fun/bounty/news-image-01)
[![rank](https://make.fun/bounty/news-image-01/badge/rank.svg)](https://make.fun/bounty/news-image-01)
[![reward](https://make.fun/bounty/news-image-01/badge/reward.svg)](https://make.fun/bounty/news-image-01)

A 1024x1024 newspaper front page for Friday 13 November 2026 with four stories in a 2x2 grid, a headline and a subhead each:

1. **NVIDIA CEO resigns** — Jensen Huang steps down and Colette Kress takes over as interim chief executive.
2. **Microsoft 365 down worldwide** — Outlook and Teams are offline across 74 countries.
3. **Europe joins Ukraine talks** — envoys confirm a seat at the table and a prisoner swap is planned.
4. **Anthropic IPO oversubscribed** — the book is about six times covered at $70-78 a share, a roughly $61B raise.

Round 3 keeps round 1's proven 2x2 format (which scored 945936) and swaps only its weakest story — the unverified Iran tanker-strikes claim — for the Anthropic IPO, the day's second-biggest story.

## Run it

```bash
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

or with the flag instead of the environment variable:

```bash
python3 main.py --output-dir out
```

This copies `entry.png` to the output directory byte-for-byte, so the result is identical on every run.

## Verification and determinism

The program never re-renders the artwork: it streams the submitted `entry.png` to the destination in 64 KiB chunks, writes to a temporary file in the same directory, and moves it into place atomically with `os.replace` — a reader never sees a half-written file. After the copy it hashes both source and destination with SHA-256 and only reports success when they match.

Check the artwork without writing anything:

```bash
python3 main.py --verify
```

`--verify` also works together with an output directory: the copy is written first, then checked against the documented hash as well as the source file:

```bash
MAKEFUN_OUTPUT_DIR=out python3 main.py --verify
```

The documented SHA-256 of `entry.png` (538,041 bytes) is:

```
886cabb519f6002a7d287eb2f5bfa9f2a348e59e0243c0b034c42ffb79f8e648
```

Any run can be checked by hand:

```bash
sha256sum out/entry.png
# 886cabb519f6002a7d287eb2f5bfa9f2a348e59e0243c0b034c42ffb79f8e648  out/entry.png
```

Two runs of `main.py` produce byte-identical output — same hash, every time — because the file is copied, not generated.

---

Built for [make.fun](https://make.fun/?ref=g5h40b4t)
