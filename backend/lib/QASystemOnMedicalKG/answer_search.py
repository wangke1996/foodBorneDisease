#!/usr/bin/env python3
# coding: utf-8
# File: answer_search.py


from py2neo import Graph
type_table = {'disease_symptom': 'symptom', 'symptom_disease': 'disease',
              'result_from': 'food', 'disease_easyget': 'people'}


class AnswerSearcher:
    def __init__(self):
        self.g = Graph("http://localhost:7474", auth=("neo4j", "ohahaha"))
        self.num_limit = 100

    '''执行cypher查询，并返回相应结果'''

    def search_main(self, sql_):
        final_answers = []
        dialog_state = "Waiting"
        question_type = sql_['question_type']
        queries = sql_['sql']
        answers = []
        # query = queries[0]
        # ress = self.g.run(query).data()
        # answers += ress
        # desc =self.get_desc(question_type,answers)
        desc = []
        desc_len = []
        candi_answers = set()
        for query in queries:
            ress = self.g.run(query).data()
            answers += ress
            temp = set(self.get_desc(question_type, ress))
            desc.append(temp)
            desc_len.append(len(temp))

        if len(answers) > 1 and question_type == 'symptom_disease':
            dialog_state = "Questioning"

        if not answers:
            final_answers = []

        else:
            origin_entity = sql_['entities']
            candi_answers = desc[0]
            for d in desc:
                candi_answers = candi_answers & d

            # 去交集后若为0 去最大值

            if len(candi_answers) == 0:
                candi_answers = desc[desc_len.index(max(desc_len))]
                origin_entity = [sql_['entities']
                                 [desc_len.index(max(desc_len))]]
            candi_answers = list(candi_answers)

            answer_entity_type = type_table[question_type]

            answer_entity,final_answer = self.answer_prettify(question_type, answers)
            if final_answer:
                final_answers.append(final_answer)
            links = {}
            for candi_answer in candi_answers:
                links[candi_answer] = origin_entity

        return dialog_state, answer_entity,final_answers,answer_entity_type,links

    # def get_desc(self, question_type,answers):
    #     if question_type == 'disease_symptom':
    #         desc = {'symptom':[i['n.name'] for i in answers]}
    #     elif question_type == 'symptom_disease':
    #         desc = {'disease':[i['m.name'] for i in answers]}
    #     elif question_type == 'result_from':
    #         desc = {'food':[i['n.name'] for i in answers]}
    #     elif question_type == 'disease_easyget':
    #         desc = {'people':[i['n.name'] for i in answers]}
    #     return desc

    def get_desc(self, question_type, answers):
        if question_type == 'symptom_disease':
            desc = [i['m.name'] for i in answers]
        else:  # 'disease_symptom''result_from''disease_easyget'
            desc = [i['n.name'] for i in answers]
        return desc

    def answer_prettify(self, question_type, answers):

        final_answer = []
        if question_type == 'disease_symptom':
            answer_entity = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的症状包括：{1}'.format(subject, '、'.join(
                [i['n.name'] for i in answers][:self.num_limit]))

        elif question_type == 'symptom_disease':
            subject = answers[0]['n.name']
            answer_entity = [i['m.name'] for i in answers]
            final_answer = '症状{0}可能的原因是有：{1}'.format(subject, '、'.join(
                [i['m.name'] for i in answers][:self.num_limit]))

        elif question_type == 'result_from':
            answer_entity = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '可能引起{0}的食物有：{1}'.format(subject, '、'.join(
                [i['n.name'] for i in answers][:self.num_limit]))

        elif question_type == 'disease_easyget':
            answer_entity = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']

            final_answer = '{0}的易感人群有：{1}'.format(subject, '、'.join(
                [i['n.name'] for i in answers][:self.num_limit]))

        return answer_entity,final_answer


if __name__ == '__main__':
    searcher = AnswerSearcher()
