from flask import Blueprint
from flask import request, jsonify
from logger import api_logger
from dao.user_dao import UserDao

blue = Blueprint('user_api', __name__)


@blue.route('/regist/', methods=('POST', ))
def user_regist():
    # 前端请求的Content-Type: application/json
    req_data = None
    api_logger.info(request.headers)
    if request.headers['Content-Type'].startswith('application/json'):
        req_data = request.get_json()

    api_logger.debug(req_data)

    # 验证上传的必须的数据是否存在
    if all(req_data.get('user_name', False),
           req_data.get('auth_string', False),
           req_data.get('nick_name', False),
           req_data.get('phone', False)):

        dao = UserDao()
        dao.save(**req_data)

    return jsonify({
       'code': 8000,
        'msg': 'ok',
        'data': req_data
    })


@blue.route('/login', methods=('GET', ))
def user_login():
    api_logger.debug('user login get action!')
    return "<html><head><title>Login Page</title></head><body>Hi, Disen</body></html>"