class Tree(object):
    def __init__(self, data=None, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

    def inorder(self):
        if self.left:
            for x in self.left.inorder():
                yield x

        yield self

        if self.right:
            for x in self.right.inorder():
                yield x

    def __iter__(self):
        return self.inorder()

    def __repr__(self, level=0, indent='    '):
        s = level * indent + self.data

        if self.left:
            s = f'{s}\n{self.left.__repr__(level+1, indent)}'

        if self.right:
            s = f'{s}\n{self.right.__repr__(level+1, indent)}'

        return s

def tree(List):
    n = len(List)

    if n == 0:
        return None

    i = n / 2

    return Tree(List[i], tree(List[:i]), tree(List[i + 1:]))


if __name__ == '__main__':
    t = tree('abcdef')

    print(t)
    print()

    for el in t.inorder():
        print(el.data)
