from redis import Redis

rd = Redis(host='aliyun901',
           port=6378, db=1)

if __name__ == '__main__':
    print(rd.keys("*"))
    rd.flushall()