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

#进入掌上报销V3首页
def openMobileReimb(driver):
    driver.get("http://v-mobile-at/k3cloud/mobile/k3cloud.html?entryrole=XT&appid=10728&formId=ER_MBReimb_HomePage&formType=mobile")
    Log("进入新版掌上报销")
    time.sleep(10)
    # tempUrl=driver.current_url
    # print(tempUrl)

#掌上报销V3首页暂存单据测试
def tempStorage(driver,pcDriver):
    settingUrl=driver.current_url+"/setting"
    print(settingUrl)
    driver.get(settingUrl)
    time.sleep(2)
    #检查是否开启了录单暂存功能
    settingButton=driver.find_element_by_css_selector('ul[class="setting-list"]>li')
    if settingButton.find_element_by_css_selector('p').text == "录单自动暂存":
        if is_element_exist(settingButton,'label[class="mint-switch drag-button checked"]'):
            checkedStorage(driver,pcDriver)
        # else:
        #     checkedStorage(driver,pcDriver)

def checkedStorage(driver,pcDriver):
    driver.get("http://v-mobile-at/k3cloud/mobile/k3cloud.html?entryrole=XT&appid=10728&formId=ER_MBReimb_HomePage&formType=mobile")
    time.sleep(5)
    draftAmount=float(driver.find_element_by_css_selector('a[href="#/Draft"]>h3>span').text)
    print(draftAmount)
    driver.find_element_by_css_selector('aside[class="home-add"]').click()#点击新增单据
    time.sleep(6)
    driver.find_element_by_css_selector('span[class="tangerine"]').click()#点击新增费用申请单
    time.sleep(15)
    driver.find_element_by_css_selector('textarea[placeholder="请填写事由"]').send_keys("测试新增费用申请单"+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))
    driver.find_element_by_css_selector('div[class="icon-more"]').click()#点击默认空白分录行的更多入口
    driver.find_element_by_css_selector('div[class="icon-more js-show-operate"]>aside>ul>li').click()#点击进入编辑页面
    time.sleep(5)
    # cloud在弹出基础资料的时候用的是iframe，所以需要先切换到那个iframe里面才能定位元素
    #ifameparents=driver.find_element_by_css_selector("iframe[id^='layui-layer-iframe']")

    #获取费用项选择界面的iframe
    MBReimb_ExpItem_Frame = driver.find_element_by_css_selector('iframe[src*="formId=ER_MBReimb_ExpItemV3"]')

    driver.switch_to_frame(MBReimb_ExpItem_Frame)#driver.switch_to_frame("layui-layer-iframe1")
    #print(driver.find_elements_by_css_selector("div[data-kdid='FFLOWLAYOUT']"))
    driver.find_element_by_css_selector('input[data-kdid="FEXPENSEITEMID_ITEM"]').click()#进入选择费用项目的列表
    time.sleep(3)                   #$.mobile.activePage.find("#gallery-img")
    driver.switch_to_default_content()
    #driver.find_element_by_css_selector("iframe[id^='layui-layer-iframe']")
    F8List = driver.find_element_by_css_selector('iframe[src*="formId=MOB_F8List"]')
    driver.switch_to_frame(F8List)
    driver.find_element_by_css_selector('div[data-kdid="FFLOWLAYOUT1"]>div[data-kdid="FLISTNAME"]').click()
    time.sleep(2)
    driver.switch_to_frame(MBReimb_ExpItem_Frame)
    driver.find_element_by_css_selector('input[data-kdid="FORGAMOUNT_ITEM"]').send_keys(1)
    time.sleep(2)
    driver.find_element_by_css_selector('button[data-kdc="kdbutton"]').click()
    driver.switch_to_default_content()
    
    time.sleep(2)
    driver.find_element_by_css_selector('button[data-kdc="kdbutton"]').click()
    driver.switch_to_default_content() #切换到iframe之后需要再切换原来的默认的frame，才能操作主体元素
    driver.get("http://v-mobile-at/k3cloud/mobile/k3cloud.html?entryrole=XT&appid=10728&formId=ER_MBReimb_HomePage&formType=mobile")
    time.sleep(6)
    draftAmountUpdate=float(driver.find_element_by_css_selector('a[href="#/Draft"]>h3>span').text)
    print(draftAmountUpdate)
    if draftAmountUpdate-draftAmount==1:
        Log("成功暂存一张单据")
    else:
        Log("暂存单据失败")

