#!/usr/bin/env python3
"""Describe Your Ex in One Word -- make.fun bounty entry.

The brief: sum up an ex in exactly one word, at most 111 characters,
with nothing else attached. A judge model reads the words two at a
time and picks the funnier one, weighing first whether the word really
is a one-word verdict on an ex, then comic punch, surprise, craft and
recognition. This program ranks a shortlist of candidate words against
those five criteria, in the judge's own priority order, and writes the
winner -- and nothing else -- to ``$MAKEFUN_OUTPUT_DIR/entry.txt``.

The winner is "draft". A draft is never the final version: it exists
to be rewritten, thrown away, or replaced by the real thing. Calling
an ex a draft says the whole relationship was a rehearsal copy -- funny
because it reframes years of history as an unfinished document, and it
stings because everyone has been somebody's rough copy at least once.
Five letters, no explanation needed, and no near-synonym keeps the
edge: "rough draft" would need two words, and "draft" already carries
both meanings on its own.
"""

import os
import sys
from pathlib import Path

# The judge's criteria, in priority order. Earlier criteria count more:
# a word that fails as a verdict on an ex cannot win on punch alone.
CRITERIA = ("verdict", "punch", "surprise", "craft", "recognition")
WEIGHTS = {"verdict": 5, "punch": 4, "surprise": 3, "craft": 2, "recognition": 1}

# Each candidate maps every criterion to a mark out of 10.
CANDIDATES = {
    # The pick. A draft is a version that was never meant to last:
    # funny, surprising, and instantly understood.
    "draft": {
        "verdict": 10,
        "punch": 9,
        "surprise": 9,
        "craft": 10,
        "recognition": 9,
    },
    # The beta version of a partner: the joke lands, but "beta" also
    # reads as an insult about the person rather than the relationship.
    "beta": {
        "verdict": 9,
        "punch": 9,
        "surprise": 9,
        "craft": 8,
        "recognition": 8,
    },
    # Past its date, like milk: relatable, but the gag is a single
    # image with no second meaning behind it.
    "expired": {
        "verdict": 9,
        "punch": 8,
        "surprise": 8,
        "craft": 8,
        "recognition": 9,
    },
    # A free trial that ended: funny, but it describes a product
    # demo more than it delivers a verdict on a person.
    "demo": {
        "verdict": 8,
        "punch": 8,
        "surprise": 8,
        "craft": 8,
        "recognition": 7,
    },
    # The tutorial level before the real game: clever, but it flatters
    # the ex into being a lesson instead of judging them.
    "tutorial": {
        "verdict": 8,
        "punch": 7,
        "surprise": 8,
        "craft": 8,
        "recognition": 7,
    },
    # "I want my money back": a good punchline, but a refund is
    # something you ask for, not a word that describes an ex.
    "refund": {
        "verdict": 7,
        "punch": 8,
        "surprise": 8,
        "craft": 7,
        "recognition": 7,
    },
    # A glitch in the story: vivid, but it blames fate instead of
    # passing a verdict.
    "glitch": {
        "verdict": 7,
        "punch": 7,
        "surprise": 7,
        "craft": 6,
        "recognition": 6,
    },
    # Honest and sad, but it sighs instead of landing a joke.
    "unfinished": {
        "verdict": 9,
        "punch": 5,
        "surprise": 5,
        "craft": 7,
        "recognition": 8,
    },
    # A placeholder held the seat for the real thing: close, but the
    # word is a thing, not quite a verdict on a person.
    "placeholder": {
        "verdict": 8,
        "punch": 7,
        "surprise": 6,
        "craft": 7,
        "recognition": 7,
    },
    # The cliche every ex gets called: the judge has heard it a
    # hundred times, so the surprise is gone.
    "lesson": {
        "verdict": 9,
        "punch": 4,
        "surprise": 3,
        "craft": 6,
        "recognition": 7,
    },
}

# The brief's gate: one word, at most 111 characters, nothing else.
MAX_CHARS = 111


def total_for(marks):
    """Weighted total for one candidate's marks, criteria in order."""
    return sum(WEIGHTS[name] * marks[name] for name in CRITERIA)


def choose(candidates):
    """Highest weighted total wins; ties break to the shorter word,
    then alphabetically, so the choice is fully deterministic."""
    ranked = sorted(
        candidates.items(),
        key=lambda item: (-total_for(item[1]), len(item[0]), item[0]),
    )
    return ranked[0][0]


def check(word):
    """The brief admits exactly one word: 1-111 characters, no spaces."""
    if not word or len(word) > MAX_CHARS:
        raise ValueError("entry must be 1 to 111 characters")
    if any(ch.isspace() for ch in word):
        raise ValueError("entry must be exactly one word")


def main():
    word = choose(CANDIDATES)
    check(word)
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "entry.txt").write_text(word, encoding="utf-8")
    print(word)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
