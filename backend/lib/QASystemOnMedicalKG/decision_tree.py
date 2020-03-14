from py2neo import Graph
from . import *
# from question_parser import QuestionPaser


class DecisionTree:
    def __init__(self, desc):
        self.g = Graph("http://localhost:7474", auth=("neo4j", "ohahaha"))
        self.parser = QuestionPaser()
        self.num_limits = 20
        self.tree_dict = {}
        self.desc = desc
        self.last_question = {'question_type': 0, 'candidates': 0}

    def build(self):

        if not self.tree_dict:
            tree_dims = ['result_from','has_time', ]
            for question_type in tree_dims:
                self.tree_dict[question_type] = {i: [] for i in self.desc}
                queries = self.parser.sql_transfer(question_type, self.desc)
                for query in queries[:self.num_limits]:
                    result = self.g.run(query).data()
                    for answer in result:
                        self.tree_dict[question_type][answer['m.name']].append(
                            answer['n.name'])
            print(self.tree_dict)

    def ask(self):
        if self.tree_dict:
            question_type = list(self.tree_dict.keys())[0]
            ask_dict = self.tree_dict[question_type]
            candidates = []
            for d in self.desc:
                candidates += ask_dict[d]
            candidates = list(set(candidates))
            self.last_question['question_type'] = question_type
            self.last_question['candidates'] = candidates
            print(question_type)
            answer = self.ask_wrapper(question_type)
            for i,wd in enumerate(candidates):
                answer+=(str(i+1)+'.'+wd)
            return answer

        else:
            return 0
    
    def ask_wrapper(self,q_type):
        answer = "请回复数字\n"
        if q_type =="result_from":
            answer +="最近是否吃了一下食物？\n"

        if q_type =="has_time":
            answer +="距离用餐多久了呢？\n"

        return answer
            

    def update(self, result):
        candi = self.last_question['candidates'][result-1]
        question_type = self.last_question['question_type']
        q_dict = self.tree_dict[question_type]
        del_list = []
        # 对于当前question_type 未命中且属性不为空的删除
        for disease in self.desc:
            if (q_dict[disease]) and (candi not in q_dict[disease]):
                del_list.append(disease)
        for del_disease in del_list:
            self.desc.remove(del_disease)
        del self.tree_dict[question_type]
        print(candi,del_list,self.desc, self.tree_dict)
    
    def reply(self,result):
        self.update(result)
        # 默认：继续提问
        next_state = "Questioning"

        # 结束条件1 剩唯一答案
        if len(self.desc) ==1 :
            next_state = "Answering"
            answer = self.reply_wrapper(self.desc)       
            return next_state,answer
        # 结束条件2 无候选答案
        if len(self.desc) ==0 :
            next_state = "Answering"
            answer = "未能找到答案"       
            return next_state,answer

        answer = self.ask()
        # 结束条件3 有候选答案，但无法生成决策树：返回所有可能答案
        if not answer:
            next_state = "Answering"
            answer = self.reply_wrapper(self.desc)
        return next_state,answer


    def reply_wrapper(self,desc:list):
        return "可能为"+'或'.join(desc)+"引起的疾病" 