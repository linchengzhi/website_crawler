import multiprocessing
import time

from conf.conf import Config
from control.data_bean import DataBean
from control.mongo_queue import Con
from control.parser_url import Parser

# 多进程
def start():
    start_time = time.time()
    data_bean = DataBean()
    data_bean.url = Config.site_url
    Con.push(data_bean)
    pool = multiprocessing.Pool(multiprocessing.cpu_count())  # 定义进程池大小
    for i in range(0, multiprocessing.cpu_count()):
        pool.apply_async(Parser().get())  # 使用非阻塞方式调用func，阻塞是apply()

    pool.close()  # 关闭Pool，使其不再接受新的任务
    pool.join()  # 主进程阻塞，等待子进程的退出
    end_time = time.time()
    print("time = " + str(end_time - start_time))


start()
