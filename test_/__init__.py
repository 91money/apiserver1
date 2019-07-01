import requests


def test_uploadavator():
    url = 'http://10.35.162.152:9001/upload_avator/'
    data = {
        'token': '123'
    }
    files = {
        'img': ('mm6.jpg', open('/Users/apple/Documents/imags/mm6.jpg', 'rb'), 'image/jpeg'),
    }
    resp = requests.post(url, data=data, files=files)
    resp_data = resp.json()
    print(resp_data)
    assert resp_data.get('code') == 200
    print('ok')


def test_get_img_url(key, type=0):
    resp = requests.get('http://10.35.162.152:9001/img_url/%s?type=%s' % (key, type))
    print(resp.json())


if __name__ == '__main__':
    # test_uploadavator()
    test_get_img_url('723da9b1fd15417f969cf70713f45b62', 1)
