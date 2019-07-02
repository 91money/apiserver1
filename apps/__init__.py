from flask import Flask
from flask_cors import CORS

from celery import Celery


app = Flask(__name__,
            static_folder='../uploads',
            static_url_path='/uploads')

# 配置Celery的消息中间件和结构存储位置
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

# 创建Celery的客户端
capp = Celery(__name__, broker=app.config['CELERY_BROKER_URL'])
capp.conf.update(app.config)
capp.autodiscover_tasks(('apps',), force=True)