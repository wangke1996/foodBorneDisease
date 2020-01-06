from flask import render_template, Blueprint, request
from backend.lib.chatRobot import ROBOT

main = Blueprint('main', __name__, template_folder='templates', static_folder='static', static_url_path="/static")


@main.route('/getAnswer', methods=['GET', 'POST'])
def search_food():
    message_list = request.get_json()
    return ROBOT.make_response(message_list)

# @main.route('/', defaults={'path': ''})
# @main.route('/<path:path>')
# def index(path):
#     return render_template('index.html')
