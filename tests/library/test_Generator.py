import pytest
from library.Generator import Generator


@pytest.fixture
def generator():
    class ConcreteGenerator(Generator):
        def generate_and_return_sequence(self):
            pass

    return ConcreteGenerator()


@pytest.mark.parametrize("seed", [None, 12345])
def test_set_seed(generator, seed):
    generator.set_seed(seed)
    assert generator.seed == seed


def test_set_seed_invalid(generator):
    with pytest.raises(ValueError):
        generator.set_seed("invalid_seed")


def test_generate_and_return_sequence(generator):
    with pytest.raises(NotImplementedError):
        generator.generate_and_return_sequence()


def test_generate_and_return_sequence_invalid_input(generator):
    with pytest.raises(NotImplementedError):
        generator.generate_and_return_sequence()
