# from .QASystemOnMedicalKG.chatbot_graph import ChatBotGraph

response_with_graph_example = [
    # 假设首句抽取的症状是“肌肉疼痛”，下一级决策中，需要知道吃过猪肉（可能是弓形虫、旋毛虫）还是海鲜（空肠弯曲菌），
    # 则第一次返回的graph包含如下内容
    {
        'answer': '你最近吃过以下哪种食物：1.猪肉  2.蔬菜  3. 其它这一级决策的选项',
        'graph': {
            'nodes': [
                {'id': '肌肉疼痛', 'group': '症状'},
                {'id': '猪肉', 'group': '来源'},
                {'id': '海鲜', 'group': '来源'},
                {'id': '弓形虫', 'group': '病原'},
                {'id': '旋毛虫属', 'group': '病原'},
                {'id': '空肠弯曲菌', 'group': '病原'}
            ],
            'links': [
                {'source': '弓形虫', 'target': '肌肉疼痛', 'relation': '导致'},
                {'source': '旋毛虫属', 'target': '肌肉疼痛', 'relation': '导致'},
                {'source': '空肠弯曲菌', 'target': '肌肉疼痛', 'relation': '导致'},
                {'source': '弓形虫', 'target': '猪肉', 'relation': '来源'},
                {'source': '旋毛虫属', 'target': '猪肉', 'relation': '来源'},
                {'source': '空肠弯曲菌', 'target': '海鲜', 'relation': '来源'}
            ]
        }
    },
    # 假设用户选择了猪肉，则与海鲜、空肠弯曲菌无关，去掉相关的结点和边
    # 假设此时需要根据是否有头痛的症状来决定，头痛则是弓形虫，否则旋毛虫属
    # 那么将头痛加入到图中
    {
        'answer': '你最近是否出现了头痛的症状：1.是  2.否',
        'graph': {
            'nodes': [
                {'id': '肌肉疼痛', 'group': '症状'},
                {'id': '猪肉', 'group': '来源'},
                {'id': '弓形虫', 'group': '病原'},
                {'id': '旋毛虫属', 'group': '病原'},
                {'id': '头痛', 'group': '症状'}
            ],
            'links': [
                {'source': '弓形虫', 'target': '肌肉疼痛', 'relation': '导致'},
                {'source': '旋毛虫属', 'target': '肌肉疼痛', 'relation': '导致'},
                {'source': '弓形虫', 'target': '猪肉', 'relation': '来源'},
                {'source': '旋毛虫属', 'target': '猪肉', 'relation': '来源'},
                {'source': '弓形虫', 'target': '头痛', 'relation': '导致'}
            ]
        }
    },
    # 假设用户选择是，初步确诊为弓形虫感染，与旋毛虫属无关，去掉相关的结点和边
    {
        'answer': '您好，您的情况可能是弓形虫感染导致的，请参阅本系统中“弓形虫”相关知识。',
        'result': "弓形虫",  # 确诊后，返回结果中包含病原微生物的名称
        'graph': {
            'nodes': [
                {'id': '肌肉疼痛', 'group': '症状'},
                {'id': '猪肉', 'group': '来源'},
                {'id': '弓形虫', 'group': '病原'},
                {'id': '头痛', 'group': '症状'}
            ],
            'links': [
                {'source': '弓形虫', 'target': '肌肉疼痛', 'relation': '导致'},
                {'source': '弓形虫', 'target': '猪肉', 'relation': '来源'},
                {'source': '弓形虫', 'target': '头痛', 'relation': '导致'}
            ]
        }
    }
]

responses = (x for x in response_with_graph_example * 100)  # repeat for test


class ChatRobot(object):
    def __init__(self):
        # self.handler = ChatBotGraph()
        pass

    def make_response(self, message_list):
        # answer = self.handler.chat_main(message_list[-1]['data']['text'])
        answer = "answer for: %s" % message_list[-1]['data']['text']
        return answer

    def make_response_with_graph(self, message_list):
        global responses
        response = responses.__next__()
        return response


ROBOT = ChatRobot()
