# 导入模块
import xlrd
from xlutils.copy import copy
import xlwt
import itchat
import datetime
import time
# 使用手机扫描二维码登录微信
def WeChatLogin():
    itchat.login()
# 给指定好友发送指定内容的消息
def SendAMessage(friend, message):
    users = itchat.search_friends(name=friend)
    userName = users[0]['UserName']
    itchat.send(message, toUserName = userName)
# 按照指定格式修改excel表格内容
def ModifyContent(row,col,content,sheet,new_remindbook,path,style):
    # 获取工作表内容
    new_sheet = new_remindbook.get_sheet(0)
    # 写入数据
    new_sheet.write(row,col,content,style)
    # 保存文件
    new_remindbook.save(path)
# 判断提醒是否过期
def Overdue(nowtime,deadtime):
    if deadtime < nowtime:
        return True
    else:
        return False
# 程序运行主体
if __name__=='__main__':
    #问候语
    print('Hello,PICCHKer^-^')
    # 首次执行标志
    first_exec = True
    # 微信登录
    WeChatLogin()
    # 指定微信消息推送好友
    #friend = '***'
    # 备忘本记录文件地址
    path = r'wechatnotify.xls'
    # 扫描备忘本记录
    while True:
        # 文件占用标志
        occupy = False
        # 打开excel文件，获取文件属性信息
        try:
            remindbook = xlrd.open_workbook(path, formatting_info=True)
        except:
            print('任务表打开失败')
            time.sleep(10)
            continue
        sheet = remindbook.sheet_by_index(0)
        nrows = sheet.nrows
        # 建立副本
        new_remindbook = copy(remindbook)
        # 初始化事项序号
        mark = 1
        # 初始化message信息
        message = '微信提醒测试：'
        # 执行一次备忘本扫描
        for i in range(2, nrows):
            # 如果已办结事项或者空事项，直接跳过
            if sheet.cell(i, 3).value == '是' or sheet.cell(i, 1).value == '':
                continue
            # 获取事项截止时间
            deadtime = xlrd.xldate.xldate_as_datetime(sheet.cell(i, 1).value, 0)
            deadhour = deadtime.strftime('%H:%M')
            # 获取当前时间
            nowtime = datetime.datetime.now()
            nowhour = nowtime.strftime("%H:%M")
            # 如果过期，则将过期标志设置为是
            if Overdue(nowtime, deadtime):
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
                # 为过期事项添加背景色（按指定格式重填）
                try:
                    ModifyContent(i, 0, sheet.cell(i, 0).value, sheet, new_remindbook, path, style0)
                except:
                    occupy = True
                    print(nowtime)
                    print('背景色添加失败：' + sheet.cell(i, 0).value)
                    time.sleep(2)
                    break
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
                    SendAMessage(sheet.cell(i, 2).value, sheet.cell(i, 0).value)
                    print(nowtime)
                    print('成功：' + sheet.cell(i, 0).value)
                    time.sleep(2)
                except:
                    print(nowtime)
                    print('消息发送失败：' + sheet.cell(i, 0).value)
                    time.sleep(2)
                    break
                # 按照指定格式写入数据
                try:
                    ModifyContent(i, 3, '是', sheet, new_remindbook, path, style)
                    time.sleep(2)
                except:
                    occupy = True
                    print(nowtime)
                    print('文件写入失败：' + sheet.cell(i, 0).value)
                    time.sleep(2)
                    break
        #每分钟轮询一次
        time.sleep(60)