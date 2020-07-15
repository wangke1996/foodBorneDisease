import os
import ahocorasick
import json
import numpy as np
import re
import copy
from tqdm import tqdm
# 设置默认文件编码utf8
import _locale
from bert_serving.client import BertClient
import synonyms
import Levenshtein
# LTP_DATA_DIR = 'ltp_data_v3.4.0'
# cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')
# segmentor = Segmentor()
# segmentor.load(cws_model_path)

bc = BertClient()

_locale._getdefaultlocale = (lambda *args: ['en_US', 'utf8'])


def takeSecond(elem):
    return elem[1]


class QuestionClassifier:
    def __init__(self):
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        #　特征词路径
        self.disease_path = os.path.join(cur_dir, 'dict/disease.json')
        self.food_path = os.path.join(cur_dir, 'dict/food.json')
        #self.symptom_path = os.path.join(cur_dir, 'dict/symptom.json')
        self.symptom_path = os.path.join(cur_dir, 'dict/bert_2.json')
        self.symptom_w2v_path = os.path.join(cur_dir, 'dict/symptom_w2v.json')
        self.deny_path = os.path.join(cur_dir, 'dict/deny.txt')
        self.stop_path = os.path.join(cur_dir, 'dict/hit_stopwords.txt')
        # 加载特征词
        self.disease_vec = json.load(open(self.disease_path))
        self.disease_wds = list(self.disease_vec.keys())
        self.food_vec = json.load(open(self.food_path))
        self.food_wds = list(self.food_vec.keys())
        self.symptom_vec = json.load(open(self.symptom_path))
        self.symptom_w2v_vec = json.load(open(self.symptom_w2v_path))
        self.symptom_wds = list(self.symptom_vec.keys())
        self.region_vecs = dict(
            self.disease_vec, **self.food_vec, **self.symptom_vec)
        self.region_words = set(
            self.disease_wds+self.food_wds+self.symptom_wds)
        self.deny_words = [i.strip()
                           for i in open(self.deny_path) if i.strip()]
        self.stop_words = [i.strip()
                           for i in open(self.stop_path) if i.strip()]
        # 构造领域actree
        self.region_tree = self.build_actree(list(self.region_words))
        # 构建词典
        self.wdtype_dict = self.build_wdtype_dict()
        # 问句疑问词
        self.symptom_qwds = ['症状', '表征', '现象', '症候', '表现', "怎么办"]
        self.cause_qwds = ['会引起', '来源', '原因', '成因', '为什么', '怎么会', '怎样才', '咋样才',
                           '怎样会', '如何会', '为啥', '为何', '如何才会', '怎么才会', '会导致', '会造成']
        self.acompany_qwds = ['并发症', '并发', '一起发生', '一并发生',
                              '一起出现', '一并出现', '一同发生', '一同出现', '伴随发生', '伴随', '共现']
        self.lasttime_qwds = ['周期', '多久', '多长时间', '多少时间',
                              '几天', '几年', '多少天', '多少小时', '几个小时', '多少年']
        self.easyget_qwds = ['易感人群', '容易感染',
                             '易发人群', '什么人', '哪些人', '染上', '得上']
        self.people_qwds = ["孩子", "老人", "我", "男", "女"]
        self.trigger_wds = self.symptom_qwds + self.cause_qwds + self.acompany_qwds + \
            self.lasttime_qwds+self.easyget_qwds + self.people_qwds

        print('model init finished ......')

        return

    '''分类主函数'''

    def classify(self, question):

  
        data = {}
        question_cleaned = self.clean(question)
        entity_list = self.entity_extract_match(question)
        dialog_state = "Waiting"
        if len(question_cleaned )<2:
            return dialog_state,{'entities':[],'question_types':""}


        # 未命中时 同义词搜索
        if not entity_list:
            dialog_state = "SynonymQuestioning"
            Top3Scores_Bert = self.synonym_search(question_cleaned, "Bert")
            Top3Scores_L = self.synonym_search(question_cleaned, "Levenshtein")
            #Top3Scores_W = self.synonym_search(question_cleaned, "Word2Vec")
            TopScores =  Top3Scores_Bert+Top3Scores_L
            print(TopScores)
            self.TopScores = copy.deepcopy(TopScores)
            # 去重
            existing_wd = []
            for score in TopScores:
                if score[2] in existing_wd:
                    self.TopScores.remove(score)
                existing_wd.append(score[2])
            print(self.TopScores)
            self.origin_question = question_cleaned
            answer = "你想问的是不是"
            candi_synonym = []
            for i, score in enumerate(self.TopScores):
                answer += (' '+str(i+1)+'.'+score[2])
                candi_synonym.append(score[2])
            answer+= (' '+str(i+2)+'.都不是')
            SynonymQuestioning_info = {
                "answer": answer, "candi_synonym": candi_synonym}
            return dialog_state, SynonymQuestioning_info

        data['entities'] = entity_list
        # 收集问句当中所涉及到的实体类型
        types = []
        for type_ in entity_list.values():
            types += type_

        question_type = ''
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
    def clean(self,sent):
        
        sent = re.sub(r"[0-9\s+\.\!\/_,$%^*()?;；:-【】+\"\']+|[+——！，;:。？、~@#￥%……&*（）]+", "", sent)
        # for wd in self.stop_words:
        #     if wd in sent:
        #         sent = sent.replace(wd, "")
        return sent


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


    def synonym_search(self, question, method):
        n_grams = [2, 3, 4,5]
        term = []
        scores = []
        for n in n_grams:
            for i in range(len(question)-n+1):
                word = question[i:i+n]
                if method == 'Bert':
                    wd_vec = bc.encode([word])[0]
                    
                elif method == 'Word2Vec':
                    try:
                        wd_vec = synonyms.v(word)
                    except:
                        wd_vec=[0]*100
                else:
                
                    wd_vec = 0
                term.append((word, wd_vec))
        
        for word, wd_vec in term:  
            max_score = 0
            for wd, vec in self.symptom_vec.items():
                
                if method == 'Bert':
                    score = np.inner(wd_vec, vec) / \
                        (np.linalg.norm(wd_vec)*np.linalg.norm(vec))
                    score= score
                if method == "Levenshtein":
                    score = Levenshtein.jaro(word, wd)
                if method == "Word2Vec":
                    try:
                        vec = self.symptom_w2v_vec[wd]
                  
                    except:
                        vec = [0]*100           
                    score = np.inner(wd_vec, vec) / \
                        ((np.linalg.norm(wd_vec)+1e-5)*(np.linalg.norm(vec)+1e-5))
                if score >= max_score:
                    max_score = score
                    prob_entity = wd
                    original_word = word
            scores.append((original_word, max_score, prob_entity))
        scores.sort(key=takeSecond, reverse=True)
        # prob_entity = scores[0][2]
        # original_word =scores[0][0]
        # print(method)
        return scores[:3]

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
    
    question = 'input an question:'
    data = handler.classify(question)
    print(data)
