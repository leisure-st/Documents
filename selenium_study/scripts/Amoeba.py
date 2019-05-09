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
from selenium.webdriver.chrome.options import Options
from common import *
from login import *

amoebaName=[]#阿米巴单元名称集合
#获取所有阿米巴单元选择项元素
amoebaEles=[]
homePageUrl='http://v-mobile-at/K3Cloud/KDMobile/AmoebaReport/index.html'#阿米巴报表首页url
#进入阿米巴报表
def openAmoeba(driver):
    driver.get("http://v-mobile-at/K3Cloud/mobile/k3cloud.html?entryrole=XT&formId=~/KDMobile/AmoebaReport/index.html&formType=mobileurl&appid=10758")#进入阿米巴报表
    time.sleep(10)
    Log("进入阿米巴报表")
    time.sleep(6)

def setConfig(driver):
    #配置页非空判断测试
    driver.find_element_by_css_selector('button[class="setting-button"]').click()#点击开启报表
    time.sleep(5)
    if is_element_exist(driver,'button[class="setting-button"]'):
        Log("配置页面必录，否则无法开启报表，测试通过")
    else:
        Log("配置页面必录，否则无法开启报表，测试不通过")
    #设置配置页面账簿、利润中心、经营期间
    driver.find_element_by_css_selector('ul[class="setting-items"]>li>span:nth-child(2)>i').click()  #li:nth-child(1) 点击账簿选择入口
    time.sleep(10)
    driver.find_element_by_css_selector('i[class="m-checked round fill"]').click()#点击选择账簿
    time.sleep(5)
    driver.find_element_by_css_selector('a[class="confirm"]').click()#点击确定按钮
    time.sleep(5)
    driver.find_element_by_css_selector('ul[class="setting-items"]>li:nth-child(2)>span:nth-child(2)>i').click()  #点击阿米巴单元选择入口
    time.sleep(2)
    optionEles=driver.find_elements_by_css_selector('p[class="mint-indexsection-item"]')#可供选择的阿米巴选项元素
    for ele in optionEles:
        amoebaName.append(ele.text)
    print(amoebaName)
    selectedEles=driver.find_elements_by_css_selector('i[class="m-checked round fill checked"]')#已选中的阿米巴选项元素
    if len(optionEles)==(len(selectedEles)-1):
        driver.find_element_by_css_selector('a[class="confirm"]').click()
        Log("阿米巴单元默认全选，测试通过")
    else:
        driver.find_element_by_css_selector('label[class="check-all"]>i').click()
        driver.find_element_by_css_selector('a[class="confirm"]').click()
        Log("阿米巴单元应该默认全选，请检查")

    driver.find_element_by_css_selector('button[class="setting-button"]').click()#点击开启报表
    time.sleep(5)
    if is_element_exist(driver,'button[class="setting-button"]'):
        Log("配置页面期间必录，否则无法开启报表，测试通过")
    else:
        Log("配置页面期间必录，否则无法开启报表，测试不通过")
    driver.find_element_by_css_selector('ul[class="setting-items"]>li:nth-child(3)>span:nth-child(2)>i').click()#点击期间选择入口
    time.sleep(3)
    driver.find_element_by_css_selector('article[class="home"]>ul>li:nth-child(2)>span').click()#点击选择第一个所在期间
    time.sleep(2)
    driver.find_element_by_css_selector('button[class="setting-button"]').click()#点击开启报表
    time.sleep(5)
    if is_element_exist(driver,'button[class="setting-button"]'):
        Log("开启报表失败")
    else:
        Log("配置页面设置完毕，开启报表成功")

#首页经营利润卡片测试
def homePage(driver):
    profit=driver.find_element_by_css_selector('li[class="ct-main"]>p>span').text  #经营利润金额获取
    income=driver.find_element_by_css_selector('ul[class="line-list"]>li>p>span').text#获取经营收入金额
    cost=driver.find_element_by_css_selector('ul[class="line-list"]>li:nth-child(3)>p>span').text#获取经营成本金额
    inputTime=driver.find_element_by_css_selector('sub[class="line-sub"]>span>label').text#获取投入时间
    timeValue=driver.find_element_by_css_selector('sub[class="line-sub"]>span:nth-child(2)>label').text#获取时间附加值
    homePageList=[profit,income,cost,inputTime,timeValue]
    print(homePageList)
    for i in range(0,len(homePageList)):
        if homePageList[i]=='':
            Log("移动端首页经营利润卡片数据获取结果存在空数据")
            return None
            break
        elif  i==len(homePageList)-1:
            Log("移动端经营利润卡片有数据")
            return homePageList
        else:
            continue

