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

    def push(self, v):
        return Node(self, v)

    def reverse(self):
        return ReversedNode(self, None)

    @staticmethod
    def concat(x, y):
        if x.val is None:
            return y.eval()
        else:
            return Node(TailConcatenatedNode(x.parent, x.parent.val, y),  x.val)

    def eval(self):
        return self


class ReversedNode(Node):
    def __init__(self, parent, val):
        super().__init__(parent, val)

    def eval(self):
        ret = None
        par = self.parent
        while par.val:
            ret = Node(ret, par.val)
            par = par.parent

        return ret


class TailConcatenatedNode(Node):
    def __init__(self, parent, val, tail):
        super().__init__(parent, val)
        self.tail = tail

    def eval(self):
        return self.concat(self.pop(), self.tail)


class BankersQueue(object):
    def __init__(self, rear=Node(), rsize=0, front=Node(), fsize=0):
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
        ret = BankersQueue(self.rear.push(v), self.rsize + 1, self.front, self.fsize)
        return ret.normalize()

    def normalize(self):
        if self.rsize > self.fsize:
            return BankersQueue(Node(), 0, Node.concat(self.front, Node.reverse(self.rear)), self.rsize + self.fsize)
        else:
            return self


def main():
    # a0 = Node(None, 0)
    # a1 = a0.push(1)
    # a2 = a1.push(2)
    # a3 = a2.push(3)
    # a4 = a3.push(4)
    # a5 = a4.reverse()
    #
    # # a6 = a5.push(10)
    # # a6.all_pop()
    #
    # a10 = Node(None, 10)
    # a11 = a10.push(11)
    # a12 = a11.push(12)
    # a13 = a12.push(13)
    # a14 = a13.push(14)
    #
    # a20 = Node.concat(a4, a5)
    # a21 = Node.concat(a20, a14)
    # a20.all_pop()

    q = getN()
    root = BankersQueue()
    # a1 = root.push(10)
    queue_t: List[BankersQueue] = [root]

    for i in range(q):
        type, *args = getList()
        if type == 0:
            t, v = args
            t += 1
            queue_t.append(queue_t[t].push(v))
        else:
            t = args[0]
            # print(t)
            t += 1
            print(queue_t[t].top())
            queue_t.append(queue_t[t].pop())


if __name__ == "__main__":
    main()