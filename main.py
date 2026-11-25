"""Bincom Python Trainee test: runs every question in order and prints a report."""

from pathlib import Path

import algorithms
import colours
import db

HTML_FILE = Path(__file__).parent / "python_class_question.html"
PUZZLE_INPUT = "0101101011101011011101101000111"
PUZZLE_EXPECTED = "0000000000100000000100000000001"
SEARCH_LIST = [3, 8, 15, 22, 42, 57, 61, 79, 94]


def main():
    all_colours = colours.load_colours(HTML_FILE)
    counts = colours.count_colours(all_colours)
    total = len(all_colours)

    print("Data notes")
    print("    BLEW was read as BLUE (obvious typo).")
    print("    ARSH was kept as written: it could be ASH, so it is not guessed.")
    print(f"    {total} colour values over 5 days, {len(counts)} distinct colours.\n")

    mean_frequency, mean_names = colours.mean_colours(counts)
    print(f"Q1. Mean colour: {' and '.join(mean_names)}")
    print(f"    Mean frequency is {total}/{len(counts)} = {mean_frequency:.2f}; "
          f"these are closest ({counts[mean_names[0]]} each).")

    mode_names = colours.mode_colours(counts)
    print(f"Q2. Most worn colour: {' and '.join(mode_names)} "
          f"({counts[mode_names[0]]} of {total})")

    print(f"Q3. Median colour: {colours.median_colour(all_colours)}")
    print(f"    Middle (position {total // 2 + 1} of {total}) when all values are sorted A-Z.")

    print(f"Q4. Variance of the frequencies: {colours.variance(counts):.2f} (population)")
    print(f"    Sample variance, for reference: {colours.variance(counts, sample=True):.2f}. "
          "Population is used because this is the whole week, not a sample.")

    red = colours.probability(all_colours, "RED")
    print(f"Q5. Probability a random colour is red: {red} = {float(red):.4f} = {float(red):.2%}")

    print("Q6. PostgreSQL save (table colour_frequencies):")
    rows = db.save_and_read_back(counts)
    if rows is not None:
        print("    Saved. Read back from the database:")
        for colour, frequency in rows:
            print(f"      {colour:<8} {frequency}")

    print(f"Q7. Recursive binary search in {SEARCH_LIST}")
    target, index = algorithms.ask_and_search(SEARCH_LIST)
    print(f"    {target} found at index {index}." if index >= 0 else f"    {target} not found.")

    bits = algorithms.random_binary_digits()
    by_hand = algorithms.binary_to_decimal(bits)
    print(f"Q8. Random 4-digit binary number {bits} = {by_hand} in base 10")
    print(f"    Check with int(bits, 2): {int(bits, 2)} ({'match' if by_hand == int(bits, 2) else 'MISMATCH'})")

    print(f"Q9. Sum of the first 50 Fibonacci numbers: {algorithms.fibonacci_sum(50)}")
    print("    Sequence starts 0, 1, 1, 2, ...")

    answer = algorithms.ones_run_puzzle(PUZZLE_INPUT)
    print("Puzzle. 1 where a run of exactly three 1s ends:")
    print(f"    Input:    {PUZZLE_INPUT}")
    print(f"    Output:   {answer}")
    print(f"    Expected: {PUZZLE_EXPECTED} ({'match' if answer == PUZZLE_EXPECTED else 'MISMATCH'})")


if __name__ == "__main__":
    main()