#首页经营利润卡片数据核对测试
def compareHomePage(pcDriver,driver):
    homePageList=homePage(driver)
    box=pcDriver.find_element_by_css_selector(".ui-poplistedit-displayname")
    if box.get_attribute('title'):
        pcDriver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").clear()#清空当前搜索框text内容
    pcDriver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").send_keys("阿米巴利润汇总表")
    time.sleep(8)
    #pcDriver.find_element_by_xpath("/html/body/div[3]/div/div/div/li/span[3]").click()
    pcDriver.find_element_by_css_selector('li[class="k-state-focused"]').click()
    time.sleep(12)
    pcList=int(pcDriver.find_element_by_css_selector("span[data-kdid='sp_2_pagerlist2']").text)#检查pc端是否有数据
    time.sleep(2)
    if pcList!=0 and homePage!='':
        print("有数据")
        #获取pc端经营收入数据    style="background-color:#5CACEE; text-align:right;padding-right:5px;min-height:34px;color:#000000;"
        pcIncomeEle=pcDriver.find_elements_by_css_selector('div[style="background-color:#5CACEE; text-align:right;padding-right:5px;min-height:34px;color:#000000;"]')
        for ele in pcIncomeEle:
            #if ele.text !='':  
            eletemp=ele.find_element_by_css_selector('span')
            if eletemp.get_attribute('data-field')=="FINCOMEREALAMOUNT":
                #pcIncomeList.append(float(ele.find_element_by_css_selector('span[data-field="FINCOMEREALAMOUNT"]').text))
                if eletemp:
                    pcIncomeAmount+=float(eletemp.text)
        # pcIncomeEle=pcDriver.find_elements_by_css_selector('tr[class="k-alt"]>td>div>span[data-field="FINCOMEREALAMOUNT"]')
        # pcIncomeAmount=0
        # for ele in pcIncomeEle:
        #     if ele.text !='':
        #         pcIncomeAmount+=float(ele.text)
        #获取pc端经营成本数据：
        for ele in pcIncomeEle:
            #if ele.text !='':  
            eletemp=ele.find_element_by_css_selector('span')
            if eletemp.get_attribute('data-field')=="FCOSTREALAMOUNT":
                #pcIncomeList.append(float(ele.find_element_by_css_selector('span[data-field="FINCOMEREALAMOUNT"]').text))
                if eletemp:
                    pcCostAmount+=float(eletemp.text)

        # pcCostEle=pcDriver.find_elements_by_css_selector('tr[class="k-alt"]>td>div>span[data-field="FCOSTREALAMOUNT"]')
        # pcCostAmount=0
        # for ele in pcCostEle:
        #     if ele.text !='':
        #         pcCostAmount+=float(ele.text)
        print(pcIncomeAmount,pcCostAmount)
        #判断移动端、pc端收入、成本数据是否一致
        for i in range(0,3):
            if "," in homePageList[i]:
                homePageList[i]=homePageList[i].replace(",","")
        prof=float(homePageList[0])
        income=float(homePageList[1])
        cost=float(homePageList[2])
        if prof==income-cost:
            if income==pcIncomeAmount and cost==pcCostAmount:
                Log("移动端、pc端经营收入、经营支出数据相等")
            else:
                Log("移动端、pc端经营收入、经营支出数据不相等，请检查")
        else:
            Log("移动端经营收入、经营支出数据相减不等于经营利润表数据，请检查")
    elif pcList==0 and homePage=='':
        Log("pc端、移动端经营利润数据均为空")
    #判断附加时间测试
    if box.get_attribute('title'):
        pcDriver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").clear()#清空当前搜索框text内容
    if is_element_exist(pcDriver,'span[class=" k-i-close mainTabCloseButton"]'):
        pcDriver.find_element_by_css_selector('span[class=" k-i-close mainTabCloseButton"]').click()#关闭当前页签
    pcDriver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").send_keys("阿米巴投入时间")
    time.sleep(8)
    #pcDriver.find_element_by_xpath("/html/body/div[3]/div/div/div/li/span[3]").click()
    pcDriver.find_element_by_css_selector('li[class="k-state-focused"]').click()
    time.sleep(12)
    pcList=int(pcDriver.find_element_by_css_selector("span[data-kdid='sp_2_pagerlist2']").text)#检查pc端是否有数据
    time.sleep(2)
    if pcList!=0 and homePage!='':
        #获取投入时间
        inputTimeEle=pcDriver.find_elements_by_css_selector('span[data-field="FAMOEABTIME"]')
        pcInputTime=0
        for i in range(0,len(inputTimeEle)):
            pcInputTime+=float(inputTimeEle[i].text)
        for i in range(3,5):
            if "," in homePageList[i]:
                homePageList[i]=homePageList[i].replace(",","")
        inputTime=float(homePageList[3])
        timeValue=float(homePageList[4])
        if inputTime==pcInputTime:
            Log("移动端、pc端阿米巴投入时间相等")
        else:
            Log("移动端、pc端阿米巴投入时间不相等，请检查！")
    elif pcList==0 and homePage!='':
        Log("pc端投入时间为空，请检查！")
    elif homePage=='' and pcList!=0:
        Log("移动端端投入时间为空，请检查！")
    else:
        Log("pc端、移动端投入时间均为空")
        
