from app import add, greet, multiply


def test_add():
    assert add(2, 3) == 5


def test_multiply():
    assert multiply(4, 5) == 20


def test_greet():
    assert greet("Yash") == "Hello, Yash!"