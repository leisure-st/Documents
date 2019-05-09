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
#from login import *

#进入掌上报销
def openHandHeldBursement(driver):
    driver.get("http://v-mobile-at/k3cloud/mobile/k3cloud.html?entryrole=XT&appid=10728&formId=ER_MBReimb_HomePage&formType=mobile")
    time.sleep(10)
#新增费用申请单
def addExpenseRequest(driver,pcDriver):
    driver.find_element_by_css_selector('button[data-kdid="FBTNTOPMENU3"]').click()
    time.sleep(6)
    driver.find_element_by_css_selector('textarea[data-kdid="FREASON_ITEM"]').send_keys("测试新增费用申请单"+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))
    driver.find_element_by_css_selector('button[data-kdid="FBTNWADDPLAN"]').click()
    time.sleep(2)
    driver.find_element_by_css_selector('input[data-kdid="FEXPENSEITEMID_ITEM"]').click()
    time.sleep(4)
    # cloud在弹出基础资料的时候用的是iframe，所以需要先切换到那个iframe里面才能定位元素
    driver.switch_to_frame(driver.find_element_by_css_selector("iframe[id^='layui-layer-iframe']"))#driver.switch_to_frame("layui-layer-iframe1")
    #print(driver.find_elements_by_css_selector("div[data-kdid='FFLOWLAYOUT']"))
    driver.find_element_by_css_selector("div[data-kdid='FFLOWLAYOUT']").click()#选择费用项目
    driver.switch_to_default_content() #切换到iframe之后需要再切换原来的默认的frame，才能操作主体元素
    
    #ps: 如果那个iframe没有id或者name怎么办？
    #参考文章：https://blog.csdn.net/zhj_test/article/details/40889031

    time.sleep(2)
    #输入费用项金额
    driver.find_element_by_css_selector("input[data-kdid='FORGAMOUNT_ITEM']").send_keys(1200)#在一个页面中，data-kdid是唯一的，金蝶自定义的属性
    driver.find_element_by_css_selector('button[data-kdid="FBTNSAVEANDNEWADD"]').click()#复制行
    #driver.find_element_by_css_selector("#kdmMainform > div.ui-panel-wrapper > div > div:nth-child(1) > div:nth-child(3) > div > div > div.kdm-flowlayout-vertical.ui-controlgroup.ui-controlgroup-vertical.ui-corner-all > div > button").click()
    if is_element_exist(driver,".layui-layer-btn0"):
        driver.find_element_by_css_selector(".layui-layer-btn0").click()#可能弹出金额不能为0
    else:
        Log("金额大于0")
    driver.find_element_by_css_selector('button[data-kdid="FBTNCONFIRM"]').click()#确定返回金额
    time.sleep(4)
    driver.find_element_by_css_selector('select[data-kdid="FBORROWTYPE_ITEM"]').click()
    time.sleep(2)
    driver.find_element_by_css_selector('option[value="3"]').click()
    time.sleep(3)
    driver.find_element_by_css_selector('button[data-kdid="FBTNSUBMIT"]').click()
    time.sleep(4)
    if is_element_exist(driver,'div[class="layui-layer-content"]'):  #判断是否弹窗提示单据新增成功
        driver.find_element_by_css_selector('div>a[class="layui-layer-btn0"]').click()     #点击确定                  
        Log("移动端费用申请单新增成功！")
        tips=driver.find_element_by_css_selector('div[class="layui-layer-content"]').text#获取移动端新增单据的单据编号
        billNumber=tips[6:23]
        Log("单据编号为："+billNumber)
        #打开我的费用申请单
        box=pcDriver.find_element_by_css_selector(".ui-poplistedit-displayname")
        if box.get_attribute('title'):
            pcDriver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").clear()#清空当前搜索框text内容
        pcDriver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").send_keys("我的费用申请")
        time.sleep(6)
        pcDriver.find_element_by_xpath("/html/body/div[3]/div/div/div/li/span[3]").click()#打开单据
        time.sleep(7)
        filterOrder(driver,pcDriver,billNumber)
        time.sleep(2)
        pcDriver.find_element_by_css_selector('span[class=" k-i-close mainTabCloseButton"]').click()
        return billNumber
    else:
         Log("移动端费用申请单新增操作有误！")
         return False

#检查移动端与pc端订单是否相同
def filterOrder(driver,pcDriver,billNumber):
    filterSchemeEle=pcDriver.find_element_by_css_selector('input[class="k-input defaultQuikerRowEmptyShow"]')#获取快捷过滤方案元素
    filterScheme=filterSchemeEle.get_attribute('title')  #获取其文本
    # print(filterScheme)
    if filterScheme=="单据编号":
        pcDriver.find_element_by_css_selector('input[id$="FQKFILTERPANEL_DFR_PPART_VALUE_c"]').send_keys(billNumber)#按照移动端新增单据的单据编号查询pc端订单列表
        time.sleep(4)
        pcDriver.find_element_by_css_selector(".kd-btn-filterQuick-search").click()#点击查询
        time.sleep(3)
        pcList=int(pcDriver.find_element_by_css_selector("span[data-kdid='sp_2_pagerlist2']").text)#检查单据列表是否为空
        status=pcDriver.find_element_by_css_selector('span[data-field="FDOCUMENTSTATUS"]').text#检查查询结果单据的状态
        if pcList==1 and status=="审核中":
            Log("PC端单据同步新增成功，状态为审核中！")
        elif pcList==1 and status!="审核中":
            Log("pc端单据同步新增成功， 状态不为审核中，请检查！")
        elif pcList!=1 :
            Log("pc端单据查询无结果，请检查！")


#新增费用报销单
def addExpReimbursement(driver,pcDriver):
    driver.find_element_by_css_selector("button[data-kdid='FBTNTOPMENU4']").click()
    time.sleep(6)
    driver.find_element_by_css_selector('textarea[data-kdid="FCAUSA_ITEM"]').send_keys("测试新增费用报销单"+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))
    driver.find_element_by_css_selector('button[data-kdid="FBTNWADDPLAN"]').click()
    time.sleep(2)
    driver.find_element_by_css_selector('input[data-kdid="FEXPENSEITEMID_ITEM"]').click()
    time.sleep(5)
    driver.switch_to_frame(driver.find_element_by_css_selector("iframe[id^='layui-layer-iframe']"))#模糊前匹配
    driver.find_element_by_css_selector("div[data-kdid='FFLOWLAYOUT']").click()#选择费用项目
    driver.switch_to_default_content() 
    time.sleep(2)
    driver.find_element_by_css_selector("input[data-kdid='FORGAMOUNT_ITEM']").send_keys(1000)
    driver.find_element_by_css_selector('button[data-kdid="FBTNSAVEANDNEWADD"]').click()
    if is_element_exist(driver,".layui-layer-btn0"):
        driver.find_element_by_css_selector(".layui-layer-btn0").click()#可能弹出金额不能为0
    else:
        Log("金额大于0")
    driver.find_element_by_css_selector('button[data-kdid="FBTNCONFIRM"]').click()#确定返回金额
    time.sleep(4)
    driver.find_element_by_css_selector('button[data-kdid="FBTNSUBMIT"]').click()
    time.sleep(5)
    if is_element_exist(driver,'div[class="layui-layer-content"]'):  #判断是否弹窗提示单据新增成功
        driver.find_element_by_css_selector('div>a[class="layui-layer-btn0"]').click()     #点击确定                  
        Log("移动端费用报销单新增成功！")
        tips=driver.find_element_by_css_selector('div[class="layui-layer-content"]').text#获取移动端新增单据的单据编号
        billNumber=tips[6:24]
        Log("单据编号为："+billNumber)
        #打开我的费用申请单
        box=pcDriver.find_element_by_css_selector(".ui-poplistedit-displayname")
        if box.get_attribute('title'):
            pcDriver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").clear()#清空当前搜索框text内容
        pcDriver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").send_keys("我的费用报销")
        time.sleep(6)
        pcDriver.find_element_by_xpath("/html/body/div[3]/div/div/div/li/span[3]").click()
        time.sleep(7)
        filterOrder(driver,pcDriver,billNumber)
        time.sleep(2)
        pcDriver.find_element_by_css_selector('span[class=" k-i-close mainTabCloseButton"]').click()
    else:
         Log("移动端费用报销单新增操作有误！")