#流水查询页面获取数据,返回阿米巴单元：流水条数组成的字典
def flowQuery(driver):
    driver.find_element_by_css_selector('ul[class="home-cards"]>li>i').click()#点击进入流水查询页面
    time.sleep(3)
    flowItem=[]
    #获取每个阿米巴对应的订单条数
    for i in range(0,len(amoebaName)):
        driver.find_element_by_css_selector('section[class="nav-amoeba"]>i[class="m-arrow-right down"]').click()
        setAmoeba(driver,i)
        flowItemEle=driver.find_elements_by_css_selector('h3[class="hairlines-bottom flow-content"]')
        flowItem.append(len(flowItemEle))
        time.sleep(3)
    flowDict=dict(zip(amoebaName,flowItem))
    driver.get(homePageUrl)#回到阿米巴报表首页
    return flowDict

#流水查询页面数据核对测试
def compareFlowQuery(pcDriver,driver):
    flowDict=flowQuery(driver)
    box=pcDriver.find_element_by_css_selector(".ui-poplistedit-displayname")
    if box.get_attribute('title'):
        pcDriver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").clear()#清空当前搜索框text内容
    if is_element_exist(pcDriver,'span[class=" k-i-close mainTabCloseButton"]'):
        pcDriver.find_element_by_css_selector('span[class=" k-i-close mainTabCloseButton"]').click()#关闭当前页签
    pcDriver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").send_keys("经营流水账查询")
    time.sleep(8)
    #pcDriver.find_element_by_xpath("/html/body/div[3]/div/div/div/li/span[3]").click()
    pcDriver.find_element_by_css_selector('li[class="k-state-focused"]').click()
    time.sleep(12)
    pcList=int(pcDriver.find_element_by_css_selector("span[data-kdid='sp_2_pagerlist2']").text)#检查pc端是否有数据
    time.sleep(2)
    if pcList!=0 and flowDict!='':
        print("有数据")
        amoebaList=[]
        amoebaDict={}
        #获取pc端分录行元素列表
        #entries=pcDriver.find_elements_by_css_selector('tr[role="row"]')
        amoebaNameEles=pcDriver.find_elements_by_css_selector('span[data-field="FAMOEABID_FNAME"]')
        #print(entries)
        for ele in amoebaNameEles:
            amoebaName=ele.text
            if amoebaName!=' ' and amoebaName not in amoebaList:
                amoebaDict[amoebaName]=1
                amoebaList.append(amoebaName)
            elif amoebaName!=' ' and amoebaName in amoebaList:
                amoebaDict[amoebaName]+=1
                amoebaList.append(amoebaName)
            elif amoebaName==' ' :#当阿米巴单元为空时代表是某条订单的分录之一，此时取到的text为一个空格
                amoebaDict[amoebaList[len(amoebaList)-1]]+=1   #当阿米巴单元为空时代表是某条订单的分录之一，阿米巴单元名称与上一条分录行名称应该是一致的
        print(amoebaDict)
        for key in flowDict:
            if key in amoebaDict and flowDict[key]!=amoebaDict[key]:
                Log("移动端与pc端阿米巴单元%s流水数目不一致，请检查！"%key)
                break
            elif key in amoebaDict and flowDict[key]==amoebaDict[key]:
                Log("移动端与pc端阿米巴单元%s流水数目一致"%key)
                continue
            elif key not in amoebaDict and flowDict[key]==0:
                Log("移动端与pc端阿米巴单元%s流水数目一致，均为0"%key)
            elif key not in amoebaDict and flowDict[key]!=0:
                Log("移动端与pc端阿米巴单元%s流水数目不一致，移动端有数据，pc端没有，请检查！"%key)
    elif pcList!=0 and flowDict=='':
        Log("移动端流水数据为空，pc端有数据，请检查！")
    elif pcList==0 and flowDict!='':
        Log("移动端流水有数据，pc端数据为空，请检查！")
    elif pcList==0 and flowDict=='':
        Log("移动端、pc端流水数据均为空，测试通过")
                


