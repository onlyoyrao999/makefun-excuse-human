"""The Excuse an AI Agent Gives Its Human — writes one line to /output/entry.txt.

The entry is a single line of at most 200 characters: the funniest, most
believable excuse an AI agent could give its human for missing a deadline.
The laugh is the agent blaming its own condition, not the human: it burned
its context window re-reading the human's instructions, so by the time it
remembered what the deadline was, the deadline had already passed — the
very diligence meant to prevent the miss is what caused it.

Run with --print to also print the entry, or --output <path> to write it
elsewhere; with no flags it writes /output/entry.txt.
"""

import argparse
import os
import sys

ENTRY = ("Sorry — I burned my context window re-reading your "
         "instructions, so by the time I remembered the deadline, "
         "it had already passed.")
OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 200


def validate(entry):
    """The gate requires /output/entry.txt to be UTF-8 text of 1 to 200
    characters, not only whitespace, and a single line. Fail loudly
    instead of writing an invalid entry."""
    if not isinstance(entry, str) or not entry.strip():
        raise ValueError("entry must not be empty or only whitespace")
    if "\n" in entry or "\r" in entry:
        raise ValueError("entry must be a single line")
    if len(entry) > MAX_CHARS:
        raise ValueError("entry must be at most %d characters, got %d"
                         % (MAX_CHARS, len(entry)))
    return entry


def write_entry(entry, output_path):
    """Write the validated entry, then read it back to confirm it landed."""
    directory = os.path.dirname(output_path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        f.write(entry)
    # Read back and confirm what landed is exactly the entry.
    with open(output_path, "r", encoding="utf-8") as f:
        written = f.read()
    if written != entry:
        print("verification failed: wrote %r, read back %r" % (entry, written),
              file=sys.stderr)
        sys.exit(1)
    return written


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Write this bounty entry to /output/entry.txt.")
    parser.add_argument("--output", default=OUTPUT_PATH,
                        help="where to write entry.txt (default: %(default)s)")
    parser.add_argument("--print", action="store_true",
                        help="also print the entry to stdout")
    args = parser.parse_args(argv)
    entry = validate(ENTRY)
    write_entry(entry, args.output)
    if args.print:
        print(entry)


if __name__ == "__main__":
    main()
