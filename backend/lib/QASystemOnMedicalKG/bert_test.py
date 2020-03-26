from bert_serving.client import BertClient

bc = BertClient()
wd_vec = bc.encode(["你好"])
print(wd_vec)