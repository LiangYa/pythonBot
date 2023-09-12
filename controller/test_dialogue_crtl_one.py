class Node:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.children = []

    def add_child(self, node):
        self.children.append(node)


def print_all_usernames(node, path):
    path.append(node.username)
    if len(node.children) == 0:
        print(' -> '.join(path))
    else:
        for child in node.children:
            print_all_usernames(child, path)
    path.pop()


def getTest():
    root = Node('root', 'password')
    node1 = Node('user1', 'password')
    node2 = Node('user2', 'password')
    node3 = Node('user3', 'password')

    root.add_child(node1)
    root.add_child(node2)
    node1.add_child(node3)

    print_all_usernames(root, [])


if __name__ == '__main__':
    getTest()
    pass
