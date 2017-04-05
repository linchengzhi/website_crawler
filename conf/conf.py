import json


class Conf:
    def __init__(self):
        file = open("conf/conf.json", encoding="utf-8")
        conf = json.load(file)
        self.mongo = conf["mongo"]
        self.site_url = conf["site_url"]
        self.save_url = conf["save_url"]
        self.save_path = conf["save_path"]


Config = Conf()
