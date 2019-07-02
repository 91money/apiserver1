from libs import rd
import uuid

def new_token():
    return uuid.uuid4().hex


def save_token(token, user_id):
    # 保存token
    rd.set(token, user_id)
    rd.expire(token, 12*3600)  # 有效时间： 12小时


def check_token(token):
    # 验证token
    return rd.exists(token)


def get_token_user_id(token):
    # 通过token获取user_id
    if check_token(token):
        return rd.get(token).decode()


def add_qbuy_order(order_num, user_id):
    # 抢单成功
    # 将用户ID和订单号存入到redis缓存中
    # 抢单如果限制时间，存的时间
    # rd.set(order_num, user_id)
    # 限量或限时间
    if not rd.exists('qbuy_order') or rd.hlen('qbuy_order') < 100:
        rd.hset('qbuy_order', order_num, user_id)


def check_qbuy_status(order_num):
    if rd.hexists('qbuy_order', order_num):
        return {
            'code': 200,
            'msg': '抢单成功',
            'order_num': order_num
        }
    else:
        if rd.hlen('qbuy_order') < 100:
            return {
                'code': 201,
                'msg': '正在抢单',
                'order_num': order_num
            }
        else:
            return {
                'code': 202,
                'msg': '抢单失败',
                'order_num': order_num
            }

