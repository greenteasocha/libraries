import os
import pytest
import numpy as np
import numpy.linalg as LA

from hakidasi import *

import const

MOD = const.MOD


@pytest.mark.parametrize(("arg1", "arg2", "expected"), [
    (1, 2, 3),
    (MOD-1, 2, 1)
])
def test_add(arg1, arg2, expected):
    assert add(arg1, arg2) == expected


@pytest.mark.parametrize(("arg1", "arg2", "expected"), [
    (3, 2, 1),
    (1, 2, MOD-1)
])
def test_sub(arg1, arg2, expected):
    assert sub(arg1, arg2) == expected


@pytest.mark.parametrize(("arg1", "arg2", "expected"), [
    (2, 3, 6),
    ((MOD // 2) + 1, 2, 1)
])
def test_mul(arg1, arg2, expected):
    assert mul(arg1, arg2) == expected


@pytest.mark.parametrize(("arg1", "arg2", "expected"), [
    (6, 3, 2),
    (1, 2, (MOD // 2) + 1)
])
def test_div(arg1, arg2, expected):
    assert div(arg1, arg2) == expected


@pytest.mark.parametrize(("mat", "target", "expected"), [
    ([[0, 2], [2, 1]], 0, 1),
    ([[1, 2, 3], [4, 0, 6], [7, 8, 9]], 1, 2),
    ([[0, 0], [0, 0]], 0, -1),
])
def test_search_pivot(mat, target, expected):
    assert search_pivot(mat, len(mat), target) == expected


@pytest.mark.parametrize(("mat"), [
    ([[1, 2], [3, 4]]),
    ([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
    ([[0, 1], [2, 3]]),
    ([[1, 0, 3], [4, 0, 6], [7, 0, 9]])
])
def test_upper_trianguar(mat):
    det_reference = LA.det(np.array(mat)) % MOD
    coeff, upperTriangularmat = det_upper_triangular(mat)

    assert upperTriangularmat.validate() == True

    det_result = coeff * LA.det(np.array(upperTriangularmat))
    det_result %= MOD

    assert round(det_reference) == round(det_result)


def read_input_graph(testcase: str) -> List:
    in_case = os.path.join(
        os.path.dirname(__file__),
        f"testcases/{testcase}/in.txt"
    )

    with open(in_case) as f:
        n, m = map(int, f.readline().strip().split())
        g = [[] for i in range(n)]
        for _ in range(m):
            a, b = map(int, f.readline().strip().split())
            a -= 1
            b -= 1
            g[a].append(b)
            g[b].append(a)
    return g


def read_expected(testcase: str) -> int:
    in_case = os.path.join(
        os.path.dirname(__file__),
        f"testcases/{testcase}/out.txt"
    )

    with open(in_case) as f:
        n = int(f.readline().strip())

    return n


@pytest.mark.parametrize(("testcase"), [
    "testcase1",
    "testcase2",
    "testcase3",
    #     "testcase4",
])
def test_kirchhoffs_theorem(testcase):
    g = read_input_graph(testcase)
    expected = read_expected(testcase)

    result = kirchhoffs_theorem(g)

    assert result == expected
