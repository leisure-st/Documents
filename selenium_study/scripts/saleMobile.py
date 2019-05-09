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
from login import *
#autotester用户的联系对象业务员：张岳明
#进入销售员报表（业绩）
linkObject="张岳明"   #用户对应的联系对象
def openSaleReport(driver):
    driver.get("http://v-mobile-at/k3cloud/mobile/k3cloud.html?entryrole=XT&formId=Sal_NewMobileConsole&formType=mobileform&appid=10694")#进入移动销售
    time.sleep(10)
    Log("进入移动销售")
    time.sleep(6)

#下单