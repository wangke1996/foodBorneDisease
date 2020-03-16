from flask import render_template, Blueprint, request
from backend.lib.chat_robot import ROBOT
from backend.lib.bug_knowledge import KNOWLEDGE

main = Blueprint('main', __name__, template_folder='templates', static_folder='static', static_url_path="/static")


@main.route('/getAnswer', methods=['GET', 'POST'])
def search_food():
    message_list = request.get_json()
    return ROBOT.make_response(message_list)


@main.route('/getBugs', methods=['GET'])
def get_bugs():
    return KNOWLEDGE.get_bugs()


@main.route('/getBugDetail', methods=['GET'])
def get_bug_detail():
    bug_key = request.args.get('bugKey')
    return KNOWLEDGE.get_detail(bug_key)
# @main.route('/', defaults={'path': ''})
# @main.route('/<path:path>')
# def index(path):
#     return render_template('index.html')
