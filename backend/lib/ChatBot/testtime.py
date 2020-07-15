# import time
import os
# import random
import json
import copy
import _locale
from answer_search import *
#from decision_tree import *
from question_classifier import *
from question_parser import *
from tqdm import tqdm


# with open("jsonobj.json","w",encoding="utf-8") as f:
#         json.dump(dd,f,ensure_ascii=False)

# def randomchinese():
#     head = random.randint(0xb0, 0xf7)
#     body = random.randint(0xa1, 0xfe)
    
#     val = f'{head:x}{body:x}'
   

    
#     str = bytes.fromhex(val).decode('gb18030')
#     return str


# # P = QuestionPaser()
# # A = AnswerSearcher()
C= QuestionClassifier()
cur_dir = os.path.dirname(os.path.abspath(__file__))

# disease_path = os.path.join(cur_dir, 'dict/disease.json')
# disease_vec = json.load(open(disease_path))
# disease_wds = list(disease_vec.keys())

symptom_path= os.path.join(cur_dir, 'dict/symptom.json')
symptom_vec = json.load(open(symptom_path))
symptom_wds = list(symptom_vec.keys())

# food = os.path.join(cur_dir, 'dict/food.json')
# food_vec = json.load(open(food))
# food_wds = list(food_vec.keys())
# print("111111111")



from bert_serving.client import BertClient
bc = BertClient()
dd={}
for wd in tqdm(symptom_wds):
    dd[wd] = bc.encode([wd])[0].tolist()
with open("jsonobj.json","w",encoding="utf-8") as f:
    json.dump(dd,f,ensure_ascii=False)


# entity_wds = food_wds+disease_wds+symptom_wds
# ### 实体链接

# # total_time = 0 
# # for _ in range(100):
    
# entity = random.choice(entity_wds )
# num_left= random.choice(range(2,5))
# num_right = random.choice(range(2,5))
# str= ""
# for i in range(num_left):
#     str+=randomchinese()
# str+=entity
# for i in range(num_right):
#     str+=randomchinese()
str="肚子好痛"
#t1=time.time()
#entity_list = C.entity_extract_match(str)

#Top3Scores_L = C.synonym_search(str, "Levenshtein")
Top3Scores_Bert = C.synonym_search(str, "Bert")

# TopScores =  Top3Scores_Bert+Top3Scores_L
# TopScores1 = copy.deepcopy(TopScores)
# 去重
# existing_wd = []
# print(TopScores1)
# for score in TopScores:
#     print(score)
#     print(existing_wd)
#     if score[2] in existing_wd:
#         TopScores1.remove(score)
#         print("remove",score)
#     existing_wd.append(score[2])
# print(TopScores1)
#entity_list = C.synonym_search(str, "Word2Vec")
# t_used = time.time()-t1
# print(str,t_used,entity_list)
# total_time+=t_used

# #     #print(str)
# # total_time = total_time/100
# # print("final",total_time)


# ## 知识图谱存储
# # qts = ['disease_symptom','symptom_disease','result_from','disease_easyget']
# # total_time = 0 
# # for i in range(5):
# #     print(i)
# #     for e in disease_wds:
# #         res_classify ={}
        
# #         res_classify['question_types'] = qts[random.choice([0,2,3])]
# #         res_classify['entities']={e:['disease']}
# #         t1= time.time()
# #         res_sql = P.parser_main(res_classify)
# #         dialog_state, result,final_answers,answer_entity_type, links = A.search_main(
# #                     res_sql)
# #         t_used = time.time()-t1
        
# #         total_time+=t_used

# #     for e in symptom_wds:
# #         res_classify ={}
# #         res_classify['question_types'] = qts[1]
# #         res_classify['entities']={e:['symptom']}
# #         t1= time.time()
# #         res_sql = P.parser_main(res_classify)
# #         dialog_state, result,final_answers,answer_entity_type, links = A.search_main(
# #                     res_sql)
# #         t_used = time.time()-t1
        
# #         total_time+=t_used
# # total_time = total_time/(5*(len(symptom_wds)+len(disease_wds)))
# # print("final"+str(total_time))






# #决策树构建
# total_time = 0 
# for _ in range(500):
#     origin_entity=random.choice(symptom_wds)
#     num_left= random.choice(range(2,10))
#     answer_entities=[]
#     for i in range(num_left):

#         answer_entities.append(random.choice(disease_wds))
#     t1= time.time()
#     D = DecisionTree(answer_entities, origin_entity)
#     D.build()
#     t_used = time.time()-t1
#     total_time+=t_used
#     #print(D.tree_dict)
# total_time = total_time/(500)
# print("final"+str(total_time))
