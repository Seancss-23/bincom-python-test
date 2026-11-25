"""Search, base-10 conversion, Fibonacci and the 1s puzzle (Q7-Q9)."""

import random
import re


def binary_search(items, target, low=0, high=None):
    """Recursive binary search. Returns the index of target, or -1.

    `items` must be sorted: each step throws away half the list by assuming
    everything left of the middle is smaller and everything right is bigger.
    """
    if high is None:
        high = len(items) - 1
    if low > high:  # nothing left to look at
        return -1
    middle = (low + high) // 2
    if items[middle] == target:
        return middle
    if items[middle] < target:
        return binary_search(items, target, middle + 1, high)
    return binary_search(items, target, low, middle - 1)


def ask_and_search(numbers):
    """Ask the user for a number (re-asking on bad input) and search for it."""
    while True:
        text = input("    Enter a number to search for: ").strip()
        try:
            target = int(text)
            break
        except ValueError:
            print(f"    '{text}' is not a whole number, try again.")
    return target, binary_search(sorted(numbers), target)


def random_binary_digits(length=4):
    """Build a random string of 0s and 1s, e.g. '1011'."""
    return "".join(random.choice("01") for _ in range(length))


def binary_to_decimal(bits):
    """Convert a string of 0s and 1s to base 10 by hand.

    Each digit is worth a power of 2, from the right: 1, 2, 4, 8, ...
    """
    total = 0
    for position, digit in enumerate(reversed(bits)):
        total += int(digit) * 2 ** position
    return total


def fibonacci_sum(count):
    """Sum of the first `count` Fibonacci numbers, starting 0, 1, 1, 2, ...

    A loop, not recursion: naive recursion would redo the same work
    billions of times for 50 terms.
    """
    total = 0
    current, following = 0, 1
    for _ in range(count):
        total += current
        current, following = following, current + following
    return total


def ones_run_puzzle(bits):
    """Output 1 at the end of every run of exactly three 1s, else 0.

    Runs of one, two, four or more 1s all give 0. A run that finishes the
    string still counts (the sample ends with one).
    """
    result = ["0"] * len(bits)
    for run in re.finditer(r"1+", bits):
        if run.end() - run.start() == 3:
            result[run.end() - 1] = "1"
    return "".join(result)
