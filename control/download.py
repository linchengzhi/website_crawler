import random
import re

import requests


class download():
    user_agent_list = []
    ip_blocked = 3  # 记录ip是否被封

    def __init__(self):

        self.iplist = {}  # 储存获取到的代理ip
        self.user_agent_list = [ # 多用几个,避免被封
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]
        self.get_ip()

    # 这网址大部分不能用,只有几个可以
    # def get_ip(self):
    #     User_Agent = random.choice(self.user_agent_list)
    #     header = {}
    #     header['User-Agent'] = User_Agent
    #
    #     url = 'http://www.xicidaili.com/nn/1'
    #     req = requests.get(url, headers=header)
    #     soup = BeautifulSoup(req.text)
    #     ips = soup.findAll('tr')
    #
    #     for x in range(1, len(ips)):
    #         ip = ips[x]
    #         tds = ip.findAll("td")
    #         ip_temp = "http://"+tds[1].contents[0] + ":" + tds[2].contents[0]
    #         self.iplist[ip_temp] = self.ip_blocked

    # 这个网站会反爬虫,不能请求太频繁
    def get_ip(self):
        html = requests.get("http://haoip.cc/tiqu.htm")  ##不解释咯
        ips = re.findall(r'r/>(.*?)<b', html.text, re.S)
        for ip in ips:
            i = re.sub('\n', '', ip)
            self.iplist[i.strip()] = self.ip_blocked

    # 请求
    def get(self, url, timeout=3, proxy=None, num_retries=1):
        UA = random.choice(self.user_agent_list)
        headers = {'User-Agent': UA}
        if self.ip_blocked == 0: # 判断本机ip是否被封
            proxy = {'http': random.choice(list(self.iplist.keys())), "https": random.choice(list(self.iplist.keys()))}
        try:
            if proxy is None:
                response = requests.get(url, headers=headers, timeout=timeout)
                self.ip_blocked = 3
            else:
                response = requests.get(url, headers=headers, proxies=proxy, timeout=timeout)
                self.ip_blocked -= 1
            return response
        except Exception as e:  # 如过上面的代码执行报错则执行下面的代码
            if proxy is not None:
                self.iplist[proxy["http"]] -= 1
                if self.iplist[proxy["http"]] == -1: # 判断ip是否被封,若是则删除
                    del self.iplist[proxy["http"]]
            if num_retries < 3 and self.iplist.__len__() > 0:
                num_retries += 1
                proxy = {'http': random.choice(list(self.iplist.keys())),
                         "https": random.choice(list(self.iplist.keys()))}
                return self.get(url, timeout, proxy, num_retries)  # 加上代理再来一遍
            else:
                return ErrorCode() # 请求页面不下来,跳过


class ErrorCode(object):
    status_code = 404


new_request = download()
