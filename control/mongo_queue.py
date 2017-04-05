from pymongo import MongoClient, errors
from datetime import datetime, timedelta

from conf.conf import Config


class MongoQueue:
    OUTSTANDING = 1  # 初始状态
    PROCESSING = 2  # 正在下载状态
    COMPLETE = 3  # 下载完成状态
    FAIL = 4  # 下载失败状态

    def __init__(self, db, collection, timeout=300):  # 初始化mongo连接
        self.con = MongoClient(db["host"], db["port"])
        self.Client = self.con[db["db"]]
        self.collection = self.Client[collection]
        self.timeout = timeout

    def __bool__(self):

        record = self.collection.find_one({'status': {'$ne': self.COMPLETE}})
        return True if record else False

    # 插入url到mongo
    def push(self, data):
        try:
            self.collection.insert({'_id': data.url, 'status': self.OUTSTANDING, "up_level": data.up_level,
                                    'type': data.content_type, "depth": data.depth})
            print(data.url, "插入队列成功")
        except errors.DuplicateKeyError as e:
            print("地址已经存在")
            pass

    def pop(self):
        record = self.collection.find_and_modify(
            query={'status': self.OUTSTANDING},
            update={'$set': {'status': self.PROCESSING, 'timestamp': datetime.now()}},
        )
        if record:
            return record
        else:
            self.repair()
            raise KeyError

    def peek(self):
        record = self.collection.find_one({'status': self.OUTSTANDING})
        if record:
            return record['_id']

    def complete(self, url):
        self.collection.update({'_id': url}, {'$set': {'status': self.COMPLETE}})

    def fail(self, url):
        self.collection.update({'_id': url}, {'$set': {'status': self.FAIL}})

    def repair(self):
        record = self.collection.find_and_modify(
            query={
                'timestamp': {'$lt': datetime.now() - timedelta(seconds=self.timeout)},
                'status': {'$ne': self.COMPLETE}
            },
            update={'$set': {'status': self.OUTSTANDING}}
        )
        if record:
            print('重置URL状态', record['_id'])

    def clear(self):
        self.collection.drop()


Con = MongoQueue(Config.mongo, 'crawler_pz')


