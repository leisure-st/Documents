import os
import time
import unittest as ut
from selenium import *
from selenium import webdriver
import re
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication 
#from selenium import JavascriptExecutor


FILEPATH="D:\\autotest-log\\chrome"#输出log的路径
# host="172.20.200.120"
# port=25
# smtpObj = smtplib.SMTP( [host [, port [, local_hostname]]] )   #

#mailto_list = ['1175746962@qq.com','121036992@qq.com']          # 收件人(列表)
mail_host = "smtp.qq.com"            # 使用的邮箱的smtp服务器地址，这里是qq的smtp地址
mail_user = "121036992"                           # 用户名
mail_pass = "txjcjsgxkifhbjfc"                             # 密码需要使用开启smtp之后的授权码
mail_postfix = "qq.com"  # 邮箱的后缀


def send_mail(to_list, sub, content):
    date=time.strftime('%Y-%m-%d',time.localtime())
    me = mail_user+"@"+mail_postfix
    new_report = ["D:\\autotest-log\\chrome" + date+".txt", "log.html"]#发送当天生成的自动化测试log，发送过来是按照html的格式
    print(new_report[0])
    msg = MIMEMultipart()
    msg['Subject'] = sub                        # 主题
    msg['From'] = me
    msg['To'] = ";".join(to_list)                # 将收件人列表以‘；’分隔
    # 文本内容
    text_content = MIMEText(content)
    msg.attach(text_content)
    # 附件
    attachment = MIMEApplication(open(new_report[0], 'rb').read())
    attachment.add_header("Content-Disposition", "attachment", filename=new_report[1])
    msg.attach(attachment)
    try:
        server = smtplib.SMTP(mail_host, timeout=30)
        server.set_debuglevel(1)
        server.starttls()
        server.login(mail_user, mail_pass)               
        server.sendmail(me, to_list, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(str(e))
        return False

def send_mailList(sendAmount,mailto_list, sub, content):
    for i in range(sendAmount):                             # 发送1封，上面的列表是几个人，这个就填几这里等于1的时候为什么第二封也发送出去了？
        if send_mail(mailto_list[i], sub, content):  # 邮件主题和邮件内容
            print("done!")
        else:
            print("failed!")




def WriteLog(msg,date):
    global FILEPATH
    fo = open(FILEPATH+date+".txt", 'a+')#按日期创建log，有则直接打开
    fo.writelines(msg)
    fo.flush()
    fo.close()

def Log(msg = ''):
    currentDateTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
    date=time.strftime('%Y-%m-%d',time.localtime())
    if msg == '':
        log = '\n'
    else:
        log = '[%s]%s\n' % (currentDateTime, msg)
    WriteLog(log,date)


def is_element_exist(driver, css):
    s = driver.find_elements_by_css_selector(css_selector=css)
    if len(s) == 0:
        Log ("元素未找到:%s"%css)
        return False
    elif len(s) == 1:
        return True
    else:
        Log ("找到%s个元素：%s"%(len(s),css))
        return True
def isNum(value):
    try:
        float(value)
    except Exception as e:
        Log("出现异常：")
        print(e)
        return False
    else:
        return True

#首先，用 Javascript 代码高亮显示被操作的元素，高亮的实现方式就是利用 JavaScript 在对象的边框上渲染一个 5-8 个像素的边缘；
#然后，调用 screenshot 函数完成点击前的截图；
#最后，调用 Selenium 原生的 click 函数完成真正的点击操作。
#那么，以后凡是需要调用 click 函数时，都直接调用这个自己封装的 click 函数，直接得到高亮了被操作对象的界面截图。

# def screenClick():