#新增费用申请单
def appendExpenseRequest(driver,pcDriver):
    undoneAmount=float(driver.find_element_by_css_selector('a[href="#/UnDoneList"]>h3>span').text)
    driver.find_element_by_css_selector('aside[class="home-add"]').click()#点击新增单据
    time.sleep(6)
    driver.find_element_by_css_selector('span[class="tangerine"]').click()#点击新增费用申请单
    time.sleep(15)

    reason="测试新增费用申请单"+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
    driver.find_element_by_css_selector('textarea[placeholder="请填写事由"]').send_keys(reason)
    time.sleep(2)
    driver.find_element_by_css_selector('div[class="icon-more"]').click()#点击默认空白分录行的更多入口
    driver.find_element_by_css_selector('div[class="icon-more js-show-operate"]>aside>ul>li').click()#点击进入编辑页面
    time.sleep(5)
    MBReimb_ExpItem_Frame = driver.find_element_by_css_selector('iframe[src*="formId=ER_MBReimb_ExpItemV3"]')

    driver.switch_to_frame(MBReimb_ExpItem_Frame)#driver.switch_to_frame("layui-layer-iframe1")
    #print(driver.find_elements_by_css_selector("div[data-kdid='FFLOWLAYOUT']"))
    driver.find_element_by_css_selector('input[data-kdid="FEXPENSEITEMID_ITEM"]').click()#进入选择费用项目的列表
    time.sleep(3)                   #$.mobile.activePage.find("#gallery-img")
    driver.switch_to_default_content()
    #driver.find_element_by_css_selector("iframe[id^='layui-layer-iframe']")
    F8List = driver.find_element_by_css_selector('iframe[src*="formId=MOB_F8List"]')
    driver.switch_to_frame(F8List)
    driver.find_element_by_css_selector('div[data-kdid="FFLOWLAYOUT1"]>div[data-kdid="FLISTNAME"]').click()
    time.sleep(2)
    driver.switch_to_frame(MBReimb_ExpItem_Frame)
    driver.find_element_by_css_selector('input[data-kdid="FORGAMOUNT_ITEM"]').send_keys(1)
    time.sleep(2)
    driver.find_element_by_css_selector('button[data-kdc="kdbutton"]').click()

    driver.switch_to_default_content() #切换到iframe之后需要再切换原来的默认的frame，才能操作主体元素
    time.sleep(2)
    driver.find_element_by_css_selector('button[data-kdid="FBUTTONCOMMIT"]').click()
    time.sleep(8)
    undoneAmountUpdate=float(driver.find_element_by_css_selector('a[href="#/UnDoneList"]>h3>span').text)
    if undoneAmountUpdate-undoneAmount==1:
        Log("移动端单据数量新增加一")
        box=pcDriver.find_element_by_css_selector(".ui-poplistedit-displayname")
        if box.get_attribute('title'):
                pcDriver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").clear()#清空当前搜索框text内容
        if is_element_exist(pcDriver,'span[class=" k-i-close mainTabCloseButton"]'):
                pcDriver.find_element_by_css_selector('span[class=" k-i-close mainTabCloseButton"]').click()#关闭当前页签
        pcDriver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").send_keys("我的费用申请")
        time.sleep(6)
        pcDriver.find_element_by_css_selector('li[class="k-state-focused"]').click()
        time.sleep(8)
        pcDriver.find_element_by_css_selector('input[class="k-input defaultQuikerRowEmptyShow"]').clear()
        pcDriver.find_element_by_css_selector('input[class="k-input defaultQuikerRowEmptyShow"]').send_keys("事由")
        
        pcDriver.execute_script('document.getElementsByClassName("k-input defaultQuikerRowEmptyShow")[0].blur()')#js通过classname找

#        pcDriver.find_element_by_css_selector('a[tabindex="-1"]').click()
        time.sleep(2)
        pcDriver.find_element_by_css_selector('div[class="kdQuickFilterContainer_editorct kdItemContainer_editorct"]>div>div>textarea').send_keys(reason)
        pcDriver.find_element_by_css_selector(".kd-btn-filterQuick-search").click()#点击查询
        time.sleep(3)
        pcList=int(pcDriver.find_element_by_css_selector("span[data-kdid='sp_2_pagerlist2']").text)#检查单据列表是否为空
        status=pcDriver.find_element_by_css_selector('span[data-field="FDOCUMENTSTATUS"]').text#检查查询结果单据的状态
        if pcList==1 and status=="审核中":
            Log("PC端费用申请单据同步新增成功，状态为审核中！")
        elif pcList==1 and status!="审核中":
            Log("pc端费用申请单据同步新增成功， 状态不为审核中，请检查！")
        elif pcList!=1 :
            Log("pc端费用申请单据查询无结果，请检查！")

