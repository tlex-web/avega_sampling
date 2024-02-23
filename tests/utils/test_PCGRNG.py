from utils.PCGRNG import PCGRNG


def test_seed():
    rng = PCGRNG()
    rng.seed(12345)
    assert rng.state == 302168497208003815


def test_next():
    rng = PCGRNG()
    rng.seed(12345)
    assert rng.next() == 380414508


def test_get_random_number():
    rng = PCGRNG()
    rng.seed(12345)
    random_number = rng.get_random_number(1, 10)
    assert random_number >= 1 and random_number <= 10


def test_get_unique_random_sequence():
    rng = PCGRNG()
    rng.seed(12345)
    sequence = rng.get_unique_random_sequence(1, 10, 5)
    assert len(sequence) == 5
    assert all(number >= 1 and number <= 10 for number in sequence)
    assert len(set(sequence)) == len(sequence)


def test_get_unique_random_sequence_invalid_length():
    rng = PCGRNG()
    rng.seed(12345)
    try:
        rng.get_unique_random_sequence(1, 10, 15)
        assert False  # Should raise a ValueError
    except ValueError:
        assert True