#新增出差申请单
def addExpenseRequest_Travel(driver,pcDriver):
    driver.find_element_by_css_selector('button[data-kdid="FBTNTOPMENU1"]').click()
    time.sleep(6)
    driver.find_element_by_css_selector('textarea[data-kdid="FREASON_ITEM"]').send_keys("测试新增出差申请单"+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))
    driver.find_element_by_css_selector('button[data-kdid="FBTNWADDPLAN"]').click()
    time.sleep(2)
    driver.find_element_by_css_selector('input[data-kdid="FEXPENSEITEMID_ITEM"]').click()
    time.sleep(4)
    driver.switch_to_frame(driver.find_element_by_css_selector("iframe[id^='layui-layer-iframe']"))
    driver.find_element_by_css_selector("div[data-kdid='FFLOWLAYOUT']").click()#选择费用项目
    driver.switch_to_default_content() 
    time.sleep(2)
    driver.find_element_by_css_selector('input[data-kdid="FTRAVELSTARTSITE_ITEM"]').send_keys("上海")
    driver.find_element_by_css_selector('input[data-kdid="FTRAVELENDSITE_ITEM"]').send_keys("深圳")
    driver.find_element_by_css_selector('input[data-kdid="FAIRTICKETCOST_ITEM"]').send_keys(800)
    driver.find_element_by_css_selector('button[data-kdid="FBTNSAVEANDNEWADD"]').click()#复制行
    #driver.find_element_by_css_selector("#kdmMainform > div.ui-panel-wrapper > div > div:nth-child(1) > div:nth-child(3) > div > div > div.kdm-flowlayout-vertical.ui-controlgroup.ui-controlgroup-vertical.ui-corner-all > div > button").click()
    if is_element_exist(driver,".layui-layer-btn0"):
        driver.find_element_by_css_selector(".layui-layer-btn0").click()#可能弹出金额不能为0
    else:
        Log("金额大于0")
    driver.find_element_by_css_selector('button[data-kdid="FBTNCONFIRM"]').click()#确定返回金额
    time.sleep(4)
    driver.find_element_by_css_selector('select[data-kdid="FBORROWTYPE_ITEM"]').click()
    time.sleep(2)
    driver.find_element_by_css_selector('option[value="3"]').click()
    time.sleep(3)
    driver.find_element_by_css_selector('button[data-kdid="FBTNSUBMIT"]').click()
    time.sleep(4)
    if is_element_exist(driver,'div[class="layui-layer-content"]'):  #判断是否弹窗提示单据新增成功
        driver.find_element_by_css_selector('div>a[class="layui-layer-btn0"]').click()     #点击确定                  
        Log("移动端出差申请单新增成功！")
        tips=driver.find_element_by_css_selector('div[class="layui-layer-content"]').text#获取移动端新增单据的单据编号
        billNumber=tips[6:23]
        Log("单据编号为："+billNumber)
        #打开我的费用申请单
        box=pcDriver.find_element_by_css_selector(".ui-poplistedit-displayname")
        if box.get_attribute('title'):
            pcDriver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").clear()#清空当前搜索框text内容
        pcDriver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").send_keys("我的出差申请")
        time.sleep(6)
        pcDriver.find_element_by_xpath("/html/body/div[3]/div/div/div/li/span[3]").click()
        time.sleep(7)
        filterOrder(driver,pcDriver,billNumber)
        time.sleep(2)
        pcDriver.find_element_by_css_selector('span[class=" k-i-close mainTabCloseButton"]').click()
        return billNumber
    else:
         Log("移动端出差申请单新增操作有误！")
         return False

#新增差旅报销单
def addExpReimbursement_Travel(driver,pcDriver):
    driver.find_element_by_css_selector('button[data-kdid="FBTNTOPMENU2"]').click()
    time.sleep(5)
    driver.find_element_by_css_selector('textarea[data-kdid="FCAUSA_ITEM"]').send_keys("测试新增差旅报销单"+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))
    driver.find_element_by_css_selector('button[data-kdid="FBTNWADDPLAN"]').click()
    time.sleep(2)
    driver.find_element_by_css_selector('input[data-kdid="FEXPENSEITEMID_ITEM"]').click()
    time.sleep(5)
    driver.switch_to_frame(driver.find_element_by_css_selector("iframe[id^='layui-layer-iframe']"))                                                                          #模糊前匹配
    driver.find_element_by_css_selector("div[data-kdid='FFLOWLAYOUT']").click()#选择费用项目
    driver.switch_to_default_content() 
    time.sleep(2)
    driver.find_element_by_css_selector('input[data-kdid="FTRAVELSTARTSITE_ITEM"]').send_keys("上海")
    driver.find_element_by_css_selector('input[data-kdid="FTRAVELENDSITE_ITEM"]').send_keys("深圳")
    driver.find_element_by_css_selector('input[data-kdid="FCITYTRAFFICFEE_ITEM"]').send_keys(800)
    driver.find_element_by_css_selector('button[data-kdid="FBTNSAVEANDNEWADD"]').click()#复制行
    #driver.find_element_by_css_selector("#kdmMainform > div.ui-panel-wrapper > div > div:nth-child(1) > div:nth-child(3) > div > div > div.kdm-flowlayout-vertical.ui-controlgroup.ui-controlgroup-vertical.ui-corner-all > div > button").click()
    if is_element_exist(driver,".layui-layer-btn0"):
        driver.find_element_by_css_selector(".layui-layer-btn0").click()#可能弹出金额不能为0
    else:
        Log("金额大于0")
    driver.find_element_by_css_selector('button[data-kdid="FBTNCONFIRM"]').click()#确定返回金额
    time.sleep(4)
    driver.find_element_by_css_selector('button[data-kdid="FBTNSUBMIT"]').click()
    time.sleep(5)
    if is_element_exist(driver,'div[class="layui-layer-content"]'):  #判断是否弹窗提示单据新增成功
        driver.find_element_by_css_selector('div>a[class="layui-layer-btn0"]').click()     #点击确定                  
        Log("移动端差旅费报销单新增成功！")
        tips=driver.find_element_by_css_selector('div[class="layui-layer-content"]').text#获取移动端新增单据的单据编号
        billNumber=tips[6:19]
        Log("单据编号为："+billNumber)
        #打开我的费用申请单
        box=pcDriver.find_element_by_css_selector(".ui-poplistedit-displayname")
        if box.get_attribute('title'):
            pcDriver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").clear()#清空当前搜索框text内容
        pcDriver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").send_keys("我的差旅费报销")
        time.sleep(6)
        pcDriver.find_element_by_xpath("/html/body/div[3]/div/div/div/li/span[3]").click()
        time.sleep(7)
        filterOrder(driver,pcDriver,billNumber)
        time.sleep(2)
        pcDriver.find_element_by_css_selector('span[class=" k-i-close mainTabCloseButton"]').click()#关闭页签
    else:
         Log("移动端差旅报销单新增操作有误！")

#移动端费用申请单下推费用报销单
def pushExpenseRequest(driver,pcDriver,billNumber):
    box=pcDriver.find_element_by_css_selector(".ui-poplistedit-displayname")
    if box.get_attribute('title'):
        pcDriver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").clear()#清空当前搜索框text内容
    pcDriver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").send_keys("我的费用申请")
    time.sleep(6)
    pcDriver.find_element_by_xpath("/html/body/div[3]/div/div/div/li/span[3]").click()
    filterOrder(driver,pcDriver,billNumber)
    time.sleep(2)
    pcDriver.find_element_by_css_selector('div[class="kd-grid-celldiv kd-grid-selector "]').click()
    pcDriver.find_element_by_css_selector('span[id$="BILLMENU_TOOLBAR-tbSplitApprove"]').click()#审核
    Log("费用申请单审核成功！")
    time.sleep(3)
    driver.get("http://v-mobile-at/k3cloud/mobile/k3cloud.html?entryrole=XT&appid=10728&formId=ER_MBReimb_HomePage&formType=mobile")
    time.sleep(5)
    driver.find_element_by_css_selector('button[data-kdid="FBTNWNEXT"]').click()
    time.sleep(5)
    driver.find_element_by_css_selector('button[data-kdid="FBTNSUBMIT"]').click()
    time.sleep(5)

    driver.get("http://v-mobile-at/k3cloud/mobile/k3cloud.html?entryrole=XT&appid=10728&formId=ER_MBReimb_HomePage&formType=mobile")
    time.sleep(3)
    if is_element_exist(driver,'input[data-kdid="FTITLE_ITEM"]'):
        ele=driver.find_element_by_css_selector('input[data-kdid="FTITLE_ITEM"]')
        if "费用报销"in ele.get_attribute('value'):
            Log("移动端费用申请单下推报销单成功！")
        else:
            Log("移动端费用申请单下推报销单操作有误！")


    # if is_element_exist(driver,'div[class="layui-layer-content"]'):  #判断是否弹窗提示单据新增成功
    #     driver.find_element_by_css_selector('div>a[class="layui-layer-btn0"]').click()     #点击确定                  
    #     Log("移动端费用申请单下推报销单成功！")
    #     tips=driver.find_element_by_css_selector('div[class="layui-layer-content"]').text#获取移动端新增单据的单据编号
    #     newbillNumber=tips[6:24]
    #     Log("单据编号为："+newbillNumber)
    # else:
    #      Log("移动端费用申请单下推报销单操作有误！")

