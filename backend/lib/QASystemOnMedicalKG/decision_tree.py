from py2neo import Graph
from collections import Counter

from . import *
#from question_parser import QuestionPaser

tree_dims = {'result_from': 'food',
             'disease_symptom': 'symptom', 'has_time': 'time', }


class DecisionTree:
    def __init__(self, desc, root_symptom):
        self.g = Graph("http://localhost:7474", auth=("neo4j", "ohahaha"))
        self.parser = QuestionPaser()
        self.root_symptom = root_symptom
        self.num_limit = 5
        self.tree_dict = {}
        self.desc = desc
        self.last_question = {'question_dim': '', 'candidates': []}

    def build(self):

        # todo: 仅针对 症状-疾病

        for question_dim in list(tree_dims.keys()):
            self.tree_dict[question_dim] = {i: [] for i in self.desc}
            queries = self.parser.sql_transfer(question_dim, self.desc)
            for query in queries:
                result = self.g.run(query).data()
                for answer in result:
                    self.tree_dict[question_dim][answer['m.name']].append(
                        answer['n.name'])


    def ask(self):
        links = {i: [] for i in self.desc}
        if self.tree_dict:
            
            question_dim = list(self.tree_dict.keys())[0]
            ask_dict = self.tree_dict[question_dim]
            if not self.last_question['candidates']:
                candidates = []
                for d in self.desc:
                    candidates += ask_dict[d]
                candi_counter= Counter(candidates)
                candidates = list(set(candidates))
                for r_s in self.root_symptom:
                    if r_s in candidates:
                        candidates.remove(r_s)
                def sort_by_count(i):
                    return candi_counter[i]
                candidates.sort(key=sort_by_count,reverse=True)
            else:
                candidates = self.last_question['candidates']

            candi_to_ask = candidates[:self.num_limit]
            candidates = candidates[self.num_limit:] if len(
                candidates) > self.num_limit else []
            for d in self.desc:
                for nature in ask_dict[d]:
                    if nature != self.root_symptom and nature in candi_to_ask:
                        links[d].append(nature)

            self.last_question['question_dim'] = question_dim
            self.last_question['candidates'] = candidates
            self.last_question['candi_to_ask'] = candi_to_ask

            answer = self.ask_wrapper(question_dim)
            for i, wd in enumerate(candi_to_ask):
                answer += (' '+str(i+1)+'.'+wd)
            answer += " {}.其他".format(self.num_limit+1) if candidates else ""
            question_info = {'answer': answer, 'nature_entities': candi_to_ask, 'nature_entity_type': tree_dims[question_dim],
                            'q_type': question_dim, 'links': links}

            return question_info
        else:
            question_info = {'nature_entities': [],'links': links}
            
            return question_info

    def ask_wrapper(self, q_type):
        answer = "请回复数字或点击图谱中的节点\n"
        if q_type == "result_from":
            answer += "最近是否吃了以下食物？\n"

        if q_type == "has_time":
            answer += "距离用餐多久了呢？\n"

        if q_type == "disease_symptom":
            answer += "是否还有以下症状？\n"

        return answer

    def update(self, result):

        if result == self.num_limit+1 or result == "其他":
            del_list = self.last_question['candi_to_ask']
            return del_list
        else:          
            candi = result
            question_dim = self.last_question['question_dim']
            print(question_dim)
            self.last_question = {'question_dim': '', 'candidates': []}
            q_dict = self.tree_dict[question_dim]
            print(self.tree_dict)
            print(q_dict)
            del_list = []
            print(candi)
            # 对于当前question_dim 未命中且属性不为空的删除
            for disease in self.desc:
                if (q_dict[disease]) and (candi not in q_dict[disease]):
                    del_list.append(disease)
                print(disease, q_dict[disease])
   
            for del_disease in del_list:
                self.desc.remove(del_disease)

            del self.tree_dict[question_dim]
            return del_list

    def reply(self, result):
        
        del_list = self.update(result)
        
        # 默认：继续提问
        next_state = "Questioning"
        
        # 结束条件1 剩唯一答案
        if len(self.desc) == 1:
            next_state = "Waiting"
            answer = self.reply_wrapper(self.desc)
            question_info = {'answer': answer, 'nature_entities': [], 'nature_entity_type': '',
                             'q_type': '', 'links': {}, 'result': self.desc}
            return next_state, del_list, question_info
        print(self.desc)
        # 结束条件2 无候选答案
        if len(self.desc) == 0:
            next_state = "Waiting"
            answer = "未能找到答案"
            question_info = {'answer': answer, 'nature_entities': [], 'nature_entity_type': '',
                             'q_type': '', 'links': {},'result': self.desc}
            return next_state, del_list, question_info
        print(self.desc)
        question_info = self.ask()
        # 结束条件3 有候选答案，但无法生成决策树：返回所有可能答案
        print(self.desc,question_info['nature_entities'])
        if not question_info['nature_entities']:
            next_state = "Waiting"
            answer = self.reply_wrapper(self.desc)
            question_info['answer'] = answer
            question_info['result'] = self.desc
        return next_state, del_list, question_info

    def reply_wrapper(self, desc: list):
        return "您好，您的情况可能是"+'或'.join(desc)+"感染导致的，请参阅本系统中"+'和'.join(desc)+"相关知识。"



        