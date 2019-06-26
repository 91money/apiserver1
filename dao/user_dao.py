from dao import BaseDao
from logger import api_logger

from libs.crypt import make_password, check_password

class UserDao(BaseDao):

    def save(self, **values):
        api_logger.info('db insert app_user_2: <%s>' % values['login_name'])
        values['login_auth_str'] = make_password(values['login_auth_str'])
        return super(UserDao, self).save('app_user_2', **values)

    def check_login_name(self, login_name):
        # 检查用户名是否已存在
        result = self.query('select id as cnt from app_user_2 where login_name=%s', login_name)
        return not bool(result)

    def login(self, login_name, login_auth_str):
        sql = 'select id, login_auth_str from app_user_2 ' \
              'where login_name=%s and activated=%s'
        user_data = self.query(sql, login_name, 1)

        if user_data:
            user_id, auth_str = (user_data[0].get('id'),
                                 user_data[0].get('login_auth_str'))

            if check_password(login_auth_str, auth_str):
                # 验证成功
                user_profile = self.get_profile(user_id)
                if user_profile is None:
                    return {
                        'user_id': user_id,
                        'nick_name': login_name
                    }

                return user_profile
            api_logger.warn('用户 %s 的口令不正确' % login_name)
            raise Exception('用户 %s 的口令不正确' % login_name)
        else:
            api_logger.warn('查无此用户 %s' % login_name)
            raise Exception('查无此用户 %s' % login_name)

    def get_profile(self, user_id):
        # 获取用户的详细信息
        sql = "select user_id, nick_name, phone, photo from app_user_profile " \
              "where user_id=%s"
        user_profile = self.query(sql, user_id)
        if user_profile:
            return user_profile[0]


if __name__ == '__main__':
    dao = UserDao()
    # dao.login('disen', 'disen666')  # 登录成功之后的数据
    print(dao.check_login_name('disen'))