from .QASystemOnMedicalKG.chatbot_graph import ChatBotGraph


class ChatRobot(object):
    def __init__(self):
        self.handler = ChatBotGraph()
        pass

    def make_response(self, message_list):
        answer = self.handler.chat_main(message_list[-1]['data']['text'])

        return answer


ROBOT = ChatRobot()


