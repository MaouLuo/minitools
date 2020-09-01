# -*- coding:utf-8 -*-
# 插件工具集合库

import datetime
import configparser 
import requests
import json
import time
import hmac
import hashlib
import base64
import urllib.parse


# 配置文件读取
# item为所用api类型，path为配置文件所在路径, name为密钥字段
def r_conf(item, path='D:\\code\\config.ini', name='token'):
    config = configparser.ConfigParser()
    config.read(path, encoding='utf-8')
    cont = config.get(item, name)
    return cont


# 工作日判断
# 参数date为需判断的日期，api密钥含appkey和sign
def work_day(date, appkey, sign):
    url = 'http://api.k780.com'
    data = {
        'app': 'life.workday',
        'date': date,
        'appkey': appkey,
        'sign': sign,
        'format': 'json'
    }
    resp = requests.post(url, data=data)
    jd = json.loads(resp.text)
    if jd['result']['workmk'] == '1': # 工作日
        return True
    elif jd['result']['workmk'] == '2': # 休息日
        return False


# 获取当前时间格式，参数layout为所需输出格式字符串，常用格式如下
'''
%a 当地工作日的缩写。Sun, Mon, ..., Sat (en_US);
%A 本地化的星期中每日的完整名称。Sunday, Monday, ..., Saturday (en_US);
%w 以十进制数显示的工作日，其中0表示星期日，6表示星期六。0, 1, ..., 6
%d 补零后，以十进制数显示的月份中的一天。01, 02, ..., 31
%b 当地月份的缩写。Jan, Feb, ..., Dec (en_US);
%B 本地化的月份全名。January, February, ..., December (en_US);
%m 补零后，以十进制数显示的月份。01, 02, ..., 12
%y 补零后，以十进制数表示的，不带世纪的年份。00, 01, ..., 99
%Y 十进制数表示的带世纪的年份。0001, 0002, ..., 2013, 2014, ..., 9998, 9999
%H 以补零后的十进制数表示的小时（24 小时制）。00, 01, ..., 23
%I 以补零后的十进制数表示的小时（12 小时制）。01, 02, ..., 12
%p 本地化的 AM 或 PM 。AM, PM (en_US);
%M 补零后，以十进制数显示的分钟。00, 01, ..., 59
%S 补零后，以十进制数显示的秒。00, 01, ..., 59
%f 以十进制数表示的微秒，在左侧补零。000000, 000001, ..., 999999
%z UTC 偏移量，格式为 ±HHMM[SS[.ffffff]] （如果是简单型对象则为空字符串）。
%Z 时区名称（如果对象为简单型则为空字符串）。(空), UTC, EST, CST
%j 以补零后的十进制数表示的一年中的日序号。001, 002, ..., 366
%U 以补零后的十进制数表示的一年中的周序号（星期日作为每周的第一天）。 在新的一年中第一个星期日之前的所有日子都被视为是在第 0 周。00, 01, ..., 53
%W 以十进制数表示的一年中的周序号（星期一作为每周的第一天）。 在新的一年中第一个第期一之前的所有日子都被视为是在第 0 周。00, 01, ..., 53
%c 本地化的适当日期和时间表示。Tue Aug 16 21:30:00 1988 (en_US);
%x 本地化的适当日期表示。08/16/88 (None);08/16/1988 (en_US);
%X 本地化的适当时间表示。21:30:00 (en_US);
%% 字面的 '%' 字符。%
'''
def get_date(layout='%Y%m%d%H%M'):
    now_time = datetime.datetime.now()
    #time_str = datetime.datetime.strftime(now_time,'%H%M')
    date = now_time.strftime(layout)  
    return date


# 通过server酱发送公众号消息。每分钟相同内容只能发一次，相同内容包括标题和正文
# 调试模式仅打印不发微信
class ServerJ:
    def __init__(self, title, cont, token, debug=True): 
        self.url = 'https://sc.ftqq.com/'
        self._token = token
        self.title = title
        self.cont = cont
        self.debug = debug
  
    def check(self):
        title, cont = False, False
        print('title:{},\r\n cont:{}'.format(self.title, self.cont))
        if self.title:
            title = self.title
        if self.cont:
            cont = self.cont
        return {'title':title, 'cont':cont}

    def run(self):
        if self.cont is False:
            cont = 'No Data.'
        else:
            cont = self.cont
        
        data = {
            'text': self.title, # 消息标题，最长为256，必填
            'desp': cont # 消息内容，最长64Kb，可空，支持MarkDown。
        }
        if self.debug is True:
            print(data)
        else:
            try:
                resp = requests.post(self.url+self._token, data=data)
            except:
                print(resp.text)
        return True

# 通过钉钉群机器人发送消息，该群为免费电话内部个人群
class Dingding():
    def __init__(self, *path):
        if path:
            self.secret = r_conf(item='dingding', path=path[0], name='secret')
            
        else:            
            self.secret = r_conf(item='dingding', name='secret')
        
        self.headers = {
            'Content-Type': 'application/json',
        }

    def get_url(self):
        timestamp = str(round(time.time() * 1000))
        self.secret = 'SECd815f97f9b5f3ddf04eb6f85ab7bfd3f64cb992968d7a0690d511ba2bc6d3ba5'
        secret_enc = self.secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, self.secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        url = 'https://oapi.dingtalk.com/robot/send?access_token=796719934a205fb55623f2887305dcbaf31414e661117eb28f4bd140597a27b7&timestamp={}&sign={}'.format(timestamp, sign)
        #print(timestamp)
        #print(sign)
        return url

    def send_text(self, cont):
        data = {
            "msgtype":"text",
            "text":{
                "content": cont#"吃饭时间到啦~\n当前天气{}，气温{}".format(wea['wtNm'], wea['wtTemp']),
                #"mentioned_list":["@all"]
                }
        }
        requests.post(self.get_url(), headers=self.headers, data=json.dumps(data))