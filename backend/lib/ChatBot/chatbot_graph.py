# bert-serving-start -model_dir F:\learn\ngnlab\KG\chinese_L-12_H-768_A-12\chinese_L-12_H-768_A-12 -pooling_layer=-11
import re
from collections import Counter
# 设置默认文件编码utf8
import _locale
# from answer_search import *
# from decision_tree import *
# from question_classifier import *
# from question_parser import *
import copy
from . import *

_locale._getdefaultlocale = (lambda *args: ['en_US', 'utf8'])


dialog_state_table = ["Waiting", "Questioning", "SynonymQuestioning"]
q_type_father_children = ['disease_symptom', 'result_from', 'disease_easyget']
q_type_show ={'disease_symptom':"导致",'result_from' :"来源",'has_time':"发病",'symptom_disease':"导致",'disease_easyget':"易感"}


class RobotRespond:
    def __init__(self):
        self.dialog_state = dialog_state_table[0]
        self.classifier = QuestionClassifier()
        self.parser = QuestionPaser()
        self.searcher = AnswerSearcher()
        self.last_question = ""
        self.response = {'answer': '', 'result': '',
                         'graph': {'nodes': [],  'links': [],'last_question_candi':[]}}
        self.false_response = {'answer': '我没能理解你的问题', 'result': '',
                         'graph': {'nodes': [],  'links': [],'last_question_candi':[]}}
        self.origin_q_type = ''
        self.origin_entity = ''

    def system_main(self, sent):

        if self.dialog_state == "Waiting":
            return self.get_answer(sent)

        elif self.dialog_state == "Questioning":
            # sent  --> int or list

            if str.isdigit(sent) and int(sent)< self.decision_tree.num_limit+1:
                msg = self.response['last_question_candi'][int(sent)-1]
            elif  sent in  self.response['last_question_candi']:
                msg = sent
            elif str.isdigit(sent) and int(sent) == len( self.response['last_question_candi'])+1:
                msg  = "其他"
            else:
                temp_response = copy.deepcopy(self.response)
                temp_response['answer'] = '请正确输入\n'+temp_response['answer']
                return temp_response

            self.dialog_state, del_entity_list, question_info = self.decision_tree.reply(
                    msg)

            print(self.dialog_state, del_entity_list, question_info)
                # 更新response_graph
                # 增加新节点及链接
            for link in self.response['graph']['links']:
                link['new'] = False
            for node in self.response['graph']['nodes']:
                node['new'] = False
                node['candidate'] = False
            self.add_graph_entity(question_info)
            # 删除排除节点及链接

            self.del_graph_entity(del_entity_list)

            if self.dialog_state == "Waiting":
                temp_response = self.response
                temp_response['result'] = question_info['result']
                self.system_reset()

                return temp_response

            else:
                print(self.response)
                temp_response = copy.deepcopy(self.response)
                temp = []
                for link in temp_response['graph']['links']:
                    temp.append(link['source'])
                    #temp.append(link['target'])
                temp =Counter(temp)
                print(temp)
                for k,v in temp.items():
                    if v ==1:
                        for n in temp_response['graph']['nodes']:
                            if n['id']==k and n['group']=='disease':
                                temp_response['graph']['nodes'].remove(n)
                        for link in temp_response['graph']['links']:   
                            if (link['source']==k) or (link['target']==k):
                                temp_response['graph']['links'].remove(link)
                return  temp_response 



        elif self.dialog_state == "SynonymQuestioning":
            # 将模糊实体替换后重新回答
            self.dialog_state == "Waiting"
            if str.isdigit(sent) and int(sent)<= len(self.classifier.TopScores):
                ori_question = self.classifier.origin_question
                ori_entity = self.classifier.TopScores[int(sent)-1][0]
                true_entity = self.classifier.TopScores[int(sent)-1][2]
                return self.get_answer(ori_question.replace(ori_entity,true_entity))
            else:
                self.system_reset()
                return self.false_response

    def get_answer(self, sent):

        self.dialog_state, res_classify = self.classifier.classify(sent)
        print("res_classify"+str(res_classify))

        #  问题分类 实体抽取中模糊表达
        if self.dialog_state == "SynonymQuestioning":
            self.response['answer'] = res_classify['answer']
            self.response['candi_synonym'] = res_classify['candi_synonym']
            return self.response

       # 无分类结果
        if not res_classify['question_types']:
            self.system_reset()
            return self.false_response

        # 保存实体抽取结果
        self.origin_q_type = res_classify['question_types']
        self.origin_entity_type = list(res_classify['entities'].items())[0][1]

        

        # 查询构造
        res_sql = self.parser.parser_main(res_classify)
        print("res_sql:"+str(res_sql))
        self.dialog_state, result,final_answers,answer_entity_type, links = self.searcher.search_main(
            res_sql)
        # 构建response
        print(links)
        if links:
            answer_entities = list(links.keys())
            self.origin_entity = list(links.values())[0]
            for node in self.origin_entity:
                self.response['graph']['nodes'].append(
                    {'id': node, 'group': "origin", 'new': False,'candidate':False})

            for answer_entity in answer_entities:
                self.response['graph']['nodes'].append(
                    {'id': answer_entity, 'group': answer_entity_type,'candidate':False})
            for answer_entity, answer_entity_natures in links.items():
                for a_e_nature in answer_entity_natures:
                    if self.origin_q_type in q_type_father_children:
                        self.response['graph']['links'].append(
                            {'source': a_e_nature, 'target': answer_entity, 'relation':q_type_show[self.origin_q_type],'new':False})
                    else:
                        self.response['graph']['links'].append(
                            {'source': answer_entity, 'target': a_e_nature, 'relation':q_type_show[self.origin_q_type],'new':False})
        # 未找到答案或答案唯一 退出
        if self.dialog_state == "Waiting":
            if not final_answers:
                self.system_reset()
                return self.false_response
            else:
                self.response['answer'] = final_answers
                self.response['result'] = result
                temp_response = self.response
                self.system_reset()
                return temp_response

        #  构造决策树,第一次进入“Questioning” 才会触发
        elif self.dialog_state == "Questioning":
            self.decision_tree = DecisionTree(answer_entities, self.origin_entity)
            self.decision_tree.build()
            question_info = self.decision_tree.ask()
            self.add_graph_entity(question_info)
            temp_response = copy.deepcopy(self.response)
            temp = []
            for link in temp_response['graph']['links']:
                temp.append(link['source'])
               # temp.append(link['target'])
            temp =Counter(temp)
            print(temp)
            print(self.response)
            for k,v in temp.items():
                if v ==1:
                    for n in temp_response['graph']['nodes']:
                        if n['id']==k and n['group']=='disease':
                            temp_response['graph']['nodes'].remove(n)
                    for link in temp_response['graph']['links']:   
                        if (link['source']==k) or (link['target']==k):
                            temp_response['graph']['links'].remove(link)
            return temp_response

        # 未找到答案或答案唯一 退出
        elif self.dialog_state == "Waiting":
            self.system_reset()
            if not final_answers:
                return self.false_response
            # else:
            #     return '\n'.join(final_answers)

            return self.response

    def check_input_number(self, sent):
        if str.isdigit(sent.replace(" ", "")):
            int_list = []
            str_list = sent.split(" ")
            for str in str_list:
                if str.isdigit(str):
                    int_list.append(int(str))
            return int_list
        else:
            return False

    def add_graph_entity(self, question_info):
        self.response['last_question_candi'] = question_info['nature_entities']
        self.response['answer'] = question_info['answer']
        for nature_entity in question_info['nature_entities']:
            self.response['graph']['nodes'].append(
                {'id': nature_entity, 'group': question_info['nature_entity_type'], 'new': True,'candidate':2})
        for answer_entity, answer_entity_natures in question_info['links'].items():
            for a_e_nature in answer_entity_natures:
                self.response['graph']['links'].append(
                    {'source': answer_entity, 'target': a_e_nature, 'relation': q_type_show[question_info['q_type']], 'new': True})
        

    def del_graph_entity(self, del_entity_list):

        old_nodes = []
        for i in self.response['graph']['links']:
            old_nodes.append(i['target'])
            old_nodes.append(i['source'])

        self.response['graph']['links'] = [
            i for i in self.response['graph']['links'] if (i['source'] not in del_entity_list)and (i['target'] not in del_entity_list)]

        new_nodes = []
        for i in self.response['graph']['links']:
            new_nodes.append(i['target'])
            new_nodes.append(i['source'])

        del_nature_list = list(
            set(old_nodes)-set(new_nodes))

        self.response['graph']['nodes'] = [i for i in self.response['graph']
                                           ['nodes'] if i['id'] not in (del_nature_list+del_entity_list)]

    def system_reset(self):
        self.__init__()


if __name__ == '__main__':
    handler = RobotRespond()
    while 1:
        question = input('用户:')
        answer = handler.system_main(question)
        print(answer)
