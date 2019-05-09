# -*- encoding=utf8 -*-
__author__ = "Administrator"

import os
import time
import unittest as ut
from selenium import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options    #
import re
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from common import *
#from selenium import webdriver

# option=Options()
# option.add_argument('-headless')
# PCDriver=webdriver.Chrome(chrome_options=option)

# mobDriver=webdriver.Chrome(chrome_options=option)

# #mobile driver
mobDriver = webdriver.Chrome()
mobDriver.implicitly_wait(3)
mobDriver.maximize_window()

# mobile_emulation = {"deviceName":"iPhone 6/7/8"}  #设置以手机模式浏览
# options = Options()
# options.add_experimental_option("mobileEmulation", mobile_emulation)
# mobDriver = webdriver.Chrome(chrome_options=options)


#pc driver
PCDriver = webdriver.Chrome()
PCDriver.implicitly_wait(3)
PCDriver.maximize_window()

USERNAME='autotester'
PASSWORD='888888'
PCURL= 'http://v-mobile-at/k3cloud/html5/'    #http://172.20.178.100/k3Cloud/html5/
MOBURL = 'http://v-mobile-at/k3cloud/mobile/'

def login_mobile(driver,USERNAME,PASSWORD):
    driver.get(MOBURL)
    if is_element_exist(driver,"#login"):#判断是否打开移动工作台
        Log("移动工作台加载成功")     
    driver.find_element_by_id("username").click()
    driver.find_element_by_id("username").clear()
    driver.find_element_by_id("username").send_keys(USERNAME)
    driver.find_element_by_id("userpassword").click()
    driver.find_element_by_id("userpassword").send_keys(PASSWORD)
    driver.find_element_by_xpath("//a[@onclick='kdloginbtnClick(arguments[0])']").click()
    Log(USERNAME+'登陆成功！')                 #["移动工作台登录成功\n", USERNAME+"\n",PASSWORD+"\n"]
    
#login_mobile(driver,USERNAME,PASSWORD)
    
def login_pc(driver,USERNAME,PASSWORD):
    driver.get(PCURL)
    time.sleep(10.0)
    driver.find_element_by_css_selector('div[class="boxtitle"]>span').click()#点击切换账号登录 
    time.sleep(10.0)
    #driver.find_element_by_xpath("//input[@data-role='autocomplete']").click()
    #driver.find_element_by_xpath("//input[@data-role='autocomplete']").clear()
    driver.find_element_by_css_selector('input[id="user"]').clear()
    driver.find_element_by_css_selector('input[id="user"]').send_keys(USERNAME)
    #driver.find_element_by_xpath("//input[@style='height: 53px;width:287px;']").click()
    driver.find_element_by_css_selector('input[id="password"]').send_keys(PASSWORD)
    #driver.find_element_by_xpath("//input[@style='height: 53px;width:287px;']").send_keys(PASSWORD)
    #driver.find_element_by_xpath("//button[@data-role='button']").click()
    driver.find_element_by_css_selector('button[id="btnLogin"]').click()#点击登录
    if is_element_exist(driver,"#wholemessage_wnd_title"):#判断是否已有账号登录
        #driver.find_element_by_xpath("//button[@role='kdmsgBtton']").click()
        driver.find_element_by_css_selector('button[role="kdmsgBtton"]').click()  #class="k-button"
    Log("pc端"+USERNAME+"登录成功")