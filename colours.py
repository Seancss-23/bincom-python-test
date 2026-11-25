"""Read the Bincom colour table and answer the statistics questions (Q1-Q5)."""

import re
from collections import Counter
from fractions import Fraction
from pathlib import Path

# Obvious typos only. ARSH is deliberately NOT here: it could mean "ASH",
# so guessing would be inventing data.
TYPO_FIXES = {"BLEW": "BLUE"}


def load_colours(html_path):
    """Return every colour in the table as a flat, cleaned list (95 values)."""
    html = Path(html_path).read_text(encoding="utf-8")
    colours = []
    for row in re.findall(r"<tr>(.*?)</tr>", html, re.DOTALL):
        cells = re.findall(r"<td>(.*?)</td>", row, re.DOTALL)
        if len(cells) != 2:
            continue
        for raw in cells[1].split(","):
            colour = raw.strip().upper()
            if colour:
                colours.append(TYPO_FIXES.get(colour, colour))
    return colours


def count_colours(colours):
    """Return {colour: how many times it was worn}."""
    return Counter(colours)


def mean_colours(counts):
    """Colours aren't numbers, so use the mean frequency (total / distinct
    colours) and return the colour(s) whose count is closest to it."""
    mean_frequency = sum(counts.values()) / len(counts)
    gap = {colour: abs(n - mean_frequency) for colour, n in counts.items()}
    smallest = min(gap.values())
    return mean_frequency, sorted(c for c, g in gap.items() if g == smallest)


def mode_colours(counts):
    """Most worn colour(s); a list because there could be a tie."""
    highest = max(counts.values())
    return sorted(c for c, n in counts.items() if n == highest)


def median_colour(colours):
    """Sort alphabetically and take the middle value (index 47 of 95)."""
    return sorted(colours)[len(colours) // 2]


def variance(counts, sample=False):
    """Variance of the colour frequencies.

    Population (divide by n) is the default: we hold the whole week, not a
    sample drawn from a bigger group. sample=True divides by n - 1.
    """
    values = list(counts.values())
    mean = sum(values) / len(values)
    squared_gaps = sum((v - mean) ** 2 for v in values)
    return squared_gaps / (len(values) - 1 if sample else len(values))


def probability(colours, wanted):
    """Chance that a colour picked at random from all 95 is `wanted`, as an
    exact fraction (9/95 for red)."""
    return Fraction(colours.count(wanted.upper()), len(colours))
