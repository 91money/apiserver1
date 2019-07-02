"""
声明高并发下执行的任务
"""
from dao.order_dao import OrderDao
from libs import cache
from . import capp

import time


@capp.task
def add_order(**order_info):
    # 被Worker工作进程执行
    # 确定order_info 包含order_num（订单号）信息
    dao = OrderDao()
    if dao.save('t_order', **order_info):
        cache.add_qbuy_order(order_info['order_num'],
                             order_info['user_id'])
    return {'msg': '下单成功!',
            'user_id': order_info['user_id']}