#新增费用报销单
def appendExpReimbursement(driver,pcDriver):
    undoneAmount=float(driver.find_element_by_css_selector('a[href="#/UnDoneList"]>h3>span').text)
    driver.find_element_by_css_selector('aside[class="home-add"]').click()#点击新增单据
    time.sleep(6)
    driver.find_element_by_css_selector('span[class="blue"]').click()#点击新增费用报销单
    time.sleep(15)

    reason="测试新增费用报销单"+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
    driver.find_element_by_css_selector('div[data-kdid="FCAUSALAYOUT"]>div>div>textarea[placeholder="请填写事由"]').send_keys(reason)
    time.sleep(2)
    driver.find_element_by_css_selector('div[class="icon-more"]').click()#点击默认空白分录行的更多入口
    driver.find_element_by_css_selector('div[class="icon-more js-show-operate"]>aside>ul>li').click()#点击进入编辑页面
    time.sleep(5)
    # cloud在弹出基础资料的时候用的是iframe，所以需要先切换到那个iframe里面才能定位元素
    ifameparent=driver.find_element_by_css_selector("iframe[id^='layui-layer-iframe']")
    driver.switch_to_frame(ifameparent)#driver.switch_to_frame("layui-layer-iframe1")
    #print(driver.find_elements_by_css_selector("div[data-kdid='FFLOWLAYOUT']"))
    driver.find_element_by_css_selector('div[data-kdid="FEXPID_ITEM_Ex"]>img').click()#进入选择费用项目的列表
    time.sleep(3)
    driver.switch_to_frame(driver.find_element_by_css_selector("iframe[id^='layui-layer-iframe']"))
    driver.find_element_by_css_selector('div[data-kdid="FFLOWLAYOUT1"]>div[data-kdid="FLISTNAME"]').click()
    time.sleep(2)
    driver.switch_to_default_content()
    driver.switch_to_frame(ifameparent)
    driver.find_element_by_css_selector('input[data-kdid="FTAXSUBMITAMT_ITEM"]').send_keys(1)
    time.sleep(2)
    driver.find_element_by_css_selector('button[data-kdc="kdbutton"]').click()
    driver.switch_to_default_content() #切换到iframe之后需要再切换原来的默认的frame，才能操作主体元素
    time.sleep(2)
    driver.find_element_by_css_selector('div[data-kdid="FLABSPREAD"]').click()#点击查看全部
    driver.find_element_by_css_selector('div[data-kdid="FEXPENSEDEPTID_ITEM_Ex"]>img').click()#点击进入选择费用承担部门列表
    driver.switch_to_frame(driver.find_element_by_css_selector("iframe[id^='layui-layer-iframe']"))#模糊前匹配
    driver.find_element_by_css_selector("div[data-kdid='FFLOWLAYOUT']").click()#选择费用承担部门
    driver.switch_to_default_content() 
    time.sleep(2)

    driver.find_element_by_css_selector('button[data-kdid="FBUTTONCOMMIT"]').click()
    time.sleep(8)
    undoneAmountUpdate=float(driver.find_element_by_css_selector('a[href="#/UnDoneList"]>h3>span').text)
    if undoneAmountUpdate-undoneAmount==1:
        Log("移动端单据数量新增加一")
        box=pcDriver.find_element_by_css_selector(".ui-poplistedit-displayname")
        if box.get_attribute('title'):
                pcDriver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").clear()#清空当前搜索框text内容
        if is_element_exist(pcDriver,'span[class=" k-i-close mainTabCloseButton"]'):
                pcDriver.find_element_by_css_selector('span[class=" k-i-close mainTabCloseButton"]').click()#关闭当前页签
        pcDriver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").send_keys("我的费用报销")
        time.sleep(6)
        pcDriver.find_element_by_css_selector('li[class="k-state-focused"]').click()
        time.sleep(8)
        pcDriver.find_element_by_css_selector('input[class="k-input defaultQuikerRowEmptyShow"]').clear()
        pcDriver.find_element_by_css_selector('input[class="k-input defaultQuikerRowEmptyShow"]').send_keys("事由")
        
        pcDriver.execute_script('document.getElementsByClassName("k-input defaultQuikerRowEmptyShow")[0].blur()')#js通过classname找

