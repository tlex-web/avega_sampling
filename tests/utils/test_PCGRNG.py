from datetime import datetime, date, timedelta
from library.PRNG.PCGRNG import PCGRNG


def test_seed():
    rng = PCGRNG()
    assert rng.state == 16869222179800739361


def test_next():
    rng = PCGRNG()
    rng.seed(12345)
    assert rng.next() == 380414508


def test_get_random_number():
    rng = PCGRNG()
    rng.seed(12345)
    random_number = rng.get_random_number(1, 10)
    assert 1 <= random_number <= 10


def test_get_unique_random_number_sequence():
    rng = PCGRNG()
    rng.seed(12345)
    sequence = rng.get_unique_random_number_sequence(1, 10, 5)
    assert len(sequence) == 5
    assert set(sequence) == set([2, 3, 6, 7, 9])


def test_get_random_date():
    rng = PCGRNG()
    rng.seed(12345)
    start_date = date(2022, 1, 1)
    end_date = date(2022, 1, 10)
    random_date = rng.get_random_date(start_date, end_date)
    assert start_date <= random_date <= end_date


def test_create_unique_date_sequence():
    rng = PCGRNG()
    rng.seed(12345)
    start_date = date(2022, 1, 1)
    end_date = date(2022, 1, 10)
    length = 5
    order = "ascending"
    sequence = rng.create_unique_date_sequence(start_date, end_date, length, order)
    assert len(sequence) == length
    assert sequence == [
        datetime(2022, 1, 2, 0, 0),
        datetime(2022, 1, 3, 0, 0),
        datetime(2022, 1, 6, 0, 0),
        datetime(2022, 1, 7, 0, 0),
        datetime(2022, 1, 9, 0, 0),
    ]
