from project import get_sides, get_equilateral, create_polygon, get_ideal_ratio
import numpy as np


def test_get_sides(monkeypatch):
    input = "4"

    monkeypatch.setattr("builtins.input", lambda _: input)

    assert get_sides() == 4


def test_get_equilateral(monkeypatch):
    inputs = ["True", "T", "true", "t", "False", "F", "false", "f"]

    for i in range(len(inputs)):
        monkeypatch.setattr("builtins.input", lambda _: inputs[i])

        if i < 4:
            assert get_equilateral() == True

        else:
            assert get_equilateral() == False


def test_create_polygon():
    x_test, y_test = create_polygon(3, True)
    x_expected, y_expected = np.array(
        [
            [0.0, 1.0],
            [0.8660254037844387, -0.4999999999999998],
            [-0.8660254037844384, -0.5000000000000004],
        ]
    ).T

    assert x_test.all() == x_expected.all()
    assert y_test.all() == y_expected.all()


def test_get_ideal_ratio():
    assert get_ideal_ratio(7) == 0.6974066116513887
