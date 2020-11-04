import random
INF = 1 << 32 - 1


class Node():
    def __init__(self, val, height=0, bias=0, size=1, left=None, right=None):
        self.val = val
        self.height = height
        self.bias = bias
        self.size = size
        self.left = left
        self.right = right


class AVLTree():
    def __init__(self, root=None):
        if root:
            self.root = Node(root)
        else:
            self.root = None

    def find(self, x):
        return self._find(x, self.root)

    def _find(self, x, node):
        v = node.val
        if v == x:
            return x
        elif v > x:
            if node.left:
                return self._find(x, node.left)
            else:
                return False
        elif v < x:
            if node.right:
                return self._find(x, node.right)
            else:
                return False
        else:
            assert 0

    def add(self, val):
        if not self.root:
            self.root = Node(val)
            return

        node_hist = []
        side_hist = []  # left if side == 1 else right

        node_current = self.root
        while True:
            if val <= node_current.val:
                node_hist.append(node_current)
                side_hist.append(1)
                if node_current.left:
                    node_current = node_current.left
                else:
                    break
            else:
                node_hist.append(node_current)
                side_hist.append(-1)
                if node_current.right:
                    node_current = node_current.right
                else:
                    break

        node_child = Node(val)

        while node_hist:
            node_parent = node_hist.pop()
            side = side_hist.pop()

            if side == 1:
                node_parent.left = node_child
            elif side == -1:
                node_parent.right = node_child
            else:
                assert 0, "Invalid side value (in add)"

            self._update_property(node_parent)
            node_child = self._valanced(node_parent)

        self.root = node_child
        return

    def deleter(self, x):
        self.root = self._delete(self.root, x)

    def delete(self, val):
        node_hist = []
        side_hist = []  # left if side == 1 else right

        node_current = self.root
        while True:
            if val < node_current.val:
                node_hist.append(node_current)
                side_hist.append(1)
                if node_current.left:
                    node_current = node_current.left
                else:
                    return

            elif val > node_current.val:
                node_hist.append(node_current)
                side_hist.append(-1)
                if node_current.right:
                    node_current = node_current.right
                else:
                    return

            elif val == node_current.val:
                if node_current.left:
                    node_child = self._promote(node_current)
                else:
                    node_child = node_current.right
                break

        while node_hist:
            node_parent = node_hist.pop()
            side = side_hist.pop()

            if side == 1:
                node_parent.left = node_child
            elif side == -1:
                node_parent.right = node_child
            else:
                assert 0, "Invalid side value (in add)"

            self._update_property(node_parent)
            node_child = self._valanced(node_parent)

        self.root = node_child
        return

    def _promote(self, node):
        node_hist = []

        node_current = node
        while True:
            if not node_current.right:
                node_child = node_current.left
                break

            else:
                node_hist.append(node_current)
                node_current = node_current.right

        while node_hist:
            node_parent = node_hist.pop()
            node_parent.right = node_child

            self._update_property(node_parent)
            node_child = self._valanced(node_parent)

        return node_child

    def _promoter(self, node):
        # find and promote max value of subtree
        if not node.right:  # max
            return node.left, node.val

        else:
            r, val_pro = self._promote(node.right)
            node.right = r

            self._update_property(node)
            return self._valanced(node), val_pro

    def kth(self, k):
        # k-th smallest value
        if self.root.size < k:
            return INF

        node_current = self.root

        while True:
            sl = 0 if not node_current.left else node_current.left.size
            if sl == k - 1:
                return node_current.val

            elif sl > k - 1:
                node_current = node_current.left

            else:
                k -= sl + 1
                node_current = node_current.right

    def _update_property(self, node):
        # call this when either of children are changed
        hl = node.left.height if node.left else 0
        hr = node.right.height if node.right else 0

        sl = node.left.size if node.left else 0
        sr = node.right.size if node.right else 0

        node.height = max(hl, hr) + 1
        node.bias = hl - hr
        node.size = sl + sr + 1

    def _valanced(self, node):
        # be sure that node properties(height/bias) are updated by update_property
        bias = node.bias
        if -1 <= bias <= 1:
            return node

        elif bias == 2:
            bias_l = node.left.bias
            if bias_l == 0 or bias_l == 1:
                return self._rotateR(node)
            elif bias_l == -1:
                return self._rotateLR(node)
            else:
                assert 0, 'Invalid subtree bias : ' + str(node.left.bias)

        elif bias == -2:
            bias_r = node.right.bias
            if bias_r == -1 or bias_r == 0:
                return self._rotateL(node)
            elif bias_r == 1:
                return self._rotateRL(node)
            else:
                assert 0, 'Invalid subtree bias : ' + str(node.right.bias)

        else:
            assert 0, 'Invalid bias : ' + str(node.bias)

    def _rotateR(self, node):
        n = node
        l = node.left
        lr = l.right

        l.right = n
        n.left = lr

        self._update_property(n)
        self._update_property(l)

        return l

    def _rotateLR(self, node):
        n = node
        l = node.left
        lr = l.right
        lrl = lr.left
        lrr = lr.right

        l.right = lrl
        n.left = lrr
        lr.left = l
        lr.right = n

        self._update_property(n)
        self._update_property(l)
        self._update_property(lr)

        return lr

    def _rotateL(self, node):
        n = node
        r = node.right
        rl = r.left

        r.left = n
        n.right = rl

        self._update_property(n)
        self._update_property(r)

        return r

    def _rotateRL(self, node):
        n = node
        r = node.right
        rl = r.left
        rlr = rl.right
        rll = rl.left

        r.left = rlr
        n.right = rll
        rl.right = r
        rl.left = n

        self._update_property(n)
        self._update_property(r)
        self._update_property(rl)

        return rl

    def show_all(self):
        print("===================")
        self._show_all(self.root, 0)
        print("===================")

        return

    def _show_all(self, node, depth):
        if node.right:
            self._show_all(node.right, depth + 1)

        print("   " * depth, node.val)  # , node.bias, node.height)

        if node.left:
            self._show_all(node.left, depth + 1)


def main():
    tr = AVLTree()
    for i in range(1, 17):
        tr.add(i)
    # tr.add(11)
    # tr.add(29)
    # tr.add(89)
    # tr.add(99)
    for i in range(1, 8):
        tr.delete(i)

    tr.show_all()

    for i in range(13, 20):
        tr.delete(i)

    tr.show_all()
    ans = tr.kth(2)
    print(ans)
    # tr.delete(ans)
    # tr.show_all()
    return


if __name__ == "__main__":
    main()
