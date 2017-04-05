import os

from conf.conf import Config


class SaveFile:
    def __init__(self, data):
        self.data_bean = data
        self.handle_url()
        self.mkdir()
        self.write_file()

    # 处理特殊字符等
    def handle_url(self):
        if self.data_bean.url[len(self.data_bean.url) - 2:] == "js":
            self.data_bean.url = self.data_bean.url.replace("??", "")
        self.data_bean.url = self.data_bean.url.replace("amp;", "")
        self.data_bean.path = Config.save_path + self.data_bean.url[7:]
        if self.data_bean.url == Config.site_url:
            self.data_bean.path += "/index.html"

    # 创建文件夹
    def mkdir(self):
        path = os.path.dirname(self.data_bean.path)
        if not os.path.lexists(path):
            os.makedirs(path)

    # 写入数据到文件中
    def write_file(self):
        try:
            fd = open(self.data_bean.path, 'wb')
            fd.write(self.data_bean.raw_data)
            fd.close()
        except Exception as e:
            print(e)
