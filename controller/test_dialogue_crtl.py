# 测试流程
# 构建多叉树
# 定义流程图，使用邻接表表示
graph = {'A': ['B', 'C'],
         'B': ['D', 'E'],
         'C': ['F'],
         'D': [],
         'E': ['F'],
         'F': []}


# 定义 DFS 函数
def dfs(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        print(path)
    for node in graph[start]:
        if node not in path:
            dfs(graph, node, end, path)


def generate():
    # 测试 DFS 函数
    start_node = 'A'
    end_node = 'F'
    dfs(graph, start_node, end_node)


if __name__ == '__main__':
    generate()
    pass
