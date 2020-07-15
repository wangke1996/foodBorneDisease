# import time
import os
import random
import json
import copy
import _locale
from answer_search import *
#from decision_tree import *
from question_classifier import *
from question_parser import *
from tqdm import tqdm
import csv


###############################################
#test

C= QuestionClassifier()
cur_dir = os.path.dirname(os.path.abspath(__file__))

disease_path = os.path.join(cur_dir, 'dict/disease.json')
disease_vec = json.load(open(disease_path))
disease_wds = list(disease_vec.keys())

symptom_path= os.path.join(cur_dir, 'dict/symptom.json')
symptom_vec = json.load(open(symptom_path))
symptom_wds = list(symptom_vec.keys())

entity_wds = disease_wds+symptom_wds


from bert_serving.client import BertClient
bc = BertClient()
dd={}
for wd in tqdm(symptom_wds):
    dd[wd] = bc.encode([wd])[0].tolist()
# with open("jsonobj.json","w",encoding="utf-8") as f:
#     json.dump(dd,f,ensure_ascii=False)


C.symptom_vec=dd

x=[]
with open("test_list.txt",'r') as load_f:
    s= load_f.readlines()
    for i in s:
        i.replace('\n',"")
        x.append(i.split("^^^"))


lenx=len(x)
count_B=0
for i in tqdm(x):
    str=i[0]
    Top3Scores_B = C.synonym_search(str, "Bert")

    entity_list_B = [i[2] for i in Top3Scores_B]
    i[1]=i[1][:-1]
    if i[1] in entity_list_B:
        count_B+=1
        print("!")
    
print(count_B/lenx)
   