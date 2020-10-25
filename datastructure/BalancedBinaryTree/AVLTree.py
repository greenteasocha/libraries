class Node():
    def __init__(self, val):
        self.val = val
        self.parent = None
        self.left = None
        self.right = None


class AVLTree():
    def __init__(self, root):
        self.root = Node(root)

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
        return self._add(self.root, Node(x))

    def _add(self, node, target_node):
        if target_node.val <= node.val:
            if node.left:
                self._add(node.left, target_node)
            else:
                node.left = target_node
                target_node.parent = node
        elif target_node.val > node.val:
            if node.right:
                self.add_(node.right, target_node)
            else:
                node.right = target_node
                target_node.parent = node
        else:
            assert 0

        # balance check
        dl = 1 if not node.left else node.left.height + 1
        dr = 1 if not node.right else node.right.height + 1

        if dl > dr + 1:

    def delete(self, x):
        pass

    def _rotate_r(self, node):
        n = node
        p = node.parent
        c = node.left
        node.left = c.right
        c.right = node
        p.


def main():
    tr = AVLTree(10)

    print(tr.find(10))
    print(tr.find(9))

    tr.add(9)
    print(tr.find(10))
    print(tr.find(9))

    return


if __name__ == "__main__":
    main()
