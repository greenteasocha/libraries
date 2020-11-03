import random


class Node():
    def __init__(self, val, height=0, bias=0, left=None, right=None):
        self.val = val
        self.height = height
        self.bias = bias
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
        self._set_height(node)
        return self._valanced(node)

    def _set_height(self, node):
        # call this when either of children is chenged
        node.hl = 0 if not node.left else node.left.height + 1
        node.hr = 0 if not node.right else node.right.height + 1

        node.height = max(node.hl, node.hr)
        node.bias = node.hl - node.hr

    def _valanced(self, node):
        # be sure that node properties(height/bias) are updated by set_height
        if -1 <= node.bias <= 1:
            return node

        elif node.bias == 2:
            if node.left.bias in [0, 1]:
                return self._rotateR(node)
            elif node.left.bias == -1:
                return self._rotateLR(node)
            else:
                assert 0, 'Invalid subtree bias : ' + str(node.left.bias)

        elif node.bias == -2:
            if node.right.bias in [-1, 0]:
                return self._rotateL(node)
            elif node.right.bias == 1:
                return self._rotateRL(node)
            else:
                assert 0, 'Invalid subtree bias : ' + str(node.right.bias)

        else:
            assert 0, 'Invalid bias : ' + str(node.bias)

    def delete(self, x):
        # if x is not found, return False
        self.root, res = self._delete(self.root, x)
        return res

    def _delete(self, node, x):
        if node.val > x:
            if not node.left:
                return node, False
            else:
                l, res = self._delete(node.left, x)
                node.left = l
                res = False

        elif node.val < x:
            if not node.right:
                return node, False
            else:
                r, res = self._delete(node.right, x)
                node.right = r

        elif node.val == x:
            if not node.left:
                return node.right, True
            else:
                l, val = self._promote(node.left)
                res = True
                node.val = val

        self._set_height(node)
        return self._valanced(node), res

    def _promote(self, node):
        # find and promote max value of subtree
        if not node.right:  # max
            return node.left, node.val

        else:
            r, val_pro = self._promote(node.right)
            node.right = r

            self._set_height(node)
            return self._valanced(node), val_pro

    def _rotateR(self, node):
        n = node
        l = node.left
        lr = l.right

        l.right = n
        n.left = lr

        self._set_height(n)
        self._set_height(l)

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

        self._set_height(n)
        self._set_height(l)
        self._set_height(lr)

        return lr

    def _rotateL(self, node):
        n = node
        r = node.right
        rl = r.left

        r.left = n
        n.right = rl

        self._set_height(n)
        self._set_height(r)

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

        self._set_height(n)
        self._set_height(r)
        self._set_height(rl)

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
    # for i in range(10):
    #     tr.add(random.randint(1, 10))

    # tr.show_all()

    # delcn = 0
    # for i in range(5000):
    #     res = tr.delete(random.randint(1, 10))
    #     if res:
    #         delcn += 1

    # tr.show_all()

    # print(delcn)
    tr.add(1)
    tr.add(2)
    tr.add(3)
    tr.add(4)
    tr.add(5)
    tr.add(6)

    tr.show_all()
    # return?

    tr.delete(6)
    tr.delete(5)
    tr.delete(3)
    tr.show_all()
    return

    tr.delete()
    tr.delete()

    # tr.add(10)
    # tr.add(5)
    # tr.add(12)
    # tr.add(1)
    # tr.add(8)
    # tr.show_all()
    # tr.add(6)
    # tr.show_all()
    return


if __name__ == "__main__":
    main()
