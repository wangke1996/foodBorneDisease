
# bert-serving-start -model_dir F:\learn\ngnlab\KG\chinese_L-12_H-768_A-12\chinese_L-12_H-768_A-12
from . import *
# from question_classifier import *
# from question_parser import *
# from answer_search import *
# from decision_tree import *

# 设置默认文件编码utf8
import _locale
_locale._getdefaultlocale = (lambda *args: ['en_US', 'utf8'])


dialog_state_table = ["Answering", "Questioning", "SynonymQuestioning"]

'''问答类'''


class ChatBotGraph:
    def __init__(self):
        self.dialog_state = dialog_state_table[0]
        self.classifier = QuestionClassifier()
        self.parser = QuestionPaser()
        self.searcher = AnswerSearcher()
        self.last_question = ""

    def chat_main(self, sent):
        if self.dialog_state == "Answering":
            return self.get_answer(sent)

        elif self.dialog_state == "Questioning":
            # sent  --> int or list
            if str.isdigit(sent):
                self.dialog_state, answer = self.decision_tree.reply(int(sent))
            else:
                answer = self.decision_tree.ask()
            return answer

        elif self.dialog_state == "SynonymQuestioning":
            if sent == "是":
                return self.get_answer(self.last_question)
            else:
                return "我没能理解你的问题"

    def get_answer(self, sent):
        init_answer = '没答上来'
        self.dialog_state, res_classify = self.classifier.classify(sent)
        if self.dialog_state == "SynonymQuestioning":
            self.last_question = res_classify
            return "你想问的是不是:"+self.last_question+"(是/否)"
        print(res_classify)
        if not res_classify:
            return init_answer
        res_sql = self.parser.parser_main(res_classify)
        print(res_sql)
        self.dialog_state, final_answers, desc = self.searcher.search_main(
            res_sql)
        if self.dialog_state == "Questioning":
            self.decision_tree = DecisionTree(desc)
            self.decision_tree.build()
            question = self.decision_tree.ask()

            return question

        elif self.dialog_state == "Answering":
            if not final_answers:
                return init_answer
            else:
                return '\n'.join(final_answers)


if __name__ == '__main__':
    handler = ChatBotGraph()
    while 1:
        question = input('用户:')
        answer = handler.chat_main(question)
        print('小勇:', answer)
