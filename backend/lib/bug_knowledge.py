from backend.lib.config import CONFIG
from backend.lib.data_helper import load_json
from backend.lib.tool_function import dfs


class BugKnowledge(object):
    def split_menu_and_detail(self, bugs):
        detail = {}

        def fun(node: dict):
            if 'detail' in node:
                detail[node['key']] = node['detail']
                node.pop('detail')

        dfs(bugs, fun)
        menu = bugs
        return menu, detail

    def __init__(self):
        bugs = load_json(CONFIG.bugs_converted_json)
        self.menu, self.detail = self.split_menu_and_detail(bugs)

    def get_bugs(self):
        return self.menu

    def get_detail(self, bug_key):
        return self.detail.get(bug_key, {})


KNOWLEDGE = BugKnowledge()
