class MaxTriesException(Exception):
    "this is user's Exception for check the length of name "

    def __init__(self, funcName):
        self.funcName = funcName

    def __str__(self):
        print("函数:" + self.funcName + "重试次数过多")
        if self.funcName == 'GetAuth':
            print("有可能是他妈的账号密码没填对")


def RetryMethodWhenFail(func):
    retryTimes = 0

    def wrapper( *args, **kwargs):
        nonlocal retryTimes
        while True:
            retryTimes += 1
            try:
                if retryTimes >= 50:
                    raise MaxTriesException(func.__name__)
                result = func( *args, **kwargs)
                break
            except AttributeError as e:
                raise e
            except MaxTriesException as e:
                raise e
            except Exception:
                continue
        return result

    return wrapper
