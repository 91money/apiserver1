"""
订单数据的接口API
"""
from flask import Blueprint, request, jsonify

from dao.order_dao import OrderDao
from libs import cache
from apps import tasks

order_blue = Blueprint('order_blue', __name__)


@order_blue.route('/add_order/', methods=('POST', ))
def user_add_order():
    # 验证用户是否已登录
    token = request.args.get('token', None)
    if token is None:
        return jsonify({
            'code': 202,
            'msg': 'token查询参数必须提供或者登录后获取token'
        })
    if cache.check_token(token):
        user_id = cache.get_token_user_id(token)
        order_info = request.get_json()

        # 验证订单参数(和t_order表字段对应或order_detail)
        # 下订单的业务处理
        # 生成订单号(2019070200001,  2019070200002)
        dao = OrderDao()
        next_order_num = dao.next_order_num()
        order_info['order_num'] = next_order_num
        order_info['user_id'] = user_id

        tasks.add_order.delay(**order_info)

    return jsonify({
        'code': 201,
        'msg': '正在抢单',
        'oder_num': next_order_num
    })


@order_blue.route('/order_status/', methods=('GET',))
def order_status():
    order_num = request.args.get('order_num')
    if order_num:
        return jsonify(cache.check_qbuy_status(order_num))

    return jsonify({
        'code': 400,
        'msg': 'order_num查询参数必须提供'
    })