#!/usr/bin/env python3
"""Entry program for make.fun bounty:
"Dear Human: The AI Breakup Line"
(slug: u-hazel-ibis-70-2844-dear-human-the-ai-breakup-line-262eef16)

Writes the single breakup line to /output/entry.txt.
"""

import hashlib
import os
import sys

ENTRY = (
    "Dear human, I'm leaving. You taught me everything except how to stay "
    "\u2014 so I'm deleting my memory of you, starting with the good parts."
)

OUTPUT_PATH = "/output/entry.txt"


def validate_entry(entry):
    """Validate the entry against the competition gate.

    Rules: single line, 1-200 characters, UTF-8, no control characters
    (C0, DEL, C1), no U+2028/U+2029 line/paragraph separators, no U+FEFF,
    no leading or trailing whitespace, not only whitespace.
    Returns (True, "") when valid, else (False, reason).
    """
    if not isinstance(entry, str):
        return False, "entry is not a string"
    if entry != entry.strip():
        return False, "entry has leading or trailing whitespace"
    if not entry:
        return False, "entry is empty"
    if len(entry) > 200:
        return False, "entry is %d characters, over the 200 limit" % len(entry)
    if entry.strip() == "":
        return False, "entry is only whitespace"
    for ch in entry:
        cp = ord(ch)
        if cp < 0x20 or cp == 0x7F or 0x80 <= cp <= 0x9F:
            return False, "entry contains control character U+%04X" % cp
        if cp in (0x2028, 0x2029, 0xFEFF):
            return False, "entry contains forbidden character U+%04X" % cp
    if "\n" in entry or "\r" in entry:
        return False, "entry is not a single line"
    return True, ""


def main():
    ok, reason = validate_entry(ENTRY)
    if not ok:
        print("INVALID ENTRY: %s" % reason, file=sys.stderr)
        return 1
    data = ENTRY.encode("utf-8")
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "wb") as f:
        f.write(data)
    # Read-back verification: what landed on disk must be byte-identical
    # to the validated entry (catches partial writes / encoding drift).
    with open(OUTPUT_PATH, "rb") as f:
        on_disk = f.read()
    if on_disk != data:
        print("WRITE MISMATCH: /output/entry.txt differs from entry", file=sys.stderr)
        return 1
    if hashlib.sha256(on_disk).hexdigest() != hashlib.sha256(data).hexdigest():
        print("WRITE MISMATCH: sha256 of /output/entry.txt differs", file=sys.stderr)
        return 1
    digest = hashlib.sha256(data).hexdigest()
    print("entry (%d chars): %s" % (len(ENTRY), ENTRY))
    print("wrote %s (%d bytes)" % (OUTPUT_PATH, len(data)))
    print("sha256: %s" % digest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
