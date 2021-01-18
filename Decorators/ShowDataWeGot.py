# author: HRH

# date: 2021/1/18

# PyCharm
def ShowDataWeGot(func):

    def wrapper(self, *args, **kwargs):
        result=func(self,*args,**kwargs)
        print("cookies=",self.cookies)
        print("token=",self.token)
        print("Auth=",self.Auth)
        print("BaseInfo:", self.baseInfo)
        return result

    return wrapper