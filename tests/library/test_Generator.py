import pytest
import pytest_mock
from library.Generator import Generator


@pytest.fixture
def generator():
    class ConcreteGenerator(Generator):
        def generate_and_return_sequence(self):
            pass

    return ConcreteGenerator()


@pytest.fixture
def seed_value():
    return 12345


mocker = pytest_mock.mocker


def test_generator_instance(generator):
    assert isinstance(generator, Generator)


def test_seed_value(generator, seed_value):
    generator.seed = seed_value
    assert generator.seed == seed_value


def test_set_seed(generator, seed_value):
    generator.set_seed(seed_value)
    assert generator.seed == seed_value


def test_set_seed_invalid(generator):
    with pytest.raises(ValueError):
        generator.set_seed("invalid_seed")


def test_not_implemented_abc_method(generator, mocker):

    mocker.patch.object(
        generator, "generate_and_return_sequence", side_effect=NotImplementedError
    )

    with pytest.raises(NotImplementedError):
        generator.generate_and_return_sequence()
