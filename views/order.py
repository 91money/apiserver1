"""
订单数据的接口API
"""
from flask import Blueprint, request, jsonify

from libs import cache

order_blue = Blueprint('order_blue', __name__)


@order_blue.route('/add_order/', methods=('POST', ))
def add_order():
    # 验证用户是否已登录
    token = request.args.get('token', None)
    if token is None:
        return jsonify({
            'code': 202,
            'msg': 'token查询参数必须提供或者登录后获取token'
        })
    if cache.check_token(token):
        user_id = cache.get_token_user_id(token)

        # 下订单的业务处理


    return jsonify({
        'code': 200,
        'msg': '下单成功',
        'data': {
            "user_id": user_id,
            'ord_num': '100191919',
            'state': '待支付',
            'price': '2900.00元'
        }
    })