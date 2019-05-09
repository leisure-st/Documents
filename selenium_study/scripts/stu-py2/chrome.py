# -*- encoding=utf8 -*-
__author__ = "Administrator"

import os
import time
import unittest as ut
from selenium import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from selenium import webdriver

#mobile driver
mobDriver = webdriver.Chrome()
mobDriver.implicitly_wait(3)
mobDriver.maximize_window()
#pc driver
PCDriver = webdriver.Chrome()
PCDriver.implicitly_wait(3)
PCDriver.maximize_window()

SALAMOUNT_XPATH = '//*[@id="app"]/article/header/h2/span'#销售分析销售金额元素路径
USERNAME='autotester'
PASSWORD='888888'
FILEPATH="D:\\airtest-log\\chrome.txt"#输出log的路径
PCURL= 'http://k3cloudmobtest.kingdee.com/k3cloud/html5/'
MOBURL = 'http://k3cloudmobtest.kingdee.com/k3cloud/mobile/'

#pcOrg=
#mobOrg=

def WriteLog(msg):
    global FILEPATH
    fo = open(FILEPATH, 'a+')
    fo.writelines(msg)
    fo.flush()
    fo.close()

def Log(msg = ''):
    currentDateTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
    if msg == '':
        log = '\n'
    else:
        log = '[%s]%s\n' % (currentDateTime, msg)
    WriteLog(log)


def is_element_exist(driver, css):
    s = driver.find_elements_by_css_selector(css_selector=css)
    if len(s) == 0:
        Log (u"元素未找到:%s"%css)
        return False
    elif len(s) == 1:
        return True
    else:
        Log (u"找到%s个元素：%s"%(len(s),css))
        return False
def isNum(value):
    try:
        float(value)
    except Exception as e:
        Log(u"出现异常："+e)
        return False
    else:
        return True
    
def login_mobile(driver,USERNAME,PASSWORD):
    driver.get(MOBURL)
    if is_element_exist(driver,"#login"):#判断是否打开移动工作台
        Log(u"移动工作台加载成功")     
    driver.find_element_by_id("username").click()
    driver.find_element_by_id("username").clear()
    driver.find_element_by_id("username").send_keys(USERNAME)
    driver.find_element_by_id("userpassword").click()
    driver.find_element_by_id("userpassword").send_keys(PASSWORD)
    driver.find_element_by_xpath("//a[@onclick='kdloginbtnClick(arguments[0])']").click()
    Log(USERNAME+u'登陆成功！')                 #["移动工作台登录成功\n", USERNAME+"\n",PASSWORD+"\n"]
    
#login_mobile(driver,USERNAME,PASSWORD)
    
def login_pc(driver,USERNAME,PASSWORD):
    driver.get(PCURL)
    time.sleep(3.0)
    driver.find_element_by_xpath("//*[@id=\"dbox\"]/div/div[2]/span").click()
    time.sleep(5.0)
    driver.find_element_by_xpath("//input[@data-role='autocomplete']").click()
    driver.find_element_by_xpath("//input[@data-role='autocomplete']").clear()
    driver.find_element_by_xpath("//input[@data-role='autocomplete']").send_keys(USERNAME)
    driver.find_element_by_xpath("//input[@style='height: 53px;width:287px;']").click()
    driver.find_element_by_xpath("//input[@style='height: 53px;width:287px;']").send_keys(PASSWORD)
    driver.find_element_by_xpath("//button[@data-role='button']").click()
    if is_element_exist(driver,"#wholemessage_wnd_title"):#判断是否已有账号登录
        driver.find_element_by_xpath("//button[@role='kdmsgBtton']").click()
    
def get_salAmount(driver):
    time.sleep(3)
    driver.find_element_by_xpath("//a[@href='#15']").click()
    time.sleep(5)
    driver.find_element_by_xpath("//a[@href='#16']").click()#点击进入经营分析
    time.sleep(5)
    if is_element_exist(driver, ".amount"):
        #salAmount = driver.find_element_by_xpath(SALAMOUNT_XPATH).text  #销售额
        salAmount=driver.find_element_by_css_selector(".amount").text
        return salAmount
    else:
        Log(u"salAmount不存在")
        return None
    
def filter_scheme(driver):
    time.sleep(3)
    driver.find_element_by_css_selector('span[id$="BILLMENU_TOOLBAR-tbFilter"]').click()#点击过滤方案
    orglist = driver.find_element_by_css_selector('div[id$="Filter-FORGLIST-EDITOR"]>div>span>span>.ui-poplistedit-displayname').text#获取组织选择框的组织列表
    print("=========================================="+orglist+"=========================================")
    if driver.find_element_by_css_selector(".k-item k-itemAll").is_enabled:
        print(u"全部组织")
    else:
        print(u"未选中全部组织")

def get_pcsalAmount(driver):
    wait = WebDriverWait(driver, 20) #实例化一个等待对象 wait
    searchBox = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[@id=\"FSEARCH\"]/span/span/span[2]")))
    searchBox[0].click()
    # driver.implicitly_wait(2)
    # searchBox[0].send_keys('销售订单列表')       ui-poplistedit-displayname
    driver.implicitly_wait(5)
    driver.find_element_by_xpath("//input[@style='width: 120px; padding: 0px; font-size: 12px; height: 24px; margin-left: 30px; border-radius: 2px; opacity: 1; background: rgb(255, 255, 255);']").send_keys(u'销售订单列表')
    time.sleep(5)
    driver.find_element_by_xpath("/html/body/div[2]/div/div/div/li/span[3]").click()
    #pcList=driver.find_element_by_css_selector(".ui-poplistedit-displayname").text
    #pcList=driver.find_element_by_xpath('//*[@id="9d69f105-1c89-4e3d-aa2f-8d1377b6327c-FLIST-pager"]/ul/li[8]/span[1]/span/span/span/span[2]').text
    pcList=int(driver.find_element_by_css_selector("span[data-kdid='sp_2_pagerlist2']").text)
    time.sleep(5)
    if pcList == 0:
        return 0
    else:
        pcSalAmount = driver.execute_script('return $(".kd-grid-sumfooterdiv,div[data-field=\'FALLAMOUNT_LC\']").text()')#这里通过js的方式获取元素还需要多加练习
        if pcSalAmount == "":
            Log(u"pcSalAmount不存在")
            return None
        else:
            return pcSalAmount
    # return pcSalAmount    #pcsalAmount = driver.find_element_by_css_selector(".kd-grid-sumfooterdiv,div[data-field='FALLAMOUNT_LC']").text  #销售订单价税合计数值
    
        
    

#登陆移动端
# login_mobile(mobDriver,USERNAME,PASSWORD)
# mobDriver.implicitly_wait(2)
# salAmount=get_salAmount(mobDriver)
#print(salAmount)

#登陆pc端
login_pc(PCDriver,USERNAME,PASSWORD)
pcSalAmount=get_pcsalAmount(PCDriver)
#print(pcSalAmount)
filter_scheme(PCDriver)

# if salAmount != None and pcSalAmount != None:
#     if isNum(salAmount) and isNum(pcSalAmount):
#         if float(salAmount)==float(pcSalAmount):#两个值相等时，pass
#             Log(u"salAmount与pcsalAmount相等")
#         else:
#             Log(u"salAmount与pcsalAmount不相等")
#     else:
#         Log(u"有元素不为数字，请检查数值")
    
# else:
#     print(u"有不存在的元素")
        
        







