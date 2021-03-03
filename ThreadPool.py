from threading import Thread
from threading import Lock
from queue import Queue


class MyThread(Thread):
    """线程模型"""

    success_times = 1  # 成功计数
    error_times = 1  # 失败计数
    mutex = Lock()  # 线程锁

    def __init__(self, queue, **kwargs):
        super(MyThread, self).__init__(**kwargs)
        assert isinstance(queue, Queue), "必须是从queue库导入的Queue类对象!"
        self.queue = queue  # 队列对象
        self.start()  # 自动启动线程

    def run(self):
        while True:
            func, args, kwargs = self.queue.get(block=False)  # 当block为False时队列为空的时候去get,会引发异常

            try:
                call_status = func(*args, **kwargs)
                if call_status:
                    MyThread.mutex.acquire()  # 锁定
                    print("成功%d次" % MyThread.success_times)
                    MyThread.success_times += 1
                    MyThread.mutex.release()
                else:
                    print("未请求到数据!")

            except Exception as error:
                self.queue.put((func, args, kwargs))
                MyThread.mutex.acquire()  # 锁定
                print(error, "失败%d次, 任务重新放入队列" % MyThread.error_times)
                MyThread.error_times += 1
                MyThread.mutex.release()

            self.queue.task_done()


class MyThreadPool(object):

    def __init__(self, queue, size, **kwargs):
        assert isinstance(queue, Queue), "必须是从queue库导入的Queue类对象!"
        self.queue = queue
        self.pool = []
        for i in range(size):
            self.pool.append(MyThread(queue, **kwargs))

    def join_all(self):
        """
        阻塞全部线程对象
        :return:
        """
        for thread in self.pool:
            if thread.isAlive():
                thread.join()
