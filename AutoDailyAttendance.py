# author: HRH_theRenegade

# date: 2021/1/18

# PyCharm
import datetime
import json
import requests
import re

if __name__ == '__main__':

    myUserName = input()
    myPassword = input()

    # 0.模拟信息登录反反爬
    UserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"

    # 1. 请求中央认证
    # 1.1 请求页面
    URL1 = 'https://cas.dgut.edu.cn/home/Oauth/getToken/appid/illnessProtectionHome/state/home'
    headers1 = {
        "User-Agent": UserAgent
    }
    response1 = requests.get(url=URL1, headers=headers1)
    # 1.2 获取cookies - 即将授权的页面
    PHPSESSID1 = re.search(r'PHPSESSID=(.*)', str(response1.cookies)).group()[10:36]
    # 1.3 获取Token - 中央认证系统
    html1 = response1.text
    varIndex = html1.rfind("var token = ")
    firstCharIndex = html1.find('"', varIndex)
    Token1 = html1[firstCharIndex + 1:html1.find('"', firstCharIndex + 1)]

    # 2. 登录中央认证
    URL2 = "https://cas.dgut.edu.cn/home/Oauth/getToken/appid/illnessProtectionHome/state/home"
    headers2 = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": UserAgent,
        "Origin": "https://cas.dgut.edu.cn",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": URL2,
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "languageIndex=0; last_oauth_appid=illnessProtectionHome; last_oauth_state=home; PHPSESSID=" + PHPSESSID1
    }
    data2 = {
        'username': myUserName,
        'password': myPassword,
        '__token__': Token1
    }
    response2 = requests.post(url=URL2, headers=headers2, data=data2)
    # 提取access_token - 授权疫情防空登录
    infoJson = json.loads(response2.json())['info']
    accessTokenStr = requests.get(infoJson).history[0].headers['Location']
    firstCharIndex = accessTokenStr.find("=", accessTokenStr.rfind("access_token"))
    accessToken = accessTokenStr[firstCharIndex + 1:]
    authorization3 = 'Bearer ' + accessToken

    # 3.携带 access_token 登录 yqfk.dgut.edu.cn
    URL3 = 'https://yqfk.dgut.edu.cn/home/base_info/getBaseInfo'
    headers3 = {
        "Accept": "application/json",
        "authorization": authorization3,
        "User-Agent": UserAgent,
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://yqfk.dgut.edu.cn/main",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "PHPSESSID=" + PHPSESSID1
    }
    response3 = requests.get(url=URL3, headers=headers3)
    baseInfoJson = json.loads(response3.text)
    msg = str(baseInfoJson["info"]["msg"])
    print(msg)

    if "尚未" in msg:
        # 4. 准备打卡
        data4 = baseInfoJson["info"]  # 个人信息数据
        today = datetime.date.today()
        offset = datetime.timedelta(days=1)
        CN_Today = (today + offset).__str__()
        data4["submit_time"] = CN_Today
        print(data4["submit_time"])
        data4 = json.dumps(data4)
        URL4 = 'https://yqfk.dgut.edu.cn/home/base_info/addBaseInfo'
        headers4 = {
            "Accept": "application/json",
            "authorization": authorization3,
            "Content-Type": "application/json; charset=utf-8",
            "Referer": "https://yqfk.dgut.edu.cn/main",
            "sec-ch-ua-mobile": '?0',
            "User-Agent": UserAgent
        }
        response4 = requests.post(URL4, headers=headers4, data=data4)

        # 5. 检查是否打卡成功
        response5 = requests.get(url=URL3, headers=headers3)
        baseInfoJson = json.loads(response5.text)
        print(response4.text)
        print(baseInfoJson["info"]["msg"])