#设置阿米巴单元
def setAmoeba(driver,loaction):
    #点击展开阿米巴单元
    #driver.find_element_by_css_selector('section[class="nav-amoeba"]>i[class="m-arrow-right down"]').click()
    amoebaEles=driver.find_elements_by_css_selector('p[class="mint-indexsection-item"]')
    amoebaEles[loaction].find_element_by_css_selector('i').click()
    driver.find_element_by_css_selector('a[class="confirm"]').click()
    time.sleep(5)

    

#移动端新增流水记录
def addBill(driver,loaction):
    driver.find_element_by_css_selector('ul[class="home-cards"]>li:nth-child(2)>i').click()#点击进入流水录入页面
    time.sleep(3)
    #检查必录未录时是否无法提交
    driver.find_element_by_css_selector('p[class="m-btn-square"]').click()#直接点击提交
    time.sleep(2)
    if is_element_exist(driver,'p[class="m-btn-square"]'):
        Log("有必录项未录入，提交失败")
    else:
        Log("提交流水成功，请检查必录项控制")
    #录入流水
    driver.find_element_by_css_selector('i[class="m-arrow-right"]').click()
    time.sleep(5)
    setAmoeba(driver,loaction)
    #driver.get(homePageUrl)

#移动端账户余额页面
def balanceGroup(driver):
    driver.find_element_by_css_selector('ul[class="home-cards"]>li:nth-child(3)>i').click()#点击进入账户余额页面
    time.sleep(3)
    if is_element_exist(driver,'ul[class="group-list"]>li'):
        listEle=driver.find_elements_by_css_selector('ul[class="group-list"]>li')
        amoebaList=[]
        balanceList=[]
        for ele in listEle:
            amoebaList.append(ele.find_element_by_css_selector('h3[class="list-name"]').text)
            balanceList.append(float(ele.find_element_by_css_selector('div>p>span').text))
        balanceDict=dict(zip(amoebaList,balanceList))
        print(balanceDict)
        Log("已获取到移动端阿米巴账户余额数据")
        return(balanceDict)
    else:
        Log("移动端账户余额数据为空")
        return None
    driver.get(homePageUrl)#回到阿米巴报表首页

#账户余额数据核对测试
def compareBalanceGruop(pcDriver,driver):
    balanceDict=balanceGroup(driver)
    box=pcDriver.find_element_by_css_selector(".ui-poplistedit-displayname")
    if box.get_attribute('title'):
        pcDriver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").clear()#清空当前搜索框text内容
    if is_element_exist(pcDriver,'span[class=" k-i-close mainTabCloseButton"]'):
        pcDriver.find_element_by_css_selector('span[class=" k-i-close mainTabCloseButton"]').click()#关闭当前页签
    pcDriver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").send_keys("阿米巴账户余额表")
    time.sleep(8)
    #pcDriver.find_element_by_xpath("/html/body/div[3]/div/div/div/li/span[3]").click()
    pcDriver.find_element_by_css_selector('li[class="k-state-focused"]').click()
    time.sleep(12)
    pcList=int(pcDriver.find_element_by_css_selector("span[data-kdid='sp_2_pagerlist2']").text)#检查pc端是否有数据
    time.sleep(2)
    if pcList!=0 and balanceDict!='':
        print("有数据")
        pcAmoebaList=[]
        pcBalanceList=[]
        #dataListEle=pcDriver.find_elements_by_css_selector('tbody[role="rowgroup"]>tr')
        businessList=[]#经营分类名称列表
        #获取账户余额列表上所有的阿米巴单元、经营分类名称、账户余额期末余额金额
        amoebaEles=pcDriver.find_elements_by_css_selector('span[data-field="FAMEBAUNITNAME"]')
        for ele in amoebaEles:
            pcAmoebaList.append(ele.text)
        businessEles=pcDriver.find_elements_by_css_selector('span[data-field="FACCOUNTNAME"]')
        for ele in businessEles:
            businessList.append(ele.text)
        balanceEles=pcDriver.find_elements_by_css_selector('span[data-field="FENDBALANCEFOR"]')
        for ele in balanceEles:
            pcBalanceList.append(float(ele.text))
        count=0#记住初始位置
        for i in range(0,len(businessList)):#去掉不属于合计的阿米巴单元、期末余额值
            if businessList[i]!="合计":
                del pcAmoebaList[i-count]
                del pcBalanceList[i-count]
                count+=1#每删除一个元素初始位置加一
            else:
                continue        
        pcBalanceDict=dict(zip(pcAmoebaList,pcBalanceList))
        print(pcBalanceDict)
        for key in balanceDict:
            if key in pcBalanceDict:
                if balanceDict[key]==pcBalanceDict[key]:
                    Log("移动端与pc端阿米巴单元%s账户余额数目一致"%key)
                else:
                    Log("移动端与pc端阿米巴单元%s账户余额数目不一致，请检查"%key)
            else:
                Log("pc端阿米巴账户余额列表找不到%s阿米巴单元"%key)
    elif pcList!=0 and balanceDict=='':
        Log("移动端账户余额数据为空，pc端有数据，请检查！")
    elif pcList==0 and balanceDict!='':
        Log("移动端账户余额有数据，pc端数据为空，请检查！")
    elif pcList==0 and balanceDict=='':
        Log("移动端、pc端账户余额数据均为空，测试通过")

#移动端账户余额列表（账户流水）页面数据获取
def balanceList(driver):
    driver.find_element_by_css_selector('ul[class="home-cards"]>li:nth-child(3)>i').click()#点击进入账户余额页面
    time.sleep(3)
    driver.find_element_by_css_selector('h3[class="list-name"]').click()#点击进入账户余额列表
    time.sleep(3)
    businessList=[]
    businessAmount=[]
    businessDict={}
    dictList=[]
    for i in range(0,len(amoebaName)):
        driver.find_element_by_css_selector('i[class="m-arrow-right down"]').click()
        setAmoeba(driver,i)
        cardEle=driver.find_elements_by_css_selector('li[class="card-item"]')
        for ele in cardEle:
            businessList.append(ele.find_element_by_css_selector('div[class="item-block"]>p').text)
            businessAmount.append(float(ele.find_element_by_css_selector('footer[class="item-foot"]>p>span').text))  
        tempDict=dict(zip(businessList,businessAmount)) 
        dictList.append(tempDict)
    businessDict=dict(zip(amoebaName,dictList))
    Log("获取到移动端各个阿米巴单元账户余额详情列表数据")
    time.sleep(3) 
    print("======================================")
    print(businessAmount)
    print("////////////////////////////////////////")
    print(businessList)
    print("======================================")
    print(businessDict)
    driver.get(homePageUrl)#回到阿米巴报表首页
    return businessDict
    

