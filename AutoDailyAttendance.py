# author: HRH_theRenegade

# date: 2021/1/18

# PyCharm
import datetime
import time
import json
import sys
import requests
from lxml import etree
import re
from Decorators.RetryMethodWhenFail import RetryMethodWhenFail
from Decorators.ShowDataWeGot import ShowDataWeGot

"""
流程：
1.从输入获取账号密码
2.登录中央认证系统，获取cookies
3.拿cookies去获取
"""
# 从控制台输入获取账号密码
userID = input()
passwd = input()


class DataWeNeed:
    """
    一些我们需要保存的数据
    """

    @ShowDataWeGot
    def __init__(self):
        rawHtml, self.cookies = getRawResonse()
        self.token = SearchToken(rawHtml.text, self)
        self.Auth = GetAuth(self)
        self.baseInfo = GetBaseInfo_Raw(self)
        self.baseInfo = GetBaseInfo_json(self)


@RetryMethodWhenFail
def getRawResonse():
    """
    获取页面响应
    :return: 未处理过的页面代码,Cookie
    """
    url = 'https://cas.dgut.edu.cn/home/Oauth/getToken/appid/illnessProtectionHome/state/home.html'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
    }
    response = requests.get(url=url, headers=headers)
    print('在', sys._getframe().f_code.co_name, "函数的response状态:\n", response)
    cookies = re.search(r'PHPSESSID=(.*)', str(response.cookies))

    if response.ok:
        cookies = cookies.group()[10:36]
        return response, cookies


def SearchToken(html_str, DWN: DataWeNeed):
    """
    正则表达式匹配token
    :param html_str（未经处理过的页面代码）:
    :return: 处理过匹配到的token
    """
    html_str = etree.HTML(html_str)
    li_list = html_str.xpath('/html/body/script[7]/text()')
    result = re.search(r'var token =(.*)', li_list[0])
    DWN.token = (result.group()[13:-2])
    return DWN.token


def GetAuth(DWN: DataWeNeed):
    """
    获取Authentication
    :return:
    """
    global userID
    global passwd
    if len(userID) == 0 or len(passwd) == 0:
        raise AttributeError("请他妈的填写账号密码")
    url = 'https://cas.dgut.edu.cn/home/Oauth/getToken/appid/illnessProtectionHome/state/home.html'
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        "Origin": "https://cas.dgut.edu.cn",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://cas.dgut.edu.cn/home/Oauth/getToken/appid/illnessProtectionHome/state/home.html",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "languageIndex=0; last_oauth_appid=illnessProtectionHome; last_oauth_state=home; PHPSESSID=" + DWN.cookies
    }

    data = {
        'username': userID,
        'password': passwd,
        '__token__': DWN.token
    }
    response = requests.post(url=url, headers=headers, data=data)
    f = json.loads(response.json())
    response2 = requests.get(f['info'])
    print('在', sys._getframe().f_code.co_name, "函数的response状态:\n", response2)
    Auth = 'Bearer ' + response2.history[0].headers['Location'][22:]
    return Auth


@RetryMethodWhenFail
def GetBaseInfo_Raw(DWN: DataWeNeed):
    """
    获取未处理过的表单信息
    :return:
    """
    url = 'https://yqfk.dgut.edu.cn/home/base_info/getBaseInfo'
    headers = {
        "Accept": "application/json",
        "authorization": DWN.Auth,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://yqfk.dgut.edu.cn/main",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "_ga=GA1.3.1085698636.1567594517; UM_distinctid=17666b41075c41-0d0f1aed6335ee-5a301e42-1fa400-17666b41076ab6; _gid=GA1.3.747935397.1608554081; PHPSESSID=" + DWN.cookies
    }

    response = requests.get(url=url, headers=headers)
    print('在', sys._getframe().f_code.co_name, "函数的response状态:\n", response)
    baseInfo_json = json.loads(response.text)
    return baseInfo_json


# @testResultGetBaseInfo_json
def GetBaseInfo_json(DWN: DataWeNeed):
    """
    主API，处理表单信息,并写入文件，如果文件已存在则在文件中读
    :return: 处理过的表单信息，可以直接当做header
    """
    baseinfo = DWN.baseInfo['info']
    del baseinfo["whitelist"]
    del baseinfo["msg"]
    # del baseinfo['importantAreaMsg']
    flag = True
    while flag:
        try:
            with open('baseInfo' + userID + '.json', 'r', encoding='utf8') as f:
                content = f.read()

                if len(content) == 0:
                    raise FileNotFoundError
                content_json = json.loads(content)
                today = datetime.date.today()
                offset = datetime.timedelta(days=1)
                CN_Today = (today + offset).__str__()
                content_json["submit_time"] = CN_Today
                flag = False
        except FileNotFoundError:
            with open('baseInfo' + userID + '.json', 'w', encoding='utf8') as f:
                print('第一次运行吗？\n保存数据')
                json.dump(baseinfo, f)
    return content_json
