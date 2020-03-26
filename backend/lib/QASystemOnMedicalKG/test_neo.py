from py2neo import Graph
import random
from . import *
#from question_parser import QuestionPaser

tree_dims = {'result_from':'food', 'disease_symptom':'symptom','has_time':'time', }

class DecisionTree:
    def __init__(self, desc, root_symptom):
        self.g = Graph("http://localhost:7474", auth=("neo4j", "ohahaha"))
        self.parser = QuestionPaser()
        self.root_symptom=root_symptom
        self.num_limits = 5
        self.tree_dict = {}
        self.desc =list(desc.items())[0][1]
        self.last_question = {'question_dim': 0, 'total_candidates': 0,'ask_candidates':0}
        self.candidates_asked = {}

    def build(self):

        # todo: 仅针对 症状-疾病


        
        for question_dim in list(tree_dims.keys()):
            self.candidates_asked[question_dim] = []
            self.tree_dict[question_dim] = {i: [] for i in self.desc}
            queries = self.parser.sql_transfer(question_dim, self.desc)
            for query in queries:
                result = self.g.run(query).data()
                for answer in result:
                    self.tree_dict[question_dim][answer['m.name']].append(
                        answer['n.name'])
        print(self.tree_dict)

    def ask(self):
        num_ask = 8
        if self.tree_dict:
            if not self.last_question['total_candidates']:
                question_dim = list(self.tree_dict.keys())[0]
                ask_dict = self.tree_dict[question_dim]
                candidates = []
                for d in self.desc:
                    candidates += ask_dict[d]
                random.shuffle(list(set(candidates)))
                if self.root_symptom in candidates:
                    candidates.remove(self.root_symptom)
               
            else:
                question_dim = self.last_question['question_dim']
                candidates = self.last_question['total_candidates']
                ask_dict = self.tree_dict[question_dim]
            candi_for_ask = candidates[0:num_ask]
            for i in candi_for_ask:
                candidates.remove(i)      
            self.last_question['question_dim'] = question_dim
            self.last_question['total_candidates'] = candidates
            self.last_question['ask_candidates'] = candi_for_ask

            answer = self.ask_wrapper(question_dim)
            for i, wd in enumerate(candidates):
                answer += (str(i+1)+'.'+wd)

            links = {i: [] for i in self.desc}
            for d in self.desc:
                for nature in ask_dict[d]:
                    if nature in candi_for_ask:
                        links[d].append(nature)

            question_info = {'answer': answer, 'nature_entities':candi_for_ask, 'nature_entity_type': tree_dims[question_dim],
                             'q_type': question_dim, 'links': links}
            print("d_tree_response"+str(question_info))
            return question_info

        else:
            return 0

    def ask_wrapper(self, q_type):
        answer = "请回复数字\n"
        if q_type == "result_from":
            answer += "最近是否吃了以下食物？\n"

        if q_type == "has_time":
            answer += "距离用餐多久了呢？\n"

        if q_type == "disease_symptom":
            answer += "是否还有以下症状？\n"

        return answer

    def update(self, result):
        candi = self.last_question['ask_candidates'][result-1]
        question_dim = self.last_question['question_dim']
        q_dict = self.tree_dict[question_dim]
        del_list = []
        # 对于当前question_dim 未命中且属性不为空的删除
        for disease in self.desc:
            if (q_dict[disease]) and (candi not in q_dict[disease]):
                del_list.append(disease)
        for del_disease in del_list:
            self.desc.remove(del_disease)
        if not self.last_question['total_candidates']:
            del self.tree_dict[question_dim]
        return del_list
        

    def reply(self, result):
        del_list = self.update(result)
        # 默认：继续提问
        next_state = "Questioning"
        print(self.desc)
        # 结束条件1 剩唯一答案
        if len(self.desc) == 1:
            next_state = "Waiting"
            answer = self.reply_wrapper(self.desc)
            question_info = {'answer': answer, 'nature_entities': [], 'nature_entity_type': '',
                             'q_type':'' , 'links': {},'result' : self.desc}
            return next_state, del_list ,question_info
        # 结束条件2 无候选答案
        if len(self.desc) == 0:
            next_state = "Waiting"
            answer = "未能找到答案"
            question_info = {'answer': answer, 'nature_entities': [], 'nature_entity_type': '',
                             'q_type':'' , 'links': {}}
            return  next_state, del_list ,question_info

        question_info = self.ask()
        # 结束条件3 有候选答案，但无法生成决策树：返回所有可能答案

        if not question_info['nature_entities']:
            next_state = "Waiting"
            answer = self.reply_wrapper(self.desc)
            question_info['answer'] = answer
            question_info['result'] = self.desc
        return next_state, del_list , question_info

    def reply_wrapper(self, desc: list):
        
        return "您好，您的情况可能是"+'或'.join(desc)+"感染导致的，请参阅本系统中"+'和'.join(desc)+"相关知识。"
