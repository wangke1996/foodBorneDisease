# from bert_serving.server.helper import get_args_parser
# from bert_serving.server import BertServer
# args = get_args_parser().parse_args(['-model_dir', ' F:\learn\ngnlab\KG\chinese_L-12_H-768_A-1'])
# server = BertServer(args)
# server.start()


# import os
# from pyltp import Segmentor
# LTP_DATA_DIR='ltp_data_v3.4.0'
# cws_model_path=os.path.join(LTP_DATA_DIR,'cws.model')
# segmentor=Segmentor()
# segmentor.load(cws_model_path)
# words=segmentor.segment('熊高雄你吃饭了吗')
# print(type(words))
# print('\t'.join(words))
# segmentor.release()

class Person:
    def __init__(self):
        self.age = 1
    def p(self):
        self.age=2
    def l(self):
        self.__init__()

xx= Person()
print(xx.age)
xx.p()
print(xx.age)
xx.l()
print(xx.age)