from apps import app
from views import app_user, order, video
from flask_cors import CORS

APP_CONFIG={
    'host': '0.0.0.0',
    'port': 9001,
    'debug': True
}

if __name__ == '__main__':
    CORS().init_app(app)
    app.register_blueprint(app_user.blue)
    app.register_blueprint(order.order_blue)
    app.register_blueprint(video.blue)

    app.run(**APP_CONFIG)