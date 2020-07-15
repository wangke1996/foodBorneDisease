
# C= QuestionClassifier()
# cur_dir = os.path.dirname(os.path.abspath(__file__))

# disease_path = os.path.join(cur_dir, 'dict/disease.json')
# disease_vec = json.load(open(disease_path))
# disease_wds = list(disease_vec.keys())

# symptom_path= os.path.join(cur_dir, 'dict/symptom.json')
# symptom_vec = json.load(open(symptom_path))
# symptom_wds = list(symptom_vec.keys())

# entity_wds = disease_wds+symptom_wds


# from bert_serving.client import BertClient
# bc = BertClient()
# dd={}
# for wd in tqdm(symptom_wds):
#     dd[wd] = bc.encode([wd])[0].tolist()
# with open("jsonobj.json","w",encoding="utf-8") as f:
#     json.dump(dd,f,ensure_ascii=False)




# x=[]
# with open("test_list.txt",'r') as load_f:
#     s= load_f.readlines()
#     for i in s:
#         i.replace('\n',"")
#         x.append(i.split("^^^"))



# for i in range(100):
#     s=random.choice(x)
#     str = C.clean(s['originalText'])
#     str = C.clean(s)
#     Top3Scores_L = C.synonym_search(str, "Levenshtein")
#     Top3Scores_W = C.synonym_search(str, "Word2Vec")
#     entity_list_L = [i[2] for i in Top3Scores_L ]
#     entity_list_W = [i[2] for i in Top3Scores_W]
#     print("W",entity_list_W)
#     print("L",entity_list_L)
#     TopScores =  Top3Scores_L+Top3Scores_W
#     TopScores1 = copy.deepcopy(TopScores)
#     去重
#     existing_wd = []

#     for score in TopScores:
    
#         if score[2] in existing_wd:
#             TopScores1.remove(score)
#         existing_wd.append(score[2])
#     print("BERT\n",Top3Scores_Bert)
#     print("w2v\n",Top3Scores_W)
#     print("L\n",Top3Scores_L)
#     entity_list = [i[2] for i in TopScores1]

#     print("only L\n",only_L)
#     print("only WOrd\n",only_W)
#     print(i)
#     print(str)
#     print(entity_list)
#     choice = input()

#     if choice.isdigit():
#         entity= entity_list[int(choice)-1]
        
#     else :
#         entity="0"
#     if choice !="q":
#         test_list.append([str,entity])
#         with open('test_listbert.txt','a') as f:
#             f.write(str+"^^^"+entity+'\n')

# print(test_list)




