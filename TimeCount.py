import datetime


def time_count(func):
    """
    计算时间计时闭包,装饰器使用
    :param func: 
    :return: 
    """
    def wrapper(*args, **kwargs):
        start_time = datetime.datetime.now()  # 开始时间
        print("开始时间: ", start_time)
        func(*args, **kwargs)
        end_time = datetime.datetime.now()  # 结束时间
        print("结束时间: ", end_time)
        print("花费时间: ", (end_time - start_time).seconds, "秒")
    return wrapper
