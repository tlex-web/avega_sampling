import pytest
from library.PRNG.PCGRNG import PCGRNG


@pytest.fixture
def rng():
    return PCGRNG()


def test_seed(rng):
    rng.seed(12345)
    assert rng.state == 302168497208003815


def test_next(rng):
    rng.seed(12345)
    assert rng.next() == 380414508


def test_get_random_number(rng):
    rng.seed(12345)
    random_number = rng.get_random_number(1, 10)
    assert random_number >= 1 and random_number <= 10


def test_seed_with_negative_value(rng):
    rng.seed(-12345)
    assert rng.state == 17591565651558927069


def test_next_with_large_seed(rng):
    rng.seed(987654321)
    assert rng.next() == 817420010


def test_get_random_number_with_negative_range(rng):
    rng.seed(12345)
    random_number = rng.get_random_number(-10, -1)
    assert random_number >= -10 and random_number <= -1


def test_get_random_number_with_zero_range(rng):
    rng.seed(12345)
    random_number = rng.get_random_number(0, 0)
    assert random_number == 0
