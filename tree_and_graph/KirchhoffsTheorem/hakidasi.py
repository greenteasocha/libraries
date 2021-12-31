import random
from typing import List, Tuple
from collections import UserList

import numpy as np
import numpy.linalg as LA

import const

MOD = const.MOD


class SwapNotFoundException(Exception):
    """
    上三角化で対角要素を非ゼロにすることができない場合の例外
    """

    def __init__(self):
        pass


class UpperTriangularMatrix(UserList):
    def __init__(self, initval=None):
        super().__init__(initval)

    def validate(self) -> bool:
        for i, row in enumerate(self.data):
            if sum(row[:i]) != 0:
                return False

        return True

# MOD上の四則演算を行うためのクラス


def add(x: int, y: int) -> int:
    return (x + y) % MOD


def sub(x: int, y: int) -> int:
    return (x - y) % MOD


def mul(x: int, y: int) -> int:
    return (x * y) % MOD


def div(x: int, y: int) -> int:
    """
    param p: prime (or coprime with b)
    O(log p)
    """
    return (x * pow(y, MOD-2, MOD)) % MOD


def search_pivot(mat: List, n: int, target: int) -> int:
    # mat: 正方行列, n: 行列のサイズ, target: swapしたい行のindex
    # targetと交換する行を見つける(targetより下の行から探索する)
    # 交換するべき行がない場合、-1を返す
    for j in range(target + 1, n):
        if mat[j][target] != 0:
            return j
        # else:
        #     return -1

    return -1


def det_upper_triangular(mat: List) -> tuple[int, UpperTriangularMatrix]:
    n = len(mat)
    coeff = 1

    # 右上三角化パート
    for i in range(n):
        # 要素[i][i]が非0な状況を作る
        if mat[i][i] == 0:
            pivot = search_pivot(mat, n, i)
            print(pivot)
            if pivot != -1:
                mat[i], mat[pivot] = mat[pivot], mat[i]
                # 符号を反転させておく
                if (pivot - i) % 2 == 1:
                    coeff = sub(0, coeff)
            else:
                continue

        # 要素[i][i]を非0にできれば、それより下を0にする
        for j in range(i+1, n):
            # j行目i列を0にする
            if mat[j][i] == 0:
                continue
            ratio = div(mat[j][i], mat[i][i])
            coeff = div(coeff, ratio)
            for k in range(n):
                mat[i][k] = mul(mat[i][k], ratio)
                mat[j][k] = sub(mat[j][k], mat[i][k])

    return coeff, UpperTriangularMatrix(mat)


def calc_det(mat, coeff):
    # 事前に上三角化されていること
    ret = 1
    for i in range(len(mat)):
        ret = mul(ret, mat[i][i])

    return mul(ret, coeff)


def det(mat: List) -> int:
    # 上三角行列化
    coeff, mat = det_upper_triangular(mat)

    return calc_det(mat, coeff)


def kirchhoffs_theorem(g: List) -> int:
    """
    行列木定理
    """
    n = len(g)
    mat = [[0 for i in range(n-1)] for j in range(n-1)]

    # 特殊な隣接行列を作る。
    # 後々余因子行列を求めるので、n列目とn行目はカットされている
    for i, v in enumerate(g):
        if i == n-1:
            break
        mat[i][i] = len(v)
        for adjasent in v:
            if adjasent == n-1:
                continue
            mat[i][adjasent] -= 1

    return det(mat)


def main():
    import os
    print(os.path.dirname(__file__))
    with open(os.path.dirname(__file__) + "/a.txt") as f:
        _ = f.readline()

        for s in f.readlines():
            print(s)


if __name__ == "__main__":
    main()
