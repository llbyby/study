# -*- coding:utf-8 -*-

import urllib.request
import json
import logging
import xlrd
from xlutils.copy import copy
import xlwt
import sys
import time

touser = ''
agentid = 1000004
corpid = 'ww7d0cf0db2960ee82'
corpsecret = '5bQppGUfU6K_GPLfW95DdQ6TYokStzzcceq90UiI35I'
url = 'https://qyapi.weixin.qq.com'
message = 'hahahaha'

# 工资记录文件地址
path = r'salarynotify.xls'

def ModifyContent(row,col,content,sheet,new_remindbook,path,style):
    # 获取工作表内容
    new_sheet = new_remindbook.get_sheet(0)
    # 写入数据
    new_sheet.write(row,col,content,style)
    # 保存文件
    new_remindbook.save(path)

class WorkWx:
    def __init__(self, url, corpid, corpsecret):
        token_url = '%s/cgi-bin/gettoken?corpid=%s&corpsecret=%s' % (url, corpid, corpsecret)
        self.token = json.loads(urllib.request.urlopen(token_url).read().decode())['access_token']

    def send_message(self, url, data):
        send_url = '%s/cgi-bin/message/send?access_token=%s' % (url, self.token)
        self.respone = urllib.request.urlopen(urllib.request.Request(url=send_url, data=data)).read()
        x = json.loads(self.respone.decode())['errcode']
        print(x)
        if x == 0:
            print('Succesfully')

    def messages(self, message):
        values = {
            "touser": 'lvle',
            "msgtype": 'text',
            "agentid": agentid,
            "text": {'content': 'hahahahaha'},
            "safe": 0
        }
        return self.send_message(url, bytes(json.dumps(values), 'utf-8'))

if __name__ == '__main__':
    obj = WorkWx(url, corpid, corpsecret)
    ret = obj.messages(message)