#移动端出差申请单下推差旅费报销单
def pushExpenseRequest_Travel(driver,pcDriver,billNumber):
    box=pcDriver.find_element_by_css_selector(".ui-poplistedit-displayname")#定位到搜索框
    if box.get_attribute('title'):#搜索框不为空
        pcDriver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").clear()#清空当前搜索框text内容
    pcDriver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").send_keys("我的出差申请")
    time.sleep(6)
    pcDriver.find_element_by_xpath("/html/body/div[3]/div/div/div/li/span[3]").click()
    filterOrder(driver,pcDriver,billNumber)
    time.sleep(2)
    pcDriver.find_element_by_css_selector('div[class="kd-grid-celldiv kd-grid-selector "]').click()
    pcDriver.find_element_by_css_selector('span[id$="BILLMENU_TOOLBAR-tbSplitApprove"]').click()#审核
    Log("费用申请单审核成功！")
    time.sleep(3)
    driver.get("http://v-mobile-at/k3cloud/mobile/k3cloud.html?entryrole=XT&appid=10728&formId=ER_MBReimb_HomePage&formType=mobile")
    time.sleep(5)
    driver.find_element_by_css_selector('button[data-kdid="FBTNWNEXT"]').click()
    time.sleep(5)
    driver.find_element_by_css_selector('button[data-kdid="FBTNSUBMIT"]').click()
    time.sleep(5)
    driver.get("http://v-mobile-at/k3cloud/mobile/k3cloud.html?entryrole=XT&appid=10728&formId=ER_MBReimb_HomePage&formType=mobile")
    time.sleep(3)
    if is_element_exist(driver,'input[data-kdid="FTITLE_ITEM"]'):
        ele=driver.find_element_by_css_selector('input[data-kdid="FTITLE_ITEM"]')
        if "差旅报销"in ele.get_attribute('value'):
            Log("移动端出差申请单下推报销单成功！")
        else:
            Log("移动端出差申请单下推报销单操作有误！")


    #一级用例启动
def handHeldfirstLeverTest(mobDriver,pcDriver,allOrgName):
    openHandHeldBursement(mobDriver)
    #login_pc(pcDriver,USERNAME,PASSWORD)
    
    try:
        billNumber=addExpenseRequest(mobDriver,pcDriver)#新增费用申请单
    finally:
        print("执行完毕")
        #mobDriver.close()
        #pcDriver.close()
    try:
        pushExpenseRequest(mobDriver,pcDriver,billNumber)
    finally:
        print("执行完毕")
        #mobDriver.close()
        #pcDriver.close()
    try:
        billNumber=addExpenseRequest_Travel(mobDriver,pcDriver)#新增出差申请单
    finally:
        print("执行完毕")
        #mobDriver.close()
        #pcDriver.close()
    try:
        #login_pc(pcDriver,USERNAME,PASSWORD)
        pushExpenseRequest_Travel(mobDriver,pcDriver,billNumber)
    finally:
        print("执行完毕")
        #mobDriver.close()
        #pcDriver.close()


    
    
