import random
import re
import time
from urllib import parse

from control.data_bean import DataBean
from control.download import new_request
from control.mongo_queue import Con
from control.save_file import SaveFile


class Parser:
    data_bean = DataBean()  # 对取回的数据进行封装
    Count = 0 # 多进程线程时等待一下
    def get(self):

        while self.Count < 10:
            try:
                record = Con.pop()
                self.Count = 0
            except KeyError:
                print('队列没有数据,等待0.1s', )
                time.sleep(0.1)
                self.Count += 1
            else:
                if self.Count > 1:
                    self.Count -= 1
                req = new_request.get(record["_id"], 3)

                # 如果返回的code不正常就直接跳过
                if req.status_code != 200 and req.status_code != 304:
                    Con.fail(record["_id"])
                    continue

                self.data_bean.set(req, record["_id"], record["depth"])

                if self.data_bean.content_type in ["text/html", "text/css", "application/javascript"]:

                    # 查找链接  正则没学好, 不然一个for搞定
                    linkre = re.compile('href="(.+?)"')
                    srcre = re.compile('src="(.+?)"')
                    srcre2 = re.compile('src=\s"(.+?)"')
                    cssre = re.compile('url\((.+?)\)')

                    for url in linkre.findall(self.data_bean.data):
                        if "http:" not in url and "www." not in url:
                            self.handle_url(url)

                    for url in srcre.findall(self.data_bean.data):
                        if "http:" not in url and "www." not in url:
                            self.handle_url(url)

                    for url in srcre2.findall(self.data_bean.data):
                        if "http:" not in url and "www." not in url:
                            self.handle_url(url)

                    for url in cssre.findall(self.data_bean.data):
                        if "http:" not in url and "www." not in url:
                            self.handle_url(url)

                SaveFile(self.data_bean)
                Con.complete(record["_id"])

    # 处理各种奇葩的url
    def handle_url(self, url):

        d = DataBean()
        t_url = url
        url = url.split("?t=")[0]

        strre = re.compile('list[0-9]{0,}-([0-9]{0,})')
        if re.search('list[0-9]{0,}-[0-9]{0,}', url):
            for u in strre.findall(url):
                url = url.replace(u, "0")

        replace_url = url
        if url[len(url)-2:] == "js":
            replace_url = url.replace("??", "")
        replace_url = replace_url.replace("amp;", "")

        self.data_bean.data = self.data_bean.data.replace(t_url, replace_url) # 把处理后的url改到原始数据中
        self.data_bean.raw_data = self.data_bean.data.encode(self.data_bean.encoding)

        # 拼接url
        d.url = parse.urljoin(self.data_bean.url, url)
        arr = url.split(".")
        d.content_type = arr[len(arr) - 1]
        d.depth = self.data_bean.depth + 1
        d.up_level = self.data_bean.url
        Con.push(d)


