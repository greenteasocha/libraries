import sys
import random
from collections import deque

input = sys.stdin.readline
getS = lambda: input().strip()
getN = lambda: int(input())
getList = lambda: list(map(int, input().split()))
getZList = lambda: [int(x) - 1 for x in input().split()]


class SCC():
    def __init__(self, graph):
        """
        :param graph: adjacency list (0-indexed)
            ex:[[1, 2], [0, 2], [0, 1]] <- bidirectional complete graph(n=3)
        """
        self.graph = graph
        # print(self.labeling())
        self.scc = self.make_scc(self.make_rev_graph(), self.labeling())

    def make_rev_graph(self):
        ret = [[] for i in range(len(self.graph))]
        for i, x in enumerate(self.graph):
            for j in x:
                ret[j].append(i)

        return ret

    def labeling(self):
        n = len(self.graph)
        used = [0] * n
        label_order_vertexes = []
        for i in range(0, n):
            if used[i]:
                continue
            q = deque()  # [order, vertex] if order == 1: pre-order else: post-order
            q.append((1, i))
            while q:
                order, vertex = q.pop()
                if order == 1:
                    if used[vertex]:
                        continue
                    used[vertex] = 1
                    q.append((2, vertex))
                    for nx in self.graph[vertex]:
                        if not used[nx]:
                            q.append((1, nx))


                else:
                    label_order_vertexes.append(vertex)

        return label_order_vertexes

    def make_scc(self, graph, order):
        n = len(self.graph)
        used = [0] * n
        ret = []
        for i in reversed(order):
            if used[i]:
                continue
            tmp_set = []
            q = deque()
            q.append(i)
            used[i] = 1
            while q:
                vertex = q.pop()
                tmp_set.append(vertex)
                for nx in graph[vertex]:
                    if not used[nx]:
                        q.append(nx)
                        used[nx] = 1
            ret.append(tmp_set)

        return ret


def main():
    # submission for "Typical90 #21"
    # https://atcoder.jp/contests/typical90/tasks/typical90_u

    n, m = getList()
    g = [[] for i in range(n)]
    for i in range(m):
        a, b = getZList()
        if a == b:  # remove self loop
            continue
        g[a].append(b)

    g = [list(set(v)) for v in g]  # remove multiple edges
    scc = SCC(g)

    ans = 0
    for v_set in scc.scc:
        l = len(v_set)
        ans += (l * (l-1)) // 2

    print(ans)


def ran(n):
    li = [i for i in range(n)]
    lil = [random.choice(li) for i in range(2)]

    return lil


if __name__ == "__main__":
    main()
