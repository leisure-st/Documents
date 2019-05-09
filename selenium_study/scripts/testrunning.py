# -*- encoding=utf8 -*-
__author__ = "Administrator"

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
from common import *
from saleAnalysis import *
from login import *
from handheldReimbursement import *
from saleReport import *
from plannerAssistant import *
from Amoeba import *
from mobileReimb import *




orgName=('销售公司','机加事业部','变电器公司')
allOrgName=('销售公司','机加事业部','变电器公司','蓝海机械总公司','蓝海柴油机公司','蓝海柴油机本部','总装事业部','深圳销售公司')

mailto_list = ['1175746962@qq.com','121036992@qq.com','3272959045@qq.com']           # 收件人(列表)
# mail_host = "smtp.qq.com"            # 使用的邮箱的smtp服务器地址，这里是qq的smtp地址
# mail_user = "121036992"                           # 用户名
# mail_pass = "leisure1234"                             # 密码
# mail_postfix = "qq.com" 
sub='自动化测试报告'
content='content  content'


try:
    #登陆移动端
    # login_mobile(mobDriver,USERNAME,PASSWORD)
    # mobDriver.implicitly_wait(2)
    # time.sleep(4)
    login_pc(PCDriver,USERNAME,PASSWORD)
   
    mobileReimbfirstLeverTest(mobDriver,PCDriver)


  

finally:
    Log("一级测试用例执行完毕")
    print("一级测试用例执行完毕")
    # mobDriver.close()
    # PCDriver.close()
    

