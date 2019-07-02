from dao import BaseDao
from datetime import datetime


class OrderDao(BaseDao):
    def next_order_num(self):
        data = self.query('select max(order_num) as max_num from t_order')[0]
        next_num = data.get('max_num')
        current_date = datetime.now().strftime('%Y%m%d')
        if next_num:
            last_date = next_num[:8]
            last_num = next_num[8:]
            if current_date == last_date:
                last_num = int(last_num)+1
                return "%s%s" % (last_date, str(last_num).rjust(5, '0'))

        return '%s00001' % current_date




if __name__ == '__main__':
    dao = OrderDao()
    print(dao.next_order_num())