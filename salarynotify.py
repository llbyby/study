# -*- coding:utf-8 -*-

import urllib.request
import json
import logging
import xlrd
from xlutils.copy import copy
import xlwt
import sys
import time
import uuid

operator = '彭总'
macaddress = '00:09:0f:fe:00:01'
touser = ''
agentid = 1000004
corpid = 'ww7d0cf0db2960ee82'
corpsecret = '5bQppGUfU6K_GPLfW95DdQ6TYokStzzcceq90UiI35I'
url = 'https://qyapi.weixin.qq.com'
message = ''

logging.basicConfig(level=logging.DEBUG, filename='salarynotify.log',
                    format='%(asctime)s - %(levelname)s: %(message)s')

# 工资记录文件地址
path = r'salarynotify.xls'

#获取本地MAC地址
def get_mac_address():
    mac=uuid.UUID(int = uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e+2] for e in range(0,11,2)])

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
        if x == 0:
            logging.debug('发送成功\n%s\n%s' % (touser, message))
            return 'Succesfully'
        else:
            logging.debug('微信接口返回失败码\n%s\n%s\n%s' % (x, touser, message))
            sys.exit(0)

    def messages(self, touser, message):
        values = {
            "touser": touser,
            "msgtype": 'text',
            "agentid": agentid,
            "text": {'content': message},
            "safe": 0
        }
        return self.send_message(url, bytes(json.dumps(values), 'utf-8'))

if __name__ == '__main__':
    #MAC地址校验
    mymac = get_mac_address()
    if mymac != macaddress:
        print('本软件仅供%s使用' % operator)
        input('按任意键退出...')
        sys.exit(0)
    #密码校验
    password = input('请输入密码：')
    if password != '2803prinT':
        print('密码错误！')
        input('按任意键退出...')
        sys.exit(0)
    #问候语
    print('%s您好，现在开始发送，请不要关闭窗口' % operator)
    # 文件占用标志
    occupy = False
    # 打开excel文件，获取文件属性信息
    try:
        remindbook = xlrd.open_workbook(path, formatting_info=True)
    except:
        logging.debug('任务表打开失败')
        sys.exit(0)
    sheet = remindbook.sheet_by_index(0)
    nrows = sheet.nrows
    # 建立副本
    new_remindbook = copy(remindbook)
    # 执行一次表格扫描
    for i in range(2, nrows):
        # 如果已发送，直接跳过
        if sheet.cell(i, 11).value == '是':
            continue
        # 消息拼装
        touser = sheet.cell(i, 0).value
        message = '亲爱的' + str(sheet.cell(i, 0).value) +'，您本月的薪金明细如下：\n' \
        '粮期：' + str(sheet.cell(i, 1).value) + '~' + sheet.cell(i, 2).value + '\n' \
        '标准工资：' + str(sheet.cell(i, 3).value) + '\n' \
        '绩效工资：' + str(sheet.cell(i, 4).value) + '\n' \
        '午膳津贴：' + str(sheet.cell(i, 5).value) + '\n' \
        '供强基金：' + str(sheet.cell(i, 6).value) + '\n' \
        '其他收入：' + str(sheet.cell(i, 7).value) + '\n' \
        '扣病事假：' + str(sheet.cell(i, 8).value) + '\n' \
        '实际发放：' + str(sheet.cell(i, 9).value) + '\n' \
        '备注：' + str(sheet.cell(i, 10).value)
        # style0
        style0 = xlwt.XFStyle()
        # 设置单元格背景颜色
        pattern = xlwt.Pattern()
        pattern.pattern = 1
        pattern.pattern_fore_colour = 22
        style0.pattern = pattern
        # 字体设置
        font = xlwt.Font()
        font.name = '仿宋_GB2312'
        font.colour_index = 1
        font.height = 280
        style0.font = font
        # 边框设置
        borders = xlwt.Borders()
        borders.left = xlwt.Borders.THIN
        borders.right = xlwt.Borders.THIN
        borders.top = xlwt.Borders.THIN
        borders.bottom = xlwt.Borders.THIN
        style0.borders = borders
        # 为已发送事项添加背景色（按指定格式重填）
        try:
            ModifyContent(i, 0, sheet.cell(i, 0).value, sheet, new_remindbook, path, style0)
        except:
            logging.debug('背景色添加失败\n%s' % touser)
            sys.exit(0)
        # style
        style = xlwt.XFStyle()
        # 设置单元格字体、颜色、字号
        font = xlwt.Font()
        font.name = '仿宋_GB2312'
        font.colour_index = 0
        font.height = 280
        font.bold = False
        style.font = font
        # 设置单元格对齐方式
        alig = xlwt.Alignment()
        alig.horz = xlwt.Alignment.HORZ_CENTER
        alig.vert = xlwt.Alignment.VERT_CENTER
        style.alignment = alig
        # 边框设置
        borders = xlwt.Borders()
        borders.left = xlwt.Borders.THIN
        borders.left = xlwt.Borders.THIN
        borders.right = xlwt.Borders.THIN
        borders.top = xlwt.Borders.THIN
        borders.bottom = xlwt.Borders.THIN
        style.borders = borders
        # 发送消息
        try:
            obj = WorkWx(url, corpid, corpsecret)
            ret = obj.messages(touser, message)
        except:
            logging.debug('发送失败\n%s' % touser)
            sys.exit(0)
        # 按照指定格式写入数据
        try:
            ModifyContent(i, 11, '是', sheet, new_remindbook, path, style)
            time.sleep(2)
        except:
            logging.debug('标记发送状态失败\n%s' % touser)
            sys.exit(0)
        #2秒间隔
        time.sleep(2)