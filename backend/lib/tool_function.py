def dfs(node, before_fun=None, after_fun=None):
    if type(node) == list:
        for child in node:
            dfs(child, before_fun, after_fun)
        return
    if before_fun is not None:
        before_fun(node)
    if 'children' in node:
        dfs(node['children'], before_fun, after_fun)
    if after_fun is not None:
        after_fun(node)
