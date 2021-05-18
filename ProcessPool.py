# -*- coding:utf-8 -*-
#!/usr/bin/env python
# Author: JISO
# Email: 747142549@qq.com
# File: ProcessPool.py
from multiprocessing import Process, Lock


class MyProcess(Process):
    """进程模型"""

    times = 1
    error_times = 1
    mutex = Lock()

    def __init__(self, queue, **kwargs):
        super(MyProcess, self).__init__(**kwargs)
        self.queue = queue  # 队列对象
        self.start()  # 自动启动进程

    def run(self):
        while True:
            func, args, kwargs = self.queue.get(block=False)

            try:
                call_status = func(*args, **kwargs)
                if call_status:
                    print("成功%d次" % MyProcess.times)
                    with MyProcess.mutex:
                        MyProcess.times += 1
                else:
                    print("未请求到数据!")
            except Exception as error:
                self.queue.put((func, args, kwargs))
                print(error, "失败%d次, 任务重新放入队列" % MyProcess.error_times)
                with MyProcess.mutex:
                    MyProcess.error_times += 1

            self.queue.task_done()


class MyProcessPool(object):

    def __init__(self, queue, size, **kwargs):
        self.queue = queue
        self.pool = []

        for i in range(size):
            self.pool.append(MyProcess(queue, **kwargs))

    def join_all(self):
        for process in self.pool:
            if process.is_alive():
                process.join()
