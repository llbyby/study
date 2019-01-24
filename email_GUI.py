# -*- coding: utf-8 -*-
# Import the email modules we'll need
import smtplib
from email.mime.text import MIMEText
from tkinter import *
import tkinter.messagebox
import sys
import importlib

# 定义邮件管理窗口类
class MailGUI:
    def __init__(self):
        self.root = Tk()
        self.root.title('邮件发放器')
        workArea = Frame(self.root, width=500, height=500)
        workArea.pack()
        # 初始化窗口
        labelframe = LabelFrame(workArea, padx=5, pady=10)  # text can empty
        labelframe.pack(fill='both')
        # 发送按钮
        btn_frame = Frame(labelframe, width=400, height=50, bg='#CCCCCC')
        btn_frame.pack(fill='y')
        sand_btn = Button(btn_frame, text='发送', padx=3, pady=2,state='active', command=self.runSendMail)
        sand_btn.pack()
        # 定义变量，保存客户输入结果
        self.v_subject = StringVar()
        self.v_receiver = StringVar()
        self.v_content = StringVar()

        # 接收人
        receiver_frame = Frame(labelframe, width=400, height=50)
        receiver_frame.pack(fill='y')
        Label(receiver_frame, width=20, pady=5, justify='left', text='接收人').pack(side='left')
        Entry(receiver_frame, width=50, textvariable=self.v_receiver).pack(side='left')
        # 主题
        subject_frame = Frame(labelframe, width=400, height=50)
        subject_frame.pack(fill='y')
        Label(subject_frame, width=20, pady=5, justify='left', text='主题  ').pack(side='left')
        Entry(subject_frame, width=50, textvariable=self.v_subject).pack(side='right')
        # 邮件内容
        content_frame = Frame(labelframe, width=400, height=50)
        content_frame.pack(fill='y')
        Label(content_frame, width=20, pady=5, justify='left', text='内容  ').pack(side='left')
        self.T_content = Text(content_frame, width=38, height=4)
        self.T_content.pack(side='right')
        self.root.mainloop()

    def runSendMail(self):
        # tkMessageBox.askquestion(title='发送邮件',message='发送?')
        receiver = self.v_receiver.get()
        sub = self.v_subject.get()
        to_list = receiver.split(',')
        content = str(self.T_content.get('0.0', END)).strip()
        self.initSMTP('xxxxx', '@sina.com', '发信人密码')
        self.sendMail(sub, to_list, content)
        tkinter.messagebox.showinfo(title='系统提示', message='发送成功')

    def initSMTP(self, mail_user, mail_server_name, mail_password):
        self.mail_user = mail_user + mail_server_name
        self.mail_password = mail_password
        self.mail_server_name = mail_server_name
        self._smtp = smtplib.SMTP_SSL()
        self._smtp.connect(self.findMailServer())
        self._smtp.login(self.mail_user, self.mail_password)

    def sendMail(self, sub, to_list, mail_body):
        msg = MIMEText(mail_body, _subtype='plain', _charset='utf-8')
        msg["Accept-Language"] = "zh-CN"
        msg["Accept-Charset"] = "ISO-8859-1,utf-8"
        msg['Subject'] = sub
        msg['From'] = self.mail_user
        msg['To'] = ";".join(to_list)
        self._smtp.sendmail(self.mail_user, to_list, msg.as_string())
        self._smtp.quit()

    def findMailServer(self):
        server_name = str(self.mail_server_name).strip()
        server_dict = {'@sina.com': 'smtp.sina.com',
                       '@126.com': 'smtp.126.com',
                       '@163.com': 'smtp.163.com',
                       '@qq.com': 'smtp.qq.com'}
        return server_dict[server_name]

try:
    importlib.reload(sys)
    MailGUI()
except Exception as e:
    print(e)