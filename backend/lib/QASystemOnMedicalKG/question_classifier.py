import os
import ahocorasick
import json
import numpy as np
# 设置默认文件编码utf8
import _locale
from bert_serving.client import BertClient
from pyltp import Segmentor

LTP_DATA_DIR = 'ltp_data_v3.4.0'
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')
segmentor = Segmentor()
segmentor.load(cws_model_path)

bc = BertClient()

_locale._getdefaultlocale = (lambda *args: ['en_US', 'utf8'])


class QuestionClassifier:
    def __init__(self):
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        #　特征词路径
        self.disease_path = os.path.join(cur_dir, 'dict/disease.json')
        self.food_path = os.path.join(cur_dir, 'dict/food.json')
        self.symptom_path = os.path.join(cur_dir, 'dict/symptom.json')
        self.deny_path = os.path.join(cur_dir, 'dict/deny.txt')
        # 加载特征词
        self.disease_vec = json.load(open(self.disease_path))
        self.disease_wds = list(self.disease_vec.keys())
        self.food_vec = json.load(open(self.food_path))
        self.food_wds = list(self.food_vec.keys())
        self.symptom_vec = json.load(open(self.symptom_path))
        self.symptom_wds = list(self.symptom_vec.keys())
        self.region_vecs = dict(
            self.disease_vec, **self.food_vec, **self.symptom_vec)
        self.region_words = set(
            self.disease_wds+self.food_wds+self.symptom_wds)
        self.deny_words = [i.strip()
                           for i in open(self.deny_path) if i.strip()]
        # 构造领域actree
        self.region_tree = self.build_actree(list(self.region_words))
        # 构建词典
        self.wdtype_dict = self.build_wdtype_dict()
        # 问句疑问词
        self.symptom_qwds = ['症状', '表征', '现象', '症候', '表现']
        self.cause_qwds = ['会引起','来源','原因', '成因', '为什么', '怎么会', '怎样才', '咋样才',
                           '怎样会', '如何会', '为啥', '为何', '如何才会', '怎么才会', '会导致', '会造成']
        self.acompany_qwds = ['并发症', '并发', '一起发生', '一并发生',
                              '一起出现', '一并出现', '一同发生', '一同出现', '伴随发生', '伴随', '共现']
        self.food_qwds = ['饮食', '饮用', '吃', '食', '伙食', '膳食', '喝',
                          '菜', '忌口', '补品', '保健品', '食谱', '菜谱', '食用', '食物', '补品']
        self.drug_qwds = ['药', '药品', '用药', '胶囊', '口服液', '炎片']
        self.prevent_qwds = ['预防', '防范', '抵制', '抵御', '防止', '躲避', '逃避', '避开', '免得', '逃开', '避开', '避掉', '躲开', '躲掉', '绕开',
                             '怎样才能不', '怎么才能不', '咋样才能不', '咋才能不', '如何才能不',
                             '怎样才不', '怎么才不', '咋样才不', '咋才不', '如何才不',
                             '怎样才可以不', '怎么才可以不', '咋样才可以不', '咋才可以不', '如何可以不',
                             '怎样才可不', '怎么才可不', '咋样才可不', '咋才可不', '如何可不']
        self.lasttime_qwds = ['周期', '多久', '多长时间', '多少时间',
                              '几天', '几年', '多少天', '多少小时', '几个小时', '多少年']
        self.cureway_qwds = ['怎么治疗', '如何医治', '怎么医治', '怎么治',
                             '怎么医', '如何治', '医治方式', '疗法', '咋治', '怎么办', '咋办', '咋治']
        self.cureprob_qwds = ['多大概率能治好', '多大几率能治好', '治好希望大么',
                              '几率', '几成', '比例', '可能性', '能治', '可治', '可以治', '可以医']
        self.easyget_qwds = ['易感人群', '容易感染',
                             '易发人群', '什么人', '哪些人', '感染', '染上', '得上']
        self.check_qwds = ['检查', '检查项目', '查出', '检查', '测出', '试出']
        self.belong_qwds = ['属于什么科', '属于', '什么科', '科室']
        self.cure_qwds = ['治疗什么', '治啥', '治疗啥', '医治啥', '治愈啥', '主治啥', '主治什么', '有什么用', '有何用', '用处', '用途',
                          '有什么好处', '有什么益处', '有何益处', '用来', '用来做啥', '用来作甚', '需要', '要']

        print('model init finished ......')

        return

    '''分类主函数'''

    def classify(self, question):
        data = {}
        entity_list = self.entity_extract_match(question)
        dialog_state = "Waiting"
        if not entity_list:
            prob_entity, original_word = self.entity_extract_bert(question)
            dialog_state = "SynonymQuestioning"
            return dialog_state, question.replace(original_word, prob_entity)
        data['entities'] = entity_list
        # 收集问句当中所涉及到的实体类型
        types = []
        for type_ in entity_list.values():
            types += type_

        question_type=''
        # todo :仅支持单一描述
        # 症状
        if self.check_words(self.symptom_qwds, question) and ('disease' in types):
            question_type = 'disease_symptom'

        if ('symptom' in types):
            question_type = 'symptom_disease'


        # 来源
        if self.check_words(self.cause_qwds, question) and ('disease' in types):
            question_type = 'result_from'

        # 疾病易感染人群
        if self.check_words(self.easyget_qwds, question) and 'disease' in types:
            question_type = 'disease_easyget'

        data['question_types'] = question_type

        return dialog_state, data

    '''构造词对应的类型'''

    def build_wdtype_dict(self):
        wd_dict = dict()
        for wd in self.region_words:
            wd_dict[wd] = []
            if wd in self.disease_wds:
                wd_dict[wd].append('disease')
            if wd in self.food_wds:
                wd_dict[wd].append('food')
            if wd in self.symptom_wds:
                wd_dict[wd].append('symptom')
        return wd_dict

    '''构造actree，加速过滤'''

    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    '''问句过滤'''

    def entity_extract_bert(self, question):
        n_grams = [2,3,4]
        for n in n_grams:
            term = []
            max_score = 0
            for i in range(len(question)):
                term.append(question[i:i+n])
            for word in term:
                wd_vec = bc.encode([word])[0]
                for wd, vec in self.symptom_vec.items():
                    score = np.inner(wd_vec, vec) / \
                        (np.linalg.norm(wd_vec)*np.linalg.norm(vec))
                    if score > max_score:

                        max_score = score
                        prob_entity = wd
                        original_word = word
        return prob_entity, original_word

    def entity_extract_match(self, question):
        region_wds = []
        for i in self.region_tree.iter(question):
            wd = i[1][1]
            region_wds.append(wd)
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)
        final_wds = [i for i in region_wds if i not in stop_wds]
        final_dict = {i: self.wdtype_dict.get(i) for i in final_wds}
        return final_dict

    '''基于特征词进行分类'''

    def check_words(self, wds, sent):
        for wd in wds:
            if wd in sent:
                return True
        return False


if __name__ == '__main__':
    handler = QuestionClassifier()
    while 1:
        question = input('input an question:')
        data = handler.classify(question)
        print(data)
