# bert-serving-start -model_dir F:\learn\ngnlab\KG\chinese_L-12_H-768_A-12\chinese_L-12_H-768_A-12
import re

# 设置默认文件编码utf8
import _locale
# from answer_search import *
# from decision_tree import *
# from question_classifier import *
# from question_parser import *

from . import *

_locale._getdefaultlocale = (lambda *args: ['en_US', 'utf8'])


dialog_state_table = ["Waiting", "Questioning", "SynonymQuestioning"]
q_type_father_children = ['disease_symptom', 'result_from', 'disease_easyget']
q_type_show ={'disease_symptom':"导致",'result_from' :"来源",'has_time':"发病",'symptom_disease':"导致"}


class RobotRespond:
    def __init__(self):
        self.dialog_state = dialog_state_table[0]
        self.classifier = QuestionClassifier()
        self.parser = QuestionPaser()
        self.searcher = AnswerSearcher()
        self.last_question = ""
        self.response = {'answer': '', 'result': '',
                         'graph': {'nodes': [],  'links': []}}
        self.false_response = {'answer': '我没能理解你的问题'}
        self.origin_q_type = ''
        self.origin_entity = ''

    def system_main(self, sent):

        if self.dialog_state == "Waiting":
            return self.get_answer(sent)

        elif self.dialog_state == "Questioning":
            # sent  --> int or list

            if str.isdigit(sent):
                self.dialog_state, del_entity_list, question_info = self.decision_tree.reply(
                    int(sent))
                # 更新response_graph
                # 增加新节点及链接
                for link in self.response['graph']['links']:
                    link['new'] = False
                for node in self.response['graph']['nodes']:
                    node['new'] = False
                self.add_graph_entity(question_info)
                # 删除排除节点及链接

                self.del_graph_entity(del_entity_list)

                if self.dialog_state == "Waiting":
                    temp_response = self.response
                    temp_response['result'] = question_info['result']
                    self.system_reset()

                    return temp_response

                else:

                    return self.response

            else:

                return self.response

        elif self.dialog_state == "SynonymQuestioning":
            # 将模糊实体替换后重新回答
            self.dialog_state == "Waiting"
            if sent == "是":
                return self.get_answer(re.sub("你想问的是不是:|(是/否)", "", self.response['answer']))
            else:
                self.system_reset()
                return self.false_response

    def get_answer(self, sent):

        # todo: 完全错误输入 仍会去返回相似度最高
        self.dialog_state, res_classify = self.classifier.classify(sent)
        print(res_classify)

        #  问题分类 实体抽取中模糊表达
        if self.dialog_state == "SynonymQuestioning":
            self.response['answer'] = "你想问的是不是:" + res_classify + "(是/否)"
            return self.response

       # 无分类结果
        if not res_classify['question_types']:
            self.system_reset()
            return self.false_response

        # 保存实体抽取结果
        self.origin_q_type = res_classify['question_types']
        self.origin_entity = list(res_classify['entities'].items())[0][0]
        self.origin_entity_type = list(res_classify['entities'].items())[0][1]

        self.response['graph']['nodes'].append(
            {'id': self.origin_entity, 'group': self.origin_entity_type, 'new': True})

        # 查询构造
        res_sql = self.parser.parser_main(res_classify)
        print(res_sql)
        self.dialog_state, final_answers, desc = self.searcher.search_main(
            res_sql)
        # 构建response

        answer_entity_type, answer_entities = list(desc.items())[0]
        for answer_entity in answer_entities:
            self.response['graph']['nodes'].append(
                {'id': answer_entity, 'group': answer_entity_type})

            if self.origin_q_type in q_type_father_children:
                self.response['graph']['links'].append(
                    {'source': self.origin_entity, 'target': answer_entity, 'relation': q_type_show[self.origin_q_type]})
            else:
                self.response['graph']['links'].append(
                    {'source': answer_entity, 'target': self.origin_entity, 'relation':q_type_show[self.origin_q_type]})

        # 未找到答案或答案唯一 退出
        if self.dialog_state == "Waiting":
            if not final_answers:
                self.system_reset()
                return self.false_response
            else:

                self.response['answer'] = final_answers
                temp_response = self.response
                self.system_reset()
                return temp_response

        #  构造决策树,第一次进入“Questioning” 才会触发
        elif self.dialog_state == "Questioning":
            self.decision_tree = DecisionTree(desc, self.origin_entity)
            self.decision_tree.build()
            question_info = self.decision_tree.ask()
            self.add_graph_entity(question_info)

            return self.response

        # 未找到答案或答案唯一 退出
        elif self.dialog_state == "Waiting":
            self.system_reset()

            if not final_answers:
                return self.false_response
            else:
                return '\n'.join(final_answers)

            return question

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
        self.response['answer'] = question_info['answer']
        for nature_entity in question_info['nature_entities']:
            self.response['graph']['nodes'].append(
                {'id': nature_entity, 'group': question_info['nature_entity_type'], 'new': True})
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
        print('小勇:', answer)
