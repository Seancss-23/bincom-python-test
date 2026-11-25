import sys
from fractions import Fraction
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import algorithms  # noqa: E402
import colours  # noqa: E402


@pytest.fixture(scope="module")
def all_colours():
    return colours.load_colours(ROOT / "python_class_question.html")


@pytest.fixture(scope="module")
def counts(all_colours):
    return colours.count_colours(all_colours)


def test_total_is_95(all_colours):
    assert len(all_colours) == 95


def test_blew_becomes_blue_and_arsh_is_kept(all_colours, counts):
    assert "BLEW" not in all_colours
    assert counts["BLUE"] == 31
    assert counts["ARSH"] == 1


def test_counts(counts):
    assert dict(counts) == {
        "BLUE": 31, "WHITE": 16, "GREEN": 10, "ORANGE": 9, "RED": 9, "BROWN": 6,
        "YELLOW": 5, "PINK": 5, "CREAM": 2, "ARSH": 1, "BLACK": 1,
    }


def test_mode(counts):
    assert colours.mode_colours(counts) == ["BLUE"]


def test_mean_colour_is_a_tie(counts):
    mean_frequency, names = colours.mean_colours(counts)
    assert mean_frequency == pytest.approx(95 / 11)
    assert names == ["ORANGE", "RED"]


def test_median(all_colours):
    assert colours.median_colour(all_colours) == "GREEN"


def test_variance(counts):
    assert colours.variance(counts) == pytest.approx(68.23, abs=0.01)
    assert colours.variance(counts, sample=True) == pytest.approx(75.05, abs=0.01)


def test_probability_of_red(all_colours):
    red = colours.probability(all_colours, "red")
    assert red == Fraction(9, 95)
    assert float(red) == pytest.approx(0.0947, abs=0.0001)


def test_binary_search_found():
    numbers = [1, 3, 5, 7, 9, 11]
    assert all(algorithms.binary_search(numbers, n) == i for i, n in enumerate(numbers))


def test_binary_search_not_found():
    assert algorithms.binary_search([1, 3, 5, 7], 4) == -1


def test_binary_search_empty_list():
    assert algorithms.binary_search([], 5) == -1


def test_binary_to_decimal():
    assert algorithms.binary_to_decimal("1011") == 11
    assert algorithms.binary_to_decimal("0000") == 0
    assert algorithms.binary_to_decimal("1111") == 15


def test_random_binary_digits_are_valid():
    for _ in range(50):
        bits = algorithms.random_binary_digits()
        assert len(bits) == 4 and set(bits) <= {"0", "1"}
        assert algorithms.binary_to_decimal(bits) == int(bits, 2)


def test_fibonacci_sum():
    assert algorithms.fibonacci_sum(50) == 20365011073
    assert algorithms.fibonacci_sum(5) == 0 + 1 + 1 + 2 + 3


def test_ones_puzzle_sample():
    sample = "0101101011101011011101101000111"
    assert algorithms.ones_run_puzzle(sample) == "0000000000100000000100000000001"


def test_ones_puzzle_ignores_runs_that_are_not_three():
    assert algorithms.ones_run_puzzle("1101111011") == "0000000000"
