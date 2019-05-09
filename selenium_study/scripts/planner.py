# -*- encoding=utf8 -*-
__author__ = "Administrator"

import os
import time
import unittest as ut
from selenium import *
from selenium import webdriver
import re
#from selenium import we
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from common import *
from login import *

    # WebElement element = driver.findElement(By("element_path"))

    # Actions actions = new Actions(driver)

    # actions.moveToElement(element).click().perform()

#进入计划员助手
def openPlannerAssistant(driver):
    driver.get("http://v-mobile-at/K3Cloud/mobile/k3cloud.html?entryrole=XT&formId=~/KDMobile/PlannerAssistant/index.html&formType=mobileurl&appid=10014")#进入计划员助手
    time.sleep(10)
    Log("进入计划员助手")
    time.sleep(6)

def select_PcFilterScheme(driver,orgName):
    time.sleep(3)
    driver.find_element_by_css_selector('span[id$="BILLMENU_TOOLBAR-tbFilter"]').click()#点击过滤方案
    time.sleep(5)
    # 获取已选组织下拉框对象
    orgSelectedBox = driver.find_element_by_css_selector('div[id$="Filter-FORGLIST-EDITOR"]>div>span>span>.ui-poplistedit-displayname')

    # 获取已选组织列表  注意去掉字符中的空格，会影响匹配
    orgSelectedList = orgSelectedBox.text.replace(' ','').split(',')

    # 点击下拉框 触发组织列表
    orgSelectedBox.click()
    time.sleep(1)

    # 获取下拉组织列表的按钮
    orgChkBoxEles = driver.find_elements_by_css_selector('button[for$="value"]')
    # 修改组织
    PcChangeOrg(orgChkBoxEles, orgSelectedList,orgName)
    time.sleep(3)
    driver.find_element_by_css_selector("a[id$='Filter-FBTNOK_c']").click()#点击确定

# 修改组织列表
def PcChangeOrg(orgChkBoxEles, orgSelectedList, orgName):
    selectedOrgSet = set(orgSelectedList).difference(set(orgName))
    unSelectedOrgSet = set(orgName).difference(set(orgSelectedList))#difference()取出现在第一个集合但不出现在第二个集合的元素  对称差symmetric_difference(y)

    for org in selectedOrgSet:
        [ele.click()  for ele in orgChkBoxEles if ele.text.strip() == org]# strip() 方法用于移除字符串头尾指定的字符（默认为空格或换行符）或字符序列，参数为空，那么会默认删除字符串头和尾的空白字符(包括\n，\r，\t这些)
    
    for org in unSelectedOrgSet:
        [ele.click() for ele in orgChkBoxEles if ele.text.strip() == org]
        
    pass

#生产齐套分析页面获取生产组织以及对应的生产订单条数  不包含结案状态的生产订单
def getPlannerMaterial(driver):
    filterEles=driver.find_elements_by_css_selector('i[class="m-arrow-right"]')   #获取组织选择、过滤方案选择的元素list
    filterEles[1].click()#点击打开过滤方案
    #选择自动化测试通用过滤方案
    for ele in driver.find_elements_by_css_selector('ul[class="as-select as-right"]>li'):
        if ele.text=="自动化测试通用过滤方案":
            ele.click()
            break
    
    time.sleep(20)
    #获取所有可选择的组织
    orgName=[]
    orderitem=[]
    productDict={}
    #获取组织列表的元素list 
    button=driver.find_elements_by_css_selector('ul[class="as-select as-left"]>li')
    for i in button:
        filterEles[0].click()#点击打开过滤方案
        driver.execute_script("$(arguments[0]).click()",i)
        time.sleep(10)
        orgName.append(i.get_attribute('textContent').replace('\n','').replace(' ',''))#去掉换行、空格
        #num=driver.execute_script("return $('.jspPane').find('li').length;")
        orderitem.append(len(driver.find_elements_by_css_selector('tr[class="m-tr-item"]')))
    productDict=dict(zip(orgName,orderitem))#生成生产组织：生产订单条目数字典
    print(productDict)
    Log("已获取到生产齐套分析页面组织和订单数据")
    return productDict