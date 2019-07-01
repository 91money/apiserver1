import os
import uuid

from flask import Blueprint
from flask import request, jsonify
from werkzeug.datastructures import FileStorage

from logger import api_logger
from dao.user_dao import UserDao

blue = Blueprint('user_api', __name__)

from datetime import datetime
from libs import cache, oss


@blue.route('/regist/', methods=('POST',))
def user_regist():
    # 前端请求的Content-Type: application/json
    req_data = None
    if request.headers['Content-Type'].startswith('application/json'):
        req_data = request.get_json()

    if req_data is None:
        api_logger.warn('%s 请求参数未上传-json' % request.remote_addr)
        return jsonify({
            'code': 9000,
            'msg': '请上传json数据，且参数必须按api接口标准给定'
        })

    api_logger.debug(req_data)

    # 验证上传的必须的数据是否存在
    if all((req_data.get('login_name', False),
            req_data.get('login_auth_str', False))):

        req_data['create_time'] = datetime.now().strftime('%Y-%m-%d')
        req_data['update_time'] = req_data['create_time']
        req_data['activated'] = 1  # 默认激活

        dao = UserDao()
        if dao.check_login_name(req_data.get('login_name')):

            if dao.save(**req_data):
                return jsonify({
                    'code': 200,
                    'msg': 'ok'
                })

            return jsonify({
                'code': 300,
                'msg': '插入数据失败, 可能存在某一些字段没有给定值'
            })
        else:
            return jsonify({
                'code': 201,
                'msg': '用户名已存在，不能再注册'
            })


@blue.route('/check_name/', methods=('GET',))
def check_login_name():
    # 查询参为数
    login_name = request.args.get('login_name')
    result = {
        'code': 200,
        'msg': '用户名不存在'
    }
    if not UserDao().check_login_name(login_name):
        result['code'] = 300
        result['msg'] = '用户名已存在'

    return jsonify(result)


@blue.route('/login/', methods=('GET',))
def user_login():
    api_logger.debug('user login get action!')
    # 验证参数
    login_name = request.args.get('login_name', None)
    auth_str = request.args.get('auth_str', None)
    if all((bool(login_name), bool(auth_str))):
        dao = UserDao()
        # 获取登录用户的信息
        try:
            login_user = dao.login(login_name, auth_str)
            # 生成token
            token = cache.new_token()

            # 将token存在redis的缓存中，绑定的数据可以是用户Id也可以是用户的信息
            cache.save_token(token, login_user.get('user_id'))
            return jsonify({
                'code': 200,
                'token': token,
                'user_data': login_user
            })
        except Exception as e:
            return jsonify({
                'code': 202,
                'msg': e
            })
    else:
        return jsonify({
            'code': 101,
            'msg': '请求参数login_name和auth_str必须存在'
        })


@blue.route('/upload_avator/', methods=('POST',))
def upload_avator():
    # 上传的头像字段为 img
    # 表单参数： token
    file: FileStorage = request.files.get('img', None)
    token = request.form.get('token', None)

    if all((bool(file), bool(token))):
        # 验证文件的类型, png/jpeg/jpg, 单张不能超过2M
        # content-type: image/png, image/jpeg
        print(file.content_length, 'bytes')
        if file.content_type in ('image/png',
                                 'image/jpeg'):
            filename = uuid.uuid4().hex \
                       + os.path.splitext(file.filename)[-1]
            file.save(filename)

            # 上传到oss云服务器上
            key = oss.upload_file(filename)

            os.remove(filename)  # 删除临时文件

            # 将key写入到DB中
            return jsonify({
                'code': 200,
                'msg': '上传文件成功',
                'file_key': key
            })
        else:
            return jsonify({
                'code': 201,
                'msg': '图片格式只支持png或jpeg'
            })

    return jsonify({
        'code': 100,
        'msg': 'POST请求参数必须有img和token'
    })


@blue.route('/img_url/<string:key>', methods=('GET', ))
def get_img_url(key):
    img_type = int(request.args.get('type', 0))

    img_url = oss.get_url(key) if img_type == 0 else oss.get_small_url(key)
    return jsonify({
        'url': img_url
    })