import random
from typing import *

    
def MP(s: str) -> List:
    """
    :param s: (ex: aabaabaaa)
    :return: (ex:  [-1,0,1,0,1,2,3,4,5,2])
    """
    ret = [-1]
    j = -1
    for i, c in enumerate(s):
        while j >= 0 and s[j] != c:
            j = ret[j]
        j += 1
        ret.append(j)

    return ret


def str_search(target: str, query: str) -> List:
    """
    :param target: (ex: "abcabcd)
    :param query:  (ex: "abcd")
    :return:       (ex: [0,0,0,1,0,0,0])
    """
    ln, lm = len(target), len(query)
    ret = [0] * ln
    border = MP(query)
    j = 0
    for i, c in enumerate(target):
        if j == -1:
            j = 0
        while j >= 0:
            if c == query[j]:
                if j == lm-1:
                    ret[i-lm+1] = 1
                    j = border[-1]
                else:
                    j += 1
                break

            else:
                j = border[j]

    return ret


def test():
    # =====================================================================
    # test_handmade
    testcase = [
        ["aaaa", "a", [1,1,1,1]],
        ["abab", "ab", [1,0,1,0]],
        ["aabaaab", "aab", [1,0,0,0,1,0,0]],
        ["abceabcdabcdabce", "abcd", [0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0]]
    ]

    for target, query, expect in testcase:
        res = str_search(target, query)
        if res == expect:
            print("OK")
        else:
            print(res)

    # =====================================================================
    # random_generated
    target = "".join([random.choice(["1", "0"]) for i in range(100)])
    query = "".join([random.choice(["1", "0"]) for i in range(3)])

    res = str_search(target, query)

    # check
    flag = True
    for i in range(0, len(target) - len(query) + 1):
        cut = target[i:i+len(query)]
        if res[i]:
            if cut != query:
                flag = False
                print(cut, query, i)
        else:
            if cut == query:
                flag = False
                print(cut, query, i)

    if flag:
        print("OK")
    else:
        print(target)
        print(query)
        print(res)


if __name__ == "__main__":
    test()