#        pcDriver.find_element_by_css_selector('a[tabindex="-1"]').click()
        time.sleep(2)
        pcDriver.find_element_by_css_selector('div[class="kdQuickFilterContainer_editorct kdItemContainer_editorct"]>div>div>textarea').send_keys(reason)
        pcDriver.find_element_by_css_selector(".kd-btn-filterQuick-search").click()#点击查询
        time.sleep(3)
        pcList=int(pcDriver.find_element_by_css_selector("span[data-kdid='sp_2_pagerlist2']").text)#检查单据列表是否为空
        status=pcDriver.find_element_by_css_selector('span[data-field="FDOCUMENTSTATUS"]').text#检查查询结果单据的状态
        if pcList==1 and status=="审核中":
            Log("PC端费用报销单据同步新增成功，状态为审核中！")
        elif pcList==1 and status!="审核中":
            Log("pc端费用报销单据同步新增成功， 状态不为审核中，请检查！")
        elif pcList!=1 :
            Log("pc端费用报销单据查询无结果，请检查！")

#新增出差申请单
def appendExpenseRequest_Travel(driver,pcDriver):
    undoneAmount=float(driver.find_element_by_css_selector('a[href="#/UnDoneList"]>h3>span').text)
    driver.find_element_by_css_selector('aside[class="yellow"]').click()#点击新增单据
    time.sleep(6)
    driver.find_element_by_css_selector('span[class="light-green"]').click()#点击新增费用报销单
    time.sleep(15)

    reason="测试新增费用报销单"+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
    driver.find_element_by_css_selector('textarea[placeholder="请填写事由"]').send_keys(reason)
    time.sleep(2)
    driver.find_element_by_css_selector('div[class="icon-more"]').click()#点击默认空白分录行的更多入口
    driver.find_element_by_css_selector('div[class="icon-more js-show-operate"]>aside>ul>li').click()#点击进入编辑页面
    time.sleep(5)
    
    # cloud在弹出基础资料的时候用的是iframe，所以需要先切换到那个iframe里面才能定位元素
    ifameparent=driver.find_element_by_css_selector("iframe[id^='layui-layer-iframe']")
    driver.switch_to_frame(ifameparent)#driver.switch_to_frame("layui-layer-iframe1")
    #print(driver.find_elements_by_css_selector("div[data-kdid='FFLOWLAYOUT']"))
    driver.find_element_by_css_selector('input[data-kdid="FTRAVELSTARTSITE_ITEM"]').send_keys("深圳")
    driver.find_element_by_css_selector('input[data-kdid="FTRAVELENDSITE_ITEM"]').send_keys("撒哈拉沙漠")

    driver.find_element_by_css_selector('input[data-kdid="FEXPENSEITEMID_ITEM"]').click()#进入选择费用项目的列表
    time.sleep(3)
    driver.switch_to_frame(driver.find_element_by_css_selector("iframe[id^='layui-layer-iframe']"))
    driver.find_element_by_css_selector('div[data-kdid="FFLOWLAYOUT1"]>div[data-kdid="FLISTNAME"]').click()
    time.sleep(2)
    driver.switch_to_default_content()
    driver.switch_to_frame(ifameparent)
    driver.find_element_by_css_selector('input[data-kdid="FORGAMOUNT_ITEM"]').send_keys(1)
    time.sleep(2)
    driver.find_element_by_css_selector('button[data-kdc="kdbutton"]').click()
    driver.switch_to_default_content() #切换到iframe之后需要再切换原来的默认的frame，才能操作主体元素
    time.sleep(2)
    driver.find_element_by_css_selector('div[data-kdid="FLABSPREAD"]').click()#点击查看全部
    driver.find_element_by_css_selector('div[data-kdid="FEXPENSEDEPTID_ITEM_Ex"]>img').click()#点击进入选择费用承担部门列表
    driver.switch_to_frame(driver.find_element_by_css_selector("iframe[id^='layui-layer-iframe']"))#模糊前匹配
    driver.find_element_by_css_selector("div[data-kdid='FFLOWLAYOUT']").click()#选择费用承担部门
    driver.switch_to_default_content() 
    time.sleep(2)
    driver.find_element_by_css_selector('button[data-kdid="FBUTTONCOMMIT"]').click()
    time.sleep(5)
    undoneAmountUpdate=float(driver.find_element_by_css_selector('a[href="#/UnDoneList"]>h3>span').text)
    if undoneAmountUpdate-undoneAmount==1:
        Log("移动端单据数量新增加一")
        box=pcDriver.find_element_by_css_selector(".ui-poplistedit-displayname")
        if box.get_attribute('title'):
                pcDriver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").clear()#清空当前搜索框text内容
        if is_element_exist(pcDriver,'span[class=" k-i-close mainTabCloseButton"]'):
                pcDriver.find_element_by_css_selector('span[class=" k-i-close mainTabCloseButton"]').click()#关闭当前页签
        pcDriver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").send_keys("我的出差申请")
        time.sleep(6)
        pcDriver.find_element_by_css_selector('li[class="k-state-focused"]').click()
        time.sleep(8)
        pcDriver.find_element_by_css_selector('input[class="k-input defaultQuikerRowEmptyShow"]').clear()
        pcDriver.find_element_by_css_selector('input[class="k-input defaultQuikerRowEmptyShow"]').send_keys("事由")
        
        pcDriver.execute_script('document.getElementsByClassName("k-input defaultQuikerRowEmptyShow")[0].blur()')#js通过classname找  取消聚焦

#        pcDriver.find_element_by_css_selector('a[tabindex="-1"]').click()
        time.sleep(2)
        pcDriver.find_element_by_css_selector('div[class="kdQuickFilterContainer_editorct kdItemContainer_editorct"]>div>div>textarea').send_keys(reason)
        pcDriver.find_element_by_css_selector(".kd-btn-filterQuick-search").click()#点击查询
        time.sleep(3)
        pcList=int(pcDriver.find_element_by_css_selector("span[data-kdid='sp_2_pagerlist2']").text)#检查单据列表是否为空
        status=pcDriver.find_element_by_css_selector('span[data-field="FDOCUMENTSTATUS"]').text#检查查询结果单据的状态
        if pcList==1 and status=="审核中":
            Log("PC端出差申请单据同步新增成功，状态为审核中！")
        elif pcList==1 and status!="审核中":
            Log("pc端出差申请单据同步新增成功， 状态不为审核中，请检查！")
        elif pcList!=1 :
            Log("pc端出差申请单据查询无结果，请检查！")
        

#新增差旅费报销单
def appendExpReimbursement_Travel(driver,pcDriver):
    undoneAmount=float(driver.find_element_by_css_selector('a[href="#/UnDoneList"]>h3>span').text)
    driver.find_element_by_css_selector('aside[class="home-add"]').click()#点击新增单据
    time.sleep(6)
    driver.find_element_by_css_selector('span[class="yellow"]').click()#点击新增费用报销单
    time.sleep(15)

    reason="测试新增费用报销单"+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
    driver.find_element_by_css_selector('div[data-kdid="FCAUSALAYOUT"]>div>div>textarea[placeholder="请填写事由"]').send_keys(reason)
    time.sleep(2)
    driver.find_element_by_css_selector('div[class="icon-more"]').click()#点击默认空白分录行的更多入口
    driver.find_element_by_css_selector('div[class="icon-more js-show-operate"]>aside>ul>li').click()#点击进入编辑页面
    time.sleep(5)
    
    # cloud在弹出基础资料的时候用的是iframe，所以需要先切换到那个iframe里面才能定位元素
    ifameparent=driver.find_element_by_css_selector("iframe[id^='layui-layer-iframe']")
    driver.switch_to_frame(ifameparent)#driver.switch_to_frame("layui-layer-iframe1")
    #print(driver.find_elements_by_css_selector("div[data-kdid='FFLOWLAYOUT']"))
    driver.find_element_by_css_selector('input[data-kdid="FTRAVELSTARTSITE_ITEM"]').send_keys("深圳")
    driver.find_element_by_css_selector('input[data-kdid="FTRAVELENDSITE_ITEM"]').send_keys("撒哈拉沙漠")
    driver.find_element_by_css_selector('div[data-kdid="FCITYTRAFFICFEELAYOUT"]>div:nth-child(2)>div>div>input[data-kdc="numberfield"]').send_keys(1)
    time.sleep(2)

    driver.find_element_by_css_selector('div[class=" kdm-itemcontrainer-item "]>div>img').click()#进入选择费用项目的列表
    time.sleep(3)
    driver.switch_to_frame(driver.find_element_by_css_selector("iframe[id^='layui-layer-iframe']"))
    driver.find_element_by_css_selector('div[data-kdid="FFLOWLAYOUT1"]>div[data-kdid="FLISTNAME"]').click()
    time.sleep(2)
    driver.switch_to_default_content()
    driver.switch_to_frame(ifameparent)
    
    driver.find_element_by_css_selector('button[data-kdc="kdbutton"]').click()
    driver.switch_to_default_content() #切换到iframe之后需要再切换原来的默认的frame，才能操作主体元素
    time.sleep(2)
    driver.find_element_by_css_selector('div[data-kdid="FLABSPREAD"]').click()#点击查看全部
    driver.find_element_by_css_selector('div[data-kdid="FEXPENSEDEPTID_ITEM_Ex"]>img').click()#点击进入选择费用承担部门列表
    driver.switch_to_frame(driver.find_element_by_css_selector("iframe[id^='layui-layer-iframe']"))#模糊前匹配
    driver.find_element_by_css_selector("div[data-kdid='FFLOWLAYOUT']").click()#选择费用承担部门
    driver.switch_to_default_content() 
    time.sleep(2)
    driver.find_element_by_css_selector('button[data-kdid="FBUTTONCOMMIT"]').click()
    time.sleep(8)
    undoneAmountUpdate=float(driver.find_element_by_css_selector('a[href="#/UnDoneList"]>h3>span').text)
    if undoneAmountUpdate-undoneAmount==1:
        Log("移动端单据数量新增加一")
        box=pcDriver.find_element_by_css_selector(".ui-poplistedit-displayname")
        if box.get_attribute('title'):
                pcDriver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").clear()#清空当前搜索框text内容
        if is_element_exist(pcDriver,'span[class=" k-i-close mainTabCloseButton"]'):
                pcDriver.find_element_by_css_selector('span[class=" k-i-close mainTabCloseButton"]').click()#关闭当前页签
        pcDriver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").send_keys("我的差旅费报销")
        time.sleep(6)
        pcDriver.find_element_by_css_selector('li[class="k-state-focused"]').click()
        time.sleep(8)
        pcDriver.find_element_by_css_selector('input[class="k-input defaultQuikerRowEmptyShow"]').clear()
        pcDriver.find_element_by_css_selector('input[class="k-input defaultQuikerRowEmptyShow"]').send_keys("事由")
        
        pcDriver.execute_script('document.getElementsByClassName("k-input defaultQuikerRowEmptyShow")[0].blur()')#js通过classname找  取消聚焦