def WebAPI():
    url='https://webapi.amap.com/count?type=loc&k=41e30b288c35c7b21f1c795a3204aa70&u=https%253A%252F%252Fyqfk.dgut.edu.cn%252Fmain&m=0&pf=windows&suc=success&cbk=jsonp_199939_&platform=JS&logversion=2.0&appname=https%3A%2F%2Fyqfk.dgut.edu.cn%2Fmain&csid=534485E8-11EE-4C08-8E55-660EC7A77685&sdkversion=1.4.15'
    headers={
        "method" : "GET",
        "authority" : "webapi.amap.com",
        "scheme" : "https",
        "path" : "/count?type=loc&k=41e30b288c35c7b21f1c795a3204aa70&u=https%253A%252F%252Fyqfk.dgut.edu.cn%252Fmain&m=0&pf=windows&suc=success&cbk=jsonp_199939_&platform=JS&logversion=2.0&appname=https%3A%2F%2Fyqfk.dgut.edu.cn%2Fmain&csid=534485E8-11EE-4C08-8E55-660EC7A77685&sdkversion=1.4.15",
        "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75",
        "accept" : "*/*",
        "sec-fetch-site" : "cross-site",
        "sec-fetch-mode" : "no-cors",
        "sec-fetch-dest" : "script",
        "referer" : "https://yqfk.dgut.edu.cn/",
        "accept-encoding" : "gzip, deflate, br",
        "accept-language" : "zh-CN,zh;q=0.9",
    }
    response=requests.get(url,headers)
    print('在', sys._getframe().f_code.co_name, "函数的response状态:\n", response)
    print(response.headers)
def RestAPI():
    url='https://restapi.amap.com/v3/assistant/coordinate/convert?coordsys=gps&output=json&s=rsv3&locations=109.27859999999998,22.697&key=41e30b288c35c7b21f1c795a3204aa70&callback=jsonp_470498_&platform=JS&logversion=2.0&appname=https%3A%2F%2Fyqfk.dgut.edu.cn%2Fmain&csid=19B5A8EB-CFDB-41AF-9BE0-39C1B5F0E4C4&sdkversion=1.4.15'
    headers={
            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75",
            "Accept" : "*/*",
            "Sec-Fetch-Site" : "cross-site",
            "Sec-Fetch-Mode" : "no-cors",
            "Sec-Fetch-Dest" : "script",
            "Referer" : "https://yqfk.dgut.edu.cn/",
            "Accept-Encoding" : "gzip, deflate, br",
            "Accept-Language" : "zh-CN,zh;q=0.9",
    }
    response=requests.get(url,headers)
    response=requests.get(url,headers)
    print('在', sys._getframe().f_code.co_name, "函数的response状态:\n", response)
    print(response.headers)
def RestAPI2():
    URL='https://restapi.amap.com/v3/geocode/regeo?key=41e30b288c35c7b21f1c795a3204aa70&s=rsv3&language=zh_cn&location=109.282874,22.69414&extensions=base&callback=jsonp_938422_&platform=JS&logversion=2.0&appname=https%3A%2F%2Fyqfk.dgut.edu.cn%2Fmain&csid=2B167EFE-9E62-4ABB-8385-A1FE0CFC4930&sdkversion=1.4.15'
    headers={
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75",
        "Accept" : "*/*",
        "Sec-Fetch-Site" : "cross-site",
        "Sec-Fetch-Mode" : "no-cors",
        "Sec-Fetch-Dest" : "script",
        "Referer" : "https://yqfk.dgut.edu.cn/",
        "Accept-Encoding" : "gzip, deflate, br",
        "Accept-Language" : "zh-CN,zh;q=0.9",
    }
    response=requests.get(URL,headers)
    print('在', sys._getframe().f_code.co_name, "函数的response状态:\n", response)
    print(response.headers)
def FuckingGPS(DWN: DataWeNeed):
    url = 'https://yqfk.dgut.edu.cn/home/base_info/getGPSAddress?longitude=109.282874&latitude=22.69414&reject=1'
    headers = {
        "Accept": "application/json",
        "authorization": DWN.Auth,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://yqfk.dgut.edu.cn/main",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "PHPSESSID="+DWN.cookies,
        'Content-Type': 'application / json; charset = utf - 8',
        'Host':'yqfk.dgut.edu.cn',
        'Connection':'keep-alive'
    }
    response=requests.get(url,headers)
    print('在', sys._getframe().f_code.co_name, "函数的response状态:\n", response)
    print(response.text)

def AutoDaily_Attendance(DWN: DataWeNeed):
    WebAPI()
    RestAPI()
    RestAPI2()
    FuckingGPS(DWN)
    url = 'https://yqfk.dgut.edu.cn/home/base_info/addBaseInfo'
    headers = {
        # 'Connection':'keep-alive',
        "Accept": "application/json",
        "Content-Type": "application/json; charset=utf-8",
        "authorization": DWN.Auth,
        # "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        # "Origin":"https://yqfk.dgut.edu.cn",
        # "Sec-Fetch-Site":"same-origin",
        # "Sec-Fetch-Mode":"cors",
        # "Sec-Fetch-Dest":"empty",
        "Referer": "https://yqfk.dgut.edu.cn/main",

        # "Accept-Language":"zh-CN,zh;q=0.9",

    }
    data = DWN.baseInfo
    response = requests.post(url, headers=headers, json=data)
    print('在', sys._getframe().f_code.co_name, "函数的response状态:\n", response)

    print(response.text)
    if response.text.find('提交异常') != -1:

        times = 0
        while True:
            time.sleep(3)
            response = requests.post(url, headers=headers, json=data)
            print(response.text)
            if response.text.find('提交异常') == -1 or times > 10:
                break
            times += 1


DWN = DataWeNeed()
AutoDaily_Attendance(DWN)
