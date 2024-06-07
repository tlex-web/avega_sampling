import pytest
from library.PRNG.PCGRNG import PCGRNG


@pytest.fixture
def rng():
    return PCGRNG()


def test_seed(rng):
    rng.seed(12345)
    assert rng.state == 0x853C49E6748FEA9B


def test_next(rng):
    rng.seed(12345)
    assert rng.next() == 0x8C6E96A7836F2DDB


def test_get_random_number(rng):
    rng.seed(12345)
    random_number = rng.get_random_number(1, 10)
    assert random_number >= 1 and random_number <= 10
