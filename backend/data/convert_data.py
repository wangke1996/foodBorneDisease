import json


def convert_bugs():
    with open('bugs.json', 'r', encoding='utf8') as f:
        data = json.load(f)
    root = {'title': '病原微生物', 'key': '病原微生物', 'children': []}

    def dfs_convert(node, new_node):
        if type(node) == list:
            for child in node:
                dfs_convert(child, new_node)
            return
        assert type(node) == dict
        if '名称' in node:
            name = node['名称']
            new_node['children'].append({'title': name, 'key': name, 'detail': node, 'parent': new_node['key']})
        else:
            for name, children in node.items():
                new_child = {'title': name, 'key': name, 'children': [], 'parent': new_node['key']}
                new_node['children'].append(new_child)
                dfs_convert(children, new_child)

    dfs_convert(data, root)
    with open('bugs_coverted.json', 'w', encoding='utf8') as f:
        json.dump([root], f, ensure_ascii=False)


if __name__ == '__main__':
    convert_bugs()
