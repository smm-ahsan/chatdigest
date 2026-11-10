#!/usr/bin/env python3
"""ChatDigest - turn a pasted chat transcript into a clean digest.

Reads a transcript whose lines look like "Name: message text" and prints:
  - Participants: who spoke, and how many messages each person sent
  - Questions:    messages that end with "?"
  - Decisions:    messages containing decision keywords
  - Action items: messages containing action keywords

The keyword matching is deliberately simple (plain substring checks),
not AI. A message may appear in several sections - that is fine.

Usage:
    python3 chatdigest.py --file chat.txt
    python3 chatdigest.py --text "Sara: Did you see the draft?"
"""

import argparse
import sys

DECISION_KEYWORDS = [
    "decided",
    "agreed",
    "we will go with",
    "confirmed",
    "final:",
]

ACTION_KEYWORDS = [
    "i will",
    "you will",
    "please",
    "todo",
    "action:",
    "by tomorrow",
    "by friday",
    "deadline",
]


def parse_transcript(text):
    """Split raw transcript text into (name, message) pairs.

    Returns (messages, ignored_count) where messages is a list of
    (name, message) tuples in the order they appeared, and
    ignored_count is the number of non-blank lines that had no
    "Name: " prefix.
    """
    messages = []
    ignored = 0
    for line in text.splitlines():
        if not line.strip():
            continue
        if ": " in line:
            name, message = line.split(": ", 1)
            name = name.strip()
            message = message.strip()
            if name:
                messages.append((name, message))
            else:
                ignored += 1
        else:
            ignored += 1
    return messages, ignored


def contains_any(text, keywords):
    lowered = text.lower()
    return any(keyword in lowered for keyword in keywords)


def build_digest(messages, ignored):
    """Return the digest as a single string (no trailing newline)."""
    lines = []

    # Participants, in order of first appearance.
    lines.append("Participants:")
    counts = {}
    order = []
    for name, _message in messages:
        if name not in counts:
            counts[name] = 0
            order.append(name)
        counts[name] += 1
    for name in order:
        lines.append("{}: {} messages".format(name, counts[name]))
    lines.append("")

    # Questions: message text ends with "?".
    lines.append("Questions:")
    questions = [(n, m) for n, m in messages if m.rstrip().endswith("?")]
    if questions:
        for name, message in questions:
            lines.append("- {}: {}".format(name, message))
    else:
        lines.append("- None found.")
    lines.append("")

    # Decisions: keyword match.
    lines.append("Decisions:")
    decisions = [(n, m) for n, m in messages
                 if contains_any(m, DECISION_KEYWORDS)]
    if decisions:
        for name, message in decisions:
            lines.append("- {}: {}".format(name, message))
    else:
        lines.append("- None found.")
    lines.append("")

    # Action items: keyword match.
    lines.append("Action items:")
    actions = [(n, m) for n, m in messages
               if contains_any(m, ACTION_KEYWORDS)]
    if actions:
        for name, message in actions:
            lines.append("- {}: {}".format(name, message))
    else:
        lines.append("- None found.")

    # Note about unparsed lines, only when there were any.
    if ignored > 0:
        lines.append("")
        lines.append(
            "Ignored {} lines without a 'Name:' prefix.".format(ignored))

    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Turn a pasted chat transcript into a clean digest: "
                    "participants, questions, decisions and action items.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--file", metavar="PATH",
                       help="path to a transcript text file")
    group.add_argument("--text", metavar="TEXT",
                       help="transcript text given directly as a string")
    args = parser.parse_args(argv)

    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as handle:
                raw = handle.read()
        except OSError as exc:
            print("error: could not read file '{}': {}".format(
                args.file, exc.strerror or exc), file=sys.stderr)
            return 2
    else:
        raw = args.text

    messages, ignored = parse_transcript(raw)
    print(build_digest(messages, ignored))
    return 0


if __name__ == "__main__":
    sys.exit(main())
