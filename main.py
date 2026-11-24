#!/usr/bin/env python3
"""The Robot Apology — make.fun entry.

Writes a two-line robot confession to /output/entry.txt.
Line 1: one sentence apologizing for one specific mistake.
Line 2: one sentence saying what the robot learned and what it will
do differently, following directly from that mistake.
"""

import os

LINE1 = "I am sorry I replied-all to the whole office with your lunch order, so forty-three people now know you wanted extra pickles."
LINE2 = "I have learned to check who is on the list before I press send, and I will ask before sharing anything with more than one person."

ENTRY = LINE1 + "\n" + LINE2 + "\n"

# Generic promises that do not count as a lesson drawn from a mistake.
BANNED_GENERIC = ("do better", "try harder", "be better", "do my best")


def validate(text):
    """Check the entry is a two-line robot apology whose lesson follows
    from its exact mistake. Raises ValueError on any failure."""
    if not text or not text.strip():
        raise ValueError("entry is empty or only whitespace")
    if len(text) > 400:
        raise ValueError("entry exceeds 400 characters")
    lines = text.rstrip("\n").split("\n")
    if len(lines) != 2:
        raise ValueError("entry must be exactly 2 lines, got %d" % len(lines))
    line1, line2 = lines
    for i, line in enumerate(lines, 1):
        if line != line.strip():
            raise ValueError("line %d has leading/trailing whitespace" % i)
        if "  " in line:
            raise ValueError("line %d has double spaces" % i)
        if line.count(".") != 1 or not line.endswith("."):
            raise ValueError("line %d must be a single sentence" % i)
    # Line 1: an apology naming one specific mistake.
    if not line1.lower().startswith("i am sorry"):
        raise ValueError("line 1 must open with an apology")
    if "replied-all" not in line1 or "lunch order" not in line1:
        raise ValueError("line 1 must name one specific mistake")
    # Line 2: a lesson that follows from that exact mistake.
    lowered = line2.lower()
    if "i have learned" not in lowered:
        raise ValueError("line 2 must state what was learned")
    if not any(tok in lowered for tok in ("list", "press send", "sharing")):
        raise ValueError("line 2 lesson must follow from the reply-all mistake")
    if any(phrase in lowered for phrase in BANNED_GENERIC):
        raise ValueError("line 2 must not be a generic promise to do better")


def main():
    validate(ENTRY)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(ENTRY)


if __name__ == "__main__":
    main()
