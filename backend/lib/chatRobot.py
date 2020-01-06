class ChatRobot(object):
    def __init__(self):
        pass

    def make_response(self, message_list):
        return 'this is a random response to "%s"' % message_list[-1]['data']['text']


ROBOT = ChatRobot()
