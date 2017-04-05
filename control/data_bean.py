class DataBean:
    url = ''
    path = ''
    cate = ''  # 目录
    depth = 1  # 记录爬虫爬到第几层
    up_level = ""
    raw_data = None
    data = None
    encoding = None
    content_type = "html"  # html img css js
    headers = None

    def reset(self):
        self.url = ''
        self.cate = ''
        self.depth = 1
        self.up_level = ""
        self.raw_data = None
        self.data = None
        self.encoding = None
        self.content_type = "html"  # html img css js
        self.headers = None

    def set(self, resp, url, depth=1):
        self.reset()

        temp = resp.headers["Content-Type"].strip()
        self.raw_data = resp.content
        if 'text/' in temp or 'javascript' in temp:
            temp = temp.split(';')
            self.content_type = temp[0]
            if len(temp) == 2 and 'charset' in temp[1]:
                self.encoding = temp[1].replace('charset=', '').strip()
            else:
                self.encoding = 'utf-8'
            self.data = self.raw_data.decode(self.encoding)
        else:
            self.content_type = temp

        if self.content_type == "text/html" and url[len(url) - 4:] != "html":
            self.url = url + "/index.html"
        else:
            self.url = url
        self.depth = depth
        arr = self.url.split("/")

        for x in arr[2:len(arr)-1]:
            self.cate = self.cate + "/" + x
        self.cate = self.cate[1:]


