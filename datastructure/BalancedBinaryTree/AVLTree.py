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

    def add(self, x):
        if not self.root:
            self.root = Node(x)
            return

        self.root = self._add(self.root, Node(x))

    def _add(self, node, target_node):
        if target_node.val <= node.val:
            if node.left:
                node.left = self._add(node.left, target_node)
            else:
                node.left = target_node
        elif target_node.val > node.val:
            if node.right:
                node.right = self._add(node.right, target_node)
            else:
                node.right = target_node
        else:
            assert 0

        # balance check
        self._update_property(node)
        return self._valanced(node)

    def delete(self, x):
        self.root = self._delete(self.root, x)

    def _delete(self, node, x):
        if node.val > x:
            if not node.left:
                return node
            else:
                l = self._delete(node.left, x)
                node.left = l

        elif node.val < x:
            if not node.right:
                return node
            else:
                r = self._delete(node.right, x)
                node.right = r

        elif node.val == x:
            if not node.left:
                return node.right
            else:
                l, val = self._promote(node.left)
                node.val = val
                node.left = l

        self._update_property(node)
        return self._valanced(node)

    def kth(self, k):
        # k-th smallest value
        if self.root.size < k:
            return INF

        return self._kth(self.root, k)

    def _kth(self, node, k):
        sl = 0 if not node.left else node.left.size
        if sl == k - 1:
            return node.val

        elif sl > k - 1:
            return self._kth(node.left, k)

        else:
            return self._kth(node.right, k - sl - 1)

    def _promote(self, node):
        # find and promote max value of subtree
        if not node.right:  # max
            return node.left, node.val

        else:
            r, val_pro = self._promote(node.right)
            node.right = r

            self._update_property(node)
            return self._valanced(node), val_pro

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
    tr.add(11)
    tr.add(29)
    tr.add(89)

    tr.show_all()
    ans = tr.kth(2)
    print(ans)
    tr.delete(ans)
    tr.show_all()
    return


if __name__ == "__main__":
    main()