#账户余额列表(账户流水)页面数据核对
def compareBalanceList(driver,pcDriver):
    businessDict=balanceList(driver)
    box=pcDriver.find_element_by_css_selector(".ui-poplistedit-displayname")
    if box.get_attribute('title'):
        pcDriver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").clear()#清空当前搜索框text内容
    if is_element_exist(pcDriver,'span[class=" k-i-close mainTabCloseButton"]'):
        pcDriver.find_element_by_css_selector('span[class=" k-i-close mainTabCloseButton"]').click()#关闭当前页签
    pcDriver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").send_keys("阿米巴账户余额表")
    time.sleep(8)
    #pcDriver.find_element_by_xpath("/html/body/div[3]/div/div/div/li/span[3]").click()
    pcDriver.find_element_by_css_selector('li[class="k-state-focused"]').click()
    time.sleep(20)
    pcList=int(pcDriver.find_element_by_css_selector("span[data-kdid='sp_2_pagerlist2']").text)#检查pc端是否有数据
    time.sleep(2)
    if pcList!=0 and businessDict!='':
        print("有数据")
        pcAmoebaList=[]
        pcBalanceList=[]
        #dataListEle=pcDriver.find_elements_by_css_selector('tbody[role="rowgroup"]>tr')
        businessList=[]#经营分类名称列表
        #获取账户余额列表上所有的阿米巴单元、经营分类名称、账户余额期末余额金额
        amoebaEles=pcDriver.find_elements_by_css_selector('span[data-field="FAMEBAUNITNAME"]')
        for ele in amoebaEles:
            pcAmoebaList.append(ele.text)
        businessEles=pcDriver.find_elements_by_css_selector('span[data-field="FACCOUNTNAME"]')
        for ele in businessEles:
            businessList.append(ele.text)
        balanceEles=pcDriver.find_elements_by_css_selector('span[data-field="FENDBALANCEFOR"]')
        for ele in balanceEles:
            pcBalanceList.append(float(ele.text))
        pcBalanceDict={}
        pcDict=dict(zip(businessList,pcBalanceList))
        for i in range(0,len(pcAmoebaList)):
            if pcAmoebaList[i] not in pcBalanceDict and businessList[i]!="合计":
                dict1={businessList[i]:pcBalanceList[i]}
                pcBalanceDict[pcAmoebaList[i]]=dict1
            elif pcAmoebaList[i] in pcBalanceDict and businessList[i]!="合计":
                key=pcBalanceDict[pcAmoebaList[i]]
                key[businessList[i]]=pcBalanceList[i]
            else:
                continue
        print(pcBalanceDict)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(businessDict)
        
        for key in pcBalanceDict:
            if key in businessDict:
                keys=(pcBalanceDict[key]).keys()
                values=(pcBalanceDict[key]).values()
                for i in keys:
                    if i in businessDict[key]:
                        if (pcBalanceDict[key])[i]==(businessDict[key])[i]:
                            Log("移动端与pc端阿米巴单元%s下%s账户余额数目一致"%(key,i))
                        else:
                            Log("移动端与pc端阿米巴单元%s下%s账户余额数目不一致，请检查！"%(key,i))
            else:
                Log("移动端阿米巴账户余额列表找不到%s阿米巴单元"%key)
    elif pcList!=0 and businessDict=='':
        Log("移动端账户余额详情数据为空，pc端有数据，请检查！")
    elif pcList==0 and businessDict!='':
        Log("移动端账户余额详情有数据，pc端数据为空，请检查！")
    elif pcList==0 and businessDict=='':
        Log("移动端、pc端账户余额详情数据均为空，测试通过")

#移动端利润排名页面数据获取
def profitRanking(driver):
    driver.find_element_by_css_selector('ul[class="home-cards"]>li:nth-child(5)>i').click()#点击进入利润排名页面
    time.sleep(3)

    proList=[]#利润数据列表
    amoebaList=[]#阿米巴数据列表
    proDict={}
    if is_element_exist(driver,'h3[class="range-amount"]'):
        proEleList=driver.find_elements_by_css_selector('h3[class="range-amount"]')
        for ele in proEleList:
            proList.append(ele.find_element_by_css_selector('span[class="amoeba"]').text)
            amoebaList.append(float(ele.find_element_by_css_selector('span[class="amount"]').text))  
        proDict=dict(zip(proList,amoebaList)) 
        Log("获取到移动端阿米巴利润数据")
    else:
        Log("阿米巴利润排名页面无数据")
    print(proDict)
    driver.get(homePageUrl)#回到阿米巴报表首页
    return proDict

