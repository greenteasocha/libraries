import sys
from typing import *

sys.setrecursionlimit(1000000)

# input aliases
input = sys.stdin.readline
getN = lambda: int(input())
getList = lambda: list(map(int, input().split()))


class Node(object):
    def __init__(self, parent=None, val=None):
        self.parent: Node = parent
        self.val: int = val

    # ============== DEBUG FUNCTIONS ================
    def all_pop(self):
        cur = self
        while True:
            if cur is None:
                break
            print(cur.val)
            cur = cur.pop()

    def all_show(self):
        # do not eval
        cur = self
        while True:
            if cur is None:
                break
            print(cur.val)
            cur = cur.parent

    # ============== END DEBUG FUNCTIONS ================

    def top(self) -> int:
        return self.val

    def pop(self):
        if self.parent:
            self.parent = self.parent.eval()
            return self.parent

    @staticmethod
    def push(x, v):
        return Node(x, v)

    def reverse(self):
        return ReversedNode(self.parent, self.val)

    @staticmethod
    def concat(x, y):
        if x is None:
            return y.eval()
        else:
            par = x.pop()
            return Node(TailConcatenatedNode(par, y),  x.val)

    def eval(self):
        return self


class ReversedNode(Node):
    def __init__(self, parent, val):
        super().__init__(parent, val)

    def eval(self):
        ret = None
        cur = self
        while cur:
            ret = Node(ret, cur.val)
            cur = cur.parent

        return ret


class TailConcatenatedNode(Node):
    def __init__(self, parent, tail):
        if parent is None:
            val = None
        else:
            val = parent.val
        super().__init__(parent, val)
        self.tail = tail

    def eval(self):
        return self.concat(self.pop(), self.tail)


class BankersQueue(object):
    def __init__(self, rear=None, rsize=0, front=None, fsize=0):
        self.rear = rear
        self.rsize = rsize
        self.front = front
        self.fsize = fsize

    def top(self):
        return self.front.top()

    def pop(self):
        ret = BankersQueue(self.rear, self.rsize, self.front.pop(), self.fsize - 1)
        return ret.normalize()

    def push(self, v):
        ret = BankersQueue(Node.push(self.rear, v), self.rsize + 1, self.front, self.fsize)
        return ret.normalize()

    def normalize(self):
        if self.rsize > self.fsize:
            return BankersQueue(None, 0, Node.concat(self.front, self.rear.reverse()), self.rsize + self.fsize)
        else:
            return self


def main():
    q = getN()
    root = BankersQueue()
    queue_t: List[BankersQueue] = [root]

    for i in range(q):
        type, *args = getList()
        if type == 0:
            t, v = args
            t += 1
            queue_t.append(queue_t[t].push(v))
        else:
            t = args[0]
            t += 1
            queue_t.append(queue_t[t].pop())
            print(queue_t[t].top())



if __name__ == "__main__":
    main()