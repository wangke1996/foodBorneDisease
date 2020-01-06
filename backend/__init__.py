from flask import Flask
from flask_cors import CORS


def creat_app():
    app = Flask(__name__, template_folder="templates", static_folder="static", static_url_path="/backend/static")
    # 防止跨域攻击
    CORS(app)
    # 注册蓝图
    from . import main
    app.register_blueprint(main.main)
    app.config['SECRET_KEY'] = 'ngn@soft'
    app.debug = True
    # db.init_app(app)
    return app