#阿米巴利润数据核对
def compareProRanking(driver,pcDriver):
    proDict=profitRanking(driver)
    box=pcDriver.find_element_by_css_selector(".ui-poplistedit-displayname")
    if box.get_attribute('title'):
        pcDriver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").clear()#清空当前搜索框text内容
    if is_element_exist(pcDriver,'span[class=" k-i-close mainTabCloseButton"]'):
        pcDriver.find_element_by_css_selector('span[class=" k-i-close mainTabCloseButton"]').click()#关闭当前页签
    pcDriver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").send_keys("阿米巴利润汇总表")
    time.sleep(8)
    pcDriver.find_element_by_css_selector('li[class="k-state-focused"]').click()
    time.sleep(20)
    pcList=int(pcDriver.find_element_by_css_selector("span[data-kdid='sp_2_pagerlist2']").text)#检查pc端是否有数据
    time.sleep(2)
    if pcList!=0 and proDict!='':
        Log("有数据")
        pcIncomeList=[]
        pcCostList=[]
        pcProList=[]#style="background-color:#FFFFFF; text-align:right;padding-right:5px;min-height:34px;color:#000000;"
        #pcIncomeEle=pcDriver.find_elements_by_css_selector('tr[class="k-alt"]>td:nth-child(5)>div>span[data-field="FINCOMEREALAMOUNT"]')
        pcIncomeEle=pcDriver.find_elements_by_css_selector('div[style="background-color:#FFFFFF; text-align:right;padding-right:5px;min-height:34px;color:#000000;"]')
        eleAmount=0
        for ele in pcIncomeEle:                                 
            #if ele.text !='':  
            eletemp=ele.find_element_by_css_selector('span')
            if eletemp.get_attribute('data-field')=="FINCOMEREALAMOUNT":
                eleAmount+=1
                #pcIncomeList.append(float(ele.find_element_by_css_selector('span[data-field="FINCOMEREALAMOUNT"]').text))
                if eletemp.text:
                    pcIncomeList.append(float(eletemp.text))
                else:
                    pcIncomeList.append(0)
            #获取pc端经营成本数据：
            if eletemp.get_attribute('data-field')=="FCOSTREALAMOUNT":
                #pcIncomeList.append(float(ele.find_element_by_css_selector('span[data-field="FINCOMEREALAMOUNT"]').text))
                if eletemp.text:
                    pcCostList.append(float(eletemp.text))
                else:
                    pcCostList.append(0)
            
        print(pcIncomeList)
        # #获取pc端经营成本数据：
        # for ele in pcIncomeEle:
        #     #if ele.text !='':  
        #     eletemp=ele.find_element_by_css_selector('span')
        #     if eletemp.get_attribute('data-field')=="FCOSTREALAMOUNT":
        #         #pcIncomeList.append(float(ele.find_element_by_css_selector('span[data-field="FINCOMEREALAMOUNT"]').text))
        #         if eletemp.text:
        #             pcCostList.append(float(eletemp.text))
        #         else:
        #             pcCostList.append(0)
        print(pcCostList)
        #获取pc端阿米巴单元名称
        amoebaNameList=[]
        amoebaEles=pcDriver.find_elements_by_css_selector('span[data-field="FAMEBAUNITNAME"]')
        for ele in amoebaEles:
            if ele.text:
                amoebaNameList.append(ele.text)
        #获取利润
        for i in range(0,eleAmount):
            pcProList.append(pcIncomeList[i]-pcCostList[i])

        pcProDict=dict(zip(amoebaNameList,pcProList)) 
        print(pcIncomeList,pcCostList,pcProList,pcProDict)

        for key in pcProDict:
            if key in proDict:
                if pcProDict[key]==proDict[key]:
                    Log("移动端与pc端阿米巴单元%s利润数目一致"%key)
                else:
                    Log("移动端与pc端阿米巴单元%s利润数目不一致，请检查！"%key)
            else:
                Log("移动端阿米巴利润排名列表找不到%s阿米巴单元"%key)
    elif pcList!=0 and proDict=='':
        Log("移动端利润详情数据为空，pc端有数据，请检查！")
    elif pcList==0 and proDict!='':
        Log("移动端利润详情有数据，pc端数据为空，请检查！")
    elif pcList==0 and proDict=='':
        Log("移动端、pc端利润详情数据均为空，测试通过")



    


    
    
    


    