#        pcDriver.find_element_by_css_selector('a[tabindex="-1"]').click()
        time.sleep(2)
        pcDriver.find_element_by_css_selector('div[class="kdQuickFilterContainer_editorct kdItemContainer_editorct"]>div>div>textarea').send_keys(reason)
        pcDriver.find_element_by_css_selector(".kd-btn-filterQuick-search").click()#点击查询
        time.sleep(3)
        pcList=int(pcDriver.find_element_by_css_selector("span[data-kdid='sp_2_pagerlist2']").text)#检查单据列表是否为空
        status=pcDriver.find_element_by_css_selector('span[data-field="FDOCUMENTSTATUS"]').text#检查查询结果单据的状态
        if pcList==1 and status=="审核中":
            Log("PC端出差申请单据同步新增成功，状态为审核中！")
        elif pcList==1 and status!="审核中":
            Log("pc端出差申请单据同步新增成功， 状态不为审核中，请检查！")
        elif pcList!=1 :
            Log("pc端出差申请单据查询无结果，请检查！")

#一级用例启动
def mobileReimbfirstLeverTest(mobDriver,pcDriver):
    openMobileReimb(mobDriver)
    
    try:
        checkedStorage(mobDriver,pcDriver)
    finally:
        Log("执行暂存单据完毕")
    try:
        appendExpenseRequest(mobDriver,pcDriver)
    finally:
        Log("执行新增费用申请单完毕")
        




    

    




    