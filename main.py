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

How the output is produced
---------------------------
The artwork itself lives in ``entry.png`` next to this script. This
program does not re-render anything: it places an exact,
byte-identical copy of that file at the output location, so every run
reproduces the same file. The copy is written in 64 KiB chunks to a
temporary file in the same directory and then moved into place with
``os.replace``, so a crash or a full disk can never leave a truncated
``entry.png`` behind at the destination -- the destination is either
the old file or the complete new one, never a half-written file.

After the copy the program hashes both the source and the destination
with SHA-256 and refuses to report success unless they match. The
documented hash of ``entry.png`` is also checked in ``--verify``
mode, which answers the question "is the file I have the exact
artwork that was submitted?" without writing anything.

Verified SHA-256 of ``entry.png``:
``886cabb519f6002a7d287eb2f5bfa9f2a348e59e0243c0b034c42ffb79f8e648``.

Usage
-----
::

    # Normal run: write entry.png to the output directory.
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

    # Verify the artwork in place, without writing anything:
    python3 main.py --verify

    # Both flags combine: write, then verify against the documented
    # hash as well as against the source file:
    MAKEFUN_OUTPUT_DIR=out python3 main.py --verify

Environment
-----------
``MAKEFUN_OUTPUT_DIR``
    Directory the finished page is written to. Defaults to
    ``/output``. The directory is created if it does not exist.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import sys
import tempfile

SOURCE_NAME = "entry.png"
OUTPUT_NAME = "entry.png"
DEFAULT_OUTPUT_DIR = "/output"
CHUNK_SIZE = 65536  # 64 KiB per read/write step.

# SHA-256 of the submitted artwork, measured at submission time.
# Every copy this program makes must hash to this value.
EXPECTED_SHA256 = (
    "886cabb519f6002a7d287eb2f5bfa9f2a348e59e0243c0b034c42ffb79f8e648"
)

# Error messages are kept in one place so callers can match on them.
ERR_SOURCE_MISSING = "source image not found"
ERR_HASH_MISMATCH = "output sha256 does not match source"
ERR_DOCUMENTED_HASH_MISMATCH = "hash does not match the documented sha256"
ERR_COPY_FAILED = "copy failed"


def source_path() -> str:
    """Return the absolute path of the artwork sitting beside this script.

    The script always works from its own directory rather than the
    caller's working directory, so it can be invoked from anywhere.
    """
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, SOURCE_NAME)


def output_path(explicit_dir: str | None = None) -> str:
    """Return where the finished page should be written.

    Precedence: an explicit ``--output-dir`` flag wins, then the
    ``MAKEFUN_OUTPUT_DIR`` environment variable, then the default.
    An empty value at any level falls through to the next one, so
    ``MAKEFUN_OUTPUT_DIR=`` is harmless.
    """
    out_dir = explicit_dir or os.environ.get("MAKEFUN_OUTPUT_DIR") or DEFAULT_OUTPUT_DIR
    return os.path.join(out_dir, OUTPUT_NAME)


def sha256_file(path: str) -> str:
    """Return the hex SHA-256 digest of the file at ``path``.

    The file is streamed in ``CHUNK_SIZE`` blocks so even a large
    image never has to sit in memory in one piece.
    """
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            chunk = fh.read(CHUNK_SIZE)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def verify_hash(path: str, expected: str) -> bool:
    """Check whether the file at ``path`` hashes to ``expected``.

    Returns ``True`` on a match and ``False`` otherwise; the caller
    decides what to report. Raises ``OSError`` if the file cannot be
    read, which is a different failure from a hash mismatch and is
    reported as such by the caller.
    """
    return sha256_file(path) == expected


def copy_image(source: str, target: str) -> None:
    """Copy ``source`` to ``target`` in chunks, atomically.

    The bytes are streamed to a temporary file created in the target
    directory (so the final rename never crosses filesystems) and
    then moved into place with ``os.replace``, which is atomic on
    POSIX: a reader of ``target`` sees either the old file or the
    complete new one, never a partial write. The temporary file is
    removed if anything goes wrong mid-copy.

    Raises
    ------
    FileNotFoundError
        If ``source`` does not exist.
    OSError
        If the target directory cannot be created, the temporary
        file cannot be written, or the rename fails.
    """
    target_dir = os.path.dirname(target) or "."
    os.makedirs(target_dir, exist_ok=True)

    tmp_fd, tmp_path = tempfile.mkstemp(
        prefix=".entry-", suffix=".tmp", dir=target_dir
    )
    try:
        with os.fdopen(tmp_fd, "wb") as out_fh, open(source, "rb") as in_fh:
            while True:
                chunk = in_fh.read(CHUNK_SIZE)
                if not chunk:
                    break
                out_fh.write(chunk)
            out_fh.flush()
            os.fsync(out_fh.fileno())
        os.replace(tmp_path, target)
    except BaseException:
        # Any failure -- a missing source, a full disk, a signal --
        # must not leave a stray temporary file behind.
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse the command-line flags for this program."""
    parser = argparse.ArgumentParser(
        description=(
            "Place a byte-identical copy of the news-image-01 front "
            "page at the output location."
        )
    )
    parser.add_argument(
        "--output-dir",
        metavar="DIR",
        default=None,
        help=(
            "directory to write entry.png to; overrides "
            "MAKEFUN_OUTPUT_DIR and the default /output"
        ),
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help=(
            "also check the artwork against the documented SHA-256 "
            "(%s...); in verify-only use, no output file is written" % EXPECTED_SHA256[:16]
        ),
    )
    return parser.parse_args(argv)


def fail(message: str, detail: str = "") -> int:
    """Print an error to stderr and return the failure exit code."""
    if detail:
        print(f"error: {message}: {detail}", file=sys.stderr)
    else:
        print(f"error: {message}", file=sys.stderr)
    return 1


def main(argv: list[str] | None = None) -> int:
    """Run the generator; return 0 on success, 1 on any failure."""
    args = parse_args(argv)
    source = source_path()

    if not os.path.isfile(source):
        return fail(ERR_SOURCE_MISSING, source)

    if args.verify:
        try:
            ok = verify_hash(source, EXPECTED_SHA256)
        except OSError as exc:
            return fail("cannot read source image", str(exc))
        if not ok:
            return fail(ERR_DOCUMENTED_HASH_MISMATCH, source)
        print(f"verified {source}")
        print(f"sha256 {EXPECTED_SHA256}")
        # Verify-only run: no output destination was requested, so
        # there is nothing to write. When an output directory was
        # given (flag or environment variable) execution continues
        # below and writes the copy as well.
        output_requested = bool(
            args.output_dir or os.environ.get("MAKEFUN_OUTPUT_DIR")
        )
        if not output_requested:
            return 0

    target = output_path(args.output_dir)
    try:
        copy_image(source, target)
    except FileNotFoundError:
        return fail(ERR_SOURCE_MISSING, source)
    except OSError as exc:
        return fail(ERR_COPY_FAILED, str(exc))

    # The destination must be byte-identical to the source; a
    # mismatch here means the storage layer corrupted the copy, so
    # the run is a failure even though a file was written.
    try:
        source_hash = sha256_file(source)
        target_hash = sha256_file(target)
    except OSError as exc:
        return fail("cannot hash output", str(exc))
    if target_hash != source_hash:
        return fail(ERR_HASH_MISMATCH, target)
    if args.verify and target_hash != EXPECTED_SHA256:
        return fail(ERR_DOCUMENTED_HASH_MISMATCH, target)

    print(f"wrote {target}")
    print(f"sha256 {target_hash}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
