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
    driver.get("http://v-mobile-at/k3cloud/KDMobile/SaleAnalysis/index.html#/")#进入业绩页面
    Log("进入移动销售-业绩")
    time.sleep(6)

# #获取用户对应的联系对象
# def getLinkObject(driver,USERNAME):
#     login_pc(driver,'administrator','888888')#管理员登录
#     driver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").send_keys('查询用户')
#     time.sleep(6)
#     driver.find_element_by_css_selector('li[class="k-state-focused"]').click() 
#     time.sleep(8)
#     userEles=driver.find_elements_by_css_selector('span[data-field="FNAME"]>a')#获取
#     for ele in userEles:
#         if ele.text==USERNAME:
#             eles

def select_MobFilterScheme(driver,orgName):
    print(orgName)
    time.sleep(3)
    driver.find_element_by_css_selector(".head-org").click()# 点击过滤方案下拉列表
    time.sleep(5)
    orgSelectedList=[]                        
    orgChkBoxEles=driver.find_elements_by_css_selector('.mint-indexsection-item')#获取组织列表的元素list      driver.execute_script('return $(".kd-grid-sumfooterdiv,div[data-field=\'FALLAMOUNT_LC\']").text()')
    print(orgChkBoxEles)
    for ele in orgChkBoxEles:
        if is_element_exist(ele,'i[class="m-checked checked"]'):
            orgSelectedList.append(ele.text)
    MobChangeOrg(orgChkBoxEles, orgSelectedList, orgName)
    #Log("设置移动端的组织如下："+orgName)
    time.sleep(6)
    driver.find_element_by_css_selector(".confirm").click()#点击确定
    
def MobChangeOrg(orgChkBoxEles, orgSelectedList, orgName):
    selectedOrgSet = set(orgSelectedList).difference(set(orgName))
    unSelectedOrgSet = set(orgName).difference(set(orgSelectedList))#difference()取出现在第一个集合但不出现在第二个集合的元素  对称差symmetric_difference(y)
    if len(selectedOrgSet) !=0:
        for org in selectedOrgSet:
            [ele.click()  for ele in orgChkBoxEles if ele.text == org]
    for org in unSelectedOrgSet:
        [ele.click() for ele in orgChkBoxEles if ele.text == org]
        
    pass

def select_PcFilterScheme(driver,orgName):
    time.sleep(3)
    driver.find_element_by_css_selector('span[id$="BILLMENU_TOOLBAR-tbFilter"]').click()#点击过滤方案
    time.sleep(5)
    orgSelectedBox = driver.find_element_by_css_selector('div[id$="Filter-FORGLIST-EDITOR"]>div>span>span>.ui-poplistedit-displayname')

    orgSelectedList = orgSelectedBox.text.replace(' ','').split(',')

    orgSelectedBox.click()
    time.sleep(1)
    orgChkBoxEles = driver.find_elements_by_css_selector('button[for$="value"]')
    # 修改组织
    PcChangeOrg(orgChkBoxEles, orgSelectedList,orgName)
    time.sleep(3)
    driver.find_element_by_css_selector("a[id$='Filter-FBTNOK_c']").click()#点击确定

# 修改组织列表
def PcChangeOrg(orgChkBoxEles, orgSelectedList, orgName):
    selectedOrgSet = set(orgSelectedList).difference(set(orgName))
    unSelectedOrgSet = set(orgName).difference(set(orgSelectedList))

    for org in selectedOrgSet:
        [ele.click()  for ele in orgChkBoxEles if ele.text.strip() == org]
    
    for org in unSelectedOrgSet:
        [ele.click() for ele in orgChkBoxEles if ele.text.strip() == org]
        
    pass

#移动销售-业绩首页业务员销售收款金额获取
def getMobSalRect(driver):
    driver.get("http://v-mobile-at/k3cloud/KDMobile/SaleAnalysis/index.html#/")#进入业绩页面
    time.sleep(4)
    if is_element_exist(driver,'li[class="banner-li"]>p>span'):
        salAmount=driver.find_element_by_css_selector('li[class="banner-li"]>p>span').text
        Log("业绩首页有对应业务员的销售收款金额"+salAmount)
        return salAmount
    else:
        Log("业绩首页未找到对应业务员销售收款金额")
        return None

#移动端销售员收款排名报表 
def mobSaleRecRankingReport(driver):
    time.sleep(2)
    driver.get("http://v-mobile-at/k3cloud/KDMobile/SaleAnalysis/index.html#/SaleRecRanking")#销售员收款排名报表
    time.sleep(5)
    if is_element_exist(driver, 'div[class="item-content"]'):  #获取数据元素列表
        orgListEles=driver.find_elements_by_css_selector('div[class="item-content"]')
    else:
        orgListEles=None
    print(orgListEles)
    time.sleep(2)
    saleRecRankingReport={}

    if orgListEles!=None:
        saleName=[]
        saleAmount=[]
        for ele in orgListEles:
            saleName.append(ele.find_element_by_css_selector('p').text)#获取销售员名称
            saleAmount.append(ele.find_element_by_css_selector('span>span').text)#获取销售员对应的销售额字段
        saleRecRankingReport=dict(zip(saleName,saleAmount))#生成销售员：销售额键值对
        print(saleRecRankingReport)
        Log("移动端销售员收款排名报表有数据")
        return saleRecRankingReport#返回销售员：销售额的键值对
    else:
        Log("移动端销售员收款排名报表暂无数据")
        return None

#对比移动端和pc端销售员收款排名报表的销售数据是否相等
def compareSaleRecRankingReport(mobDriver,pcDriver,allOrgName):
    mobDriver.get("http://v-mobile-at/k3cloud/KDMobile/SaleAnalysis/index.html#/SaleRecRanking")#销售员收款排名报表
    time.sleep(4)
    select_MobFilterScheme(mobDriver,allOrgName)#设置移动端组织列表
    time.sleep(5)
    salRecReportVal=mobSaleRecRankingReport(mobDriver)#调用移动端访问销售员收款排名报表
    time.sleep(2)
    mobDriver.find_element_by_css_selector(".head-org").click()# 点击过滤方案下拉列表
    time.sleep(2)
    orgChkBoxEles=mobDriver.find_elements_by_css_selector('.mint-indexsection-item')#获取组织列表的元素list     
    time.sleep(2)
    orgSelectedList=[]
    for ele in orgChkBoxEles:
        if is_element_exist(ele,'i[class="m-checked checked"]'):#获取已选组织列表
            orgSelectedList.append(ele.text)
        else:
            orgSelectedList=None
    time.sleep(2)
    mobDriver.find_element_by_css_selector(".confirm").click()#点击确定
    time.sleep(2)
    box=pcDriver.find_element_by_css_selector(".ui-poplistedit-displayname")
    if box.get_attribute('title'):
        pcDriver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").clear()#清空当前搜索框text内容
    pcDriver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").send_keys('收款单列表')#打开收款单列表                                                                                                                                                                     单列表
    time.sleep(8)
    pcDriver.find_element_by_css_selector('li[class="k-state-focused"]').click() 
    time.sleep(6)
    select_PcFilterScheme(pcDriver,orgSelectedList)#按照移动端报表所选组织设置pc端组织
    pcList=int(pcDriver.find_element_by_css_selector("span[data-kdid='sp_2_pagerlist2']").text)#检查pcdaunt是否有数据????????????????????????????1第？页/共n页
    time.sleep(2)
    if salRecReportVal and orgSelectedList!=None and pcList!=0:
        saleNameList=[]
        nameEles=pcDriver.find_elements_by_css_selector('span[data-field="FSALEERID_FNAME"]')#销售员元素列表
        for ele in nameEles:
            saleNameList.append(ele.text)
        noRepeatName=list(set(saleNameList))#不重复的销售员名称
        #noRepeatSale=[]
        pcSalAmountList=[]
        pcIncomeEles=pcDriver.find_elements_by_css_selector('span[data-field="FREALRECAMOUNT_H"]')#实收金额本位币元素列表     多了个币别符号？？？？？？？？
        for ele in pcIncomeEles:
            pcSalAmountList.append((ele.text)[1:])#截取从第二位到结尾字符
        
        noRepeatDict={}

        for i in range(0,len(saleNameList)):
            name=saleNameList[i]
            if noRepeatDict.__contains__(name):
                temp=float(noRepeatDict[name])
                temp+=float(pcSalAmountList[i])
                noRepeatDict[name]=temp
            else:
                noRepeatDict[name]=pcSalAmountList[i]
        print(noRepeatDict)

        for i in noRepeatName:#依次让pc端等于移动端所选组织，检查金额是否相等
            salAmount=salRecReportVal.get(i)#i产品对应的收入金额
            pcSalAmount=noRepeatDict.get(i)#i产品对应的收入金额
            if i==linkObject:#检查首页，业务员对应的收款金额是否正确
                if getMobSalRect(mobDriver):
                    salRect=float(getMobSalRect(mobDriver))
                    if salRect==float(salAmount) and salRect==float(pcSalAmount):
                        Log("移动销售-业绩，首页业务员销售收款金额与移动端报表详情页面、pc端该业务员收款金额一致")
                    else:
                        Log("移动销售-业绩，首页业务员销售收款金额与移动端报表详情页面、pc端该业务员收款金额不一致，请检查！")
                else:
                    Log("移动销售-业绩，首页业务员销售收款金额不存在")
            if salAmount!= None and pcSalAmountList != '':
                if isNum(salAmount) and isNum(pcSalAmount):
                    print(float(salAmount))
                    print(float(pcSalAmount))
                    if float(salAmount)==float(pcSalAmount):#两个值相等时，pass
                        Log(i+":销售员收款排名报表的销售数据：移动端销售金额与pc端销售金额相等")
                    else:
                        Log(i+":销售员收款排名报表的销售数据：移动端销售金额与pc端销售金不相等")
                else:
                    Log(i+":销售员收款排名报表的销售数据：有元素不为数字，请检查数值") 
            elif salAmount==None and pcSalAmountList=='':
                Log(i+"销售员收款排名报表的销售数据：移动端、pc端均无数据")  
    elif pcList==0 and salRecReportVal==False:
       Log("销售员收款排名报表的销售数据：pc端暂无数据，金额为0,金额相等")
    elif pcList==None:
        Log("销售员收款排名报表的销售数据：有不存在的元素")
    elif pcList==0 and salRecReportVal!=False:
        Log("销售员收款排名报表的销售数据：pc端数据为0，移动端有数据")
    elif pcList!=0 and salRecReportVal==False:
        Log("销售员收款排名报表的销售数据：移动端数据为0，pc端有数据")
    pcDriver.find_element_by_css_selector('span[class=" k-i-close mainTabCloseButton"]').click()

#移动端客户销售占比分析报表
def mobCustSaleProportionReport(driver):
    time.sleep(2)
    driver.get("http://v-mobile-at/k3cloud/KDMobile/SaleAnalysis/index.html#/CustSaleProportion")
    time.sleep(5)
    if is_element_exist(driver, 'h3[class="item-content"]'):  #获取数据元素列表
        orgListEles=driver.find_elements_by_css_selector('h3[class="item-content"]')
    else:
        orgListEles=None
    print(orgListEles)
    time.sleep(2)
    saleProReport={}

    if orgListEles!=None:
        saleName=[]
        saleAmount=[]
        for ele in orgListEles:
            saleName.append(ele.find_element_by_css_selector('div>span').text)#获取客户名称
            saleAmount.append(ele.find_element_by_css_selector('div span:nth-child(2)>span').text)#获取客户对应的销售额字段
        saleProReport=dict(zip(saleName,saleAmount))#生成客户：销售额键值对
        print(saleProReport)
        Log("移动端客户销售占比分析报表有数据")
        return saleProReport#返回客户：销售额的键值对
    else:
        Log("移动端客户销售占比分析报表暂无数据")
        return None
    
#对比移动端和pc端客户销售占比分析报表的销售数据是否相等
def compareCustSaleProportionReport(mobDriver,pcDriver,allOrgName):
    mobDriver.get("http://v-mobile-at/k3cloud/KDMobile/SaleAnalysis/index.html#/CustSaleProportion")#进入客户销售占比分析报表
    time.sleep(4)
    select_MobFilterScheme(mobDriver,allOrgName)#设置移动端组织列表
    time.sleep(5)
    saleProReportVal=mobCustSaleProportionReport(mobDriver)#调用移动端访问客户销售占比分析报表
    time.sleep(2)
    mobDriver.find_element_by_css_selector(".head-org").click()# 点击过滤方案下拉列表
    time.sleep(2)
    orgChkBoxEles=mobDriver.find_elements_by_css_selector('.mint-indexsection-item')#获取组织列表的元素list     
    time.sleep(2)
    orgSelectedList=[]
    for ele in orgChkBoxEles:
        if is_element_exist(ele,'i[class="m-checked checked"]'):#获取已选组织列表
            orgSelectedList.append(ele.text)
        else:
            orgSelectedList=None
    time.sleep(2)
    mobDriver.find_element_by_css_selector(".confirm").click()#点击确定
    time.sleep(2)
    box=pcDriver.find_element_by_css_selector(".ui-poplistedit-displayname")
    if box.get_attribute('title'):
        pcDriver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").clear()#清空当前搜索框text内容
    pcDriver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").send_keys('销售订单列表')#打开销售订单                                                                                                                                                                       单列表
    time.sleep(8)
    pcDriver.find_element_by_css_selector('li[class="k-state-focused"]').click() 
    time.sleep(6)
    select_PcFilterScheme(pcDriver,orgSelectedList)#按照移动端报表所选组织设置pc端组织
    pcList=int(pcDriver.find_element_by_css_selector("span[data-kdid='sp_2_pagerlist2']").text)#检查pcdaunt是否有数据????????????????????????????1第？页/共n页
    time.sleep(2)
    if saleProReportVal and orgSelectedList!=None and pcList!=0:

        ele=pcDriver.find_element_by_css_selector('div[data-role="virtualscrollable"]>div>table>tbody')#获取数据列表元素
        eleList=ele.find_elements_by_css_selector('tr[role="row"]')##获取数据列表的元素列表
        custNameList=[]
        pcSalAmountList=[]
        noRepeatDict={}
        for ele in eleList:#依次循环pc端销售订单列表每一条订单，找到客户名称、价税合计、业务员（销售员）名称
            custName=ele.find_element_by_css_selector('td:nth-child(6)>span[data-field="FCUSTID_FNAME"]').text#客户
            custNameList.append(custName)
            pcIncome=ele.find_element_by_css_selector('td:nth-child(14)>span[data-field="FALLAMOUNT_LC"]').text#物料价税合计本位币
            pcSalAmount=pcIncome[1:]#截取从第二位到结尾字符
            pcSalAmountList.append(pcSalAmount)
            obj=ele.find_element_by_css_selector('td:nth-child(8)>span[data-field="FSALERID_FNAME"]').text#业务员
            if obj==linkObject:           #只有当销售员的名称等于当前用户的联系对象时，数据才是我们需要的，才加入到字典中
                if noRepeatDict.__contains__(custName): 
                    temp=float(noRepeatDict[custName])
                    temp+=float(pcSalAmount)
                    noRepeatDict[custName]=temp
                else:
                    noRepeatDict[custName]=pcSalAmount


        noRepeatName=list(set(custNameList))#不重复的客户名称
        print(noRepeatDict)
        if noRepeatDict:#当pc端客户：销售额字典不为空时，才进行移动端、pc端数据的比较
            for i in noRepeatName:#依次检查不重复的客户名称，检查其对应金额是否相等
                salAmount=saleProReportVal.get(i)#i产品对应的收入金额
                pcSalAmount=noRepeatDict.get(i)#i产品对应的收入金额
                if salAmount!= None and pcSalAmountList != '':
                    if isNum(salAmount) and isNum(pcSalAmount):
                        print(float(salAmount))
                        print(float(pcSalAmount))
                        if float(salAmount)==float(pcSalAmount):#两个值相等时，pass
                            Log(i+":客户销售占比分析报表的销售数据：移动端销售金额与pc端销售金额相等")
                        else:
                            Log(i+":客户销售占比分析报表的销售数据：移动端销售金额与pc端销售金不相等")
                    else:
                        Log(i+":客户销售占比分析报表的销售数据：有元素不为数字，请检查数值") 
                elif salAmount==None and pcSalAmountList=='':
                    Log(i+"客户销售占比分析报表的销售数据：移动端、pc端均无数据")  
    elif pcList==0 and saleProReportVal==False:
       Log("客户销售占比分析报表的销售数据：pc端暂无数据，金额为0,金额相等")
    elif pcList==None:
        Log("客户销售占比分析报表的销售数据：有不存在的元素")
    elif pcList==0 and saleProReportVal!=False:
        Log("客户销售占比分析报表的销售数据：pc端数据为0，移动端有数据")
    elif pcList!=0 and saleProReportVal==False:
        Log("客户销售占比分析报表的销售数据：移动端数据为0，pc端有数据")
    pcDriver.find_element_by_css_selector('span[class=" k-i-close mainTabCloseButton"]').click()

#移动端产品销售占比分析报表
def mobProSaleProportionReport(driver):
    time.sleep(2)
    driver.get("http://v-mobile-at/k3cloud/KDMobile/SaleAnalysis/index.html#/ProductSaleProportion")
    time.sleep(5)
    if is_element_exist(driver, 'h3[class="item-content"]'):  #获取数据元素列表
        orgListEles=driver.find_elements_by_css_selector('h3[class="item-content"]')
    else:
        orgListEles=None
    print(orgListEles)
    time.sleep(2)
    saleProReport={}

    if orgListEles!=None:
        saleName=[]
        saleAmount=[]
        for ele in orgListEles:
            saleName.append(ele.find_element_by_css_selector('span').text)#获取产品名称
            saleAmount.append(ele.find_element_by_css_selector('div span>span').text)#获取产品对应的销售额字段
        saleProReport=dict(zip(saleName,saleAmount))#生成客户：销售额键值对
        print(saleProReport)
        Log("移动端客户销售占比分析报表有数据")
        return saleProReport#返回客户：销售额的键值对
    else:
        Log("移动端客户销售占比分析报表暂无数据")
        return None

#对比移动端和pc端产品销售占比分析报表的销售数据是否相等
def compareProSaleProportionReport(mobDriver,pcDriver,allOrgName):
    mobDriver.get("http://v-mobile-at/k3cloud/KDMobile/SaleAnalysis/index.html#/ProductSaleProportion")#进入客户销售占比分析报表
    time.sleep(4)
    select_MobFilterScheme(mobDriver,allOrgName)#设置移动端组织列表
    time.sleep(5)
    saleProReportVal=mobProSaleProportionReport(mobDriver)#调用移动端访问产品销售占比分析报表
    time.sleep(2)
    mobDriver.find_element_by_css_selector(".head-org").click()# 点击过滤方案下拉列表
    time.sleep(2)
    orgChkBoxEles=mobDriver.find_elements_by_css_selector('.mint-indexsection-item')#获取组织列表的元素list     
    time.sleep(2)
    orgSelectedList=[]
    for ele in orgChkBoxEles:
        if is_element_exist(ele,'i[class="m-checked checked"]'):#获取已选组织列表
            orgSelectedList.append(ele.text)
        else:
            orgSelectedList=None
    time.sleep(2)
    mobDriver.find_element_by_css_selector(".confirm").click()#点击确定
    time.sleep(2)
    box=pcDriver.find_element_by_css_selector(".ui-poplistedit-displayname")
    if box.get_attribute('title'):
        pcDriver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").clear()#清空当前搜索框text内容
    pcDriver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").send_keys('销售订单列表')#打开销售订单                                                                                                                                                                       单列表
    time.sleep(8)
    pcDriver.find_element_by_css_selector('li[class="k-state-focused"]').click() 
    time.sleep(6)
    select_PcFilterScheme(pcDriver,orgSelectedList)#按照移动端报表所选组织设置pc端组织
    pcList=int(pcDriver.find_element_by_css_selector("span[data-kdid='sp_2_pagerlist2']").text)#检查pcdaunt是否有数据????????????????????????????1第？页/共n页
    time.sleep(2)
    if saleProReportVal and orgSelectedList!=None and pcList!=0:

        ele=pcDriver.find_element_by_css_selector('div[data-role="virtualscrollable"]>div>table>tbody')#获取数据列表元素
        eleList=ele.find_elements_by_css_selector('tr[role="row"]')##获取数据列表的元素列表
        proNameList=[]
        pcSalAmountList=[]
        noRepeatDict={}
        for ele in eleList:#依次循环pc端销售订单列表每一条订单，找到客户名称、价税合计、业务员（销售员）名称
            proName=ele.find_element_by_css_selector('td:nth-child(10)>span[data-field="FMATERIALNAME"]').text#产品
            proNameList.append(proName)
            pcIncome=ele.find_element_by_css_selector('td:nth-child(14)>span[data-field="FALLAMOUNT_LC"]').text#物料价税合计本位币
            
            pcSalAmount=pcIncome[1:]#截取从第二位到结尾字符
            print("22222222222222222222222222222222222222222222222222222222")
            print(pcSalAmount)
            print(type(pcSalAmount))
            pcSalAmountList.append(pcSalAmount)
            obj=ele.find_element_by_css_selector('td:nth-child(8)>span[data-field="FSALERID_FNAME"]').text#业务员
            print(",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,")
            print(obj)
            if obj==linkObject:           #只有当销售员的名称等于当前用户的联系对象时，数据才是我们需要的，才加入到字典中
                if noRepeatDict.__contains__(proName): 
                    temp=float(noRepeatDict[proName])
                    temp+=float(pcSalAmount)
                    noRepeatDict[proName]=temp
                    print("kkkkkkkkkkkkkkkkkkk")
                    print(type(noRepeatDict[proName]))
                else:
                    noRepeatDict[proName]=pcSalAmount
                    print("3333333333333333333333333333333333333333333333333")
                    print(type(noRepeatDict[proName]))


        noRepeatName=list(set(proNameList))#不重复的客户名称
        print("////////////////////////////////////////////////////////////////")
        print(noRepeatDict)
        print("11111111111111111111111111111111111111111111111111111")
        if noRepeatDict:#当pc端客户：销售额字典不为空时，才进行移动端、pc端数据的比较
            for i in noRepeatName:#依次检查不重复的客户名称，检查其对应金额是否相等
                salAmount=saleProReportVal.get(i)#i产品对应的收入金额
                pcSalAmount=noRepeatDict.get(i)#i产品对应的收入金额
                print("qqqqqqqqqqqqqqqqqqqqq")
                print(type(pcSalAmount))
                if salAmount!= None and pcSalAmountList!= '':
                    print(type(salAmount))
                    print(type(pcSalAmount))
                    if isNum(salAmount) and isNum(pcSalAmount):
                        print(float(salAmount))
                        print(float(pcSalAmount))
                        if float(salAmount)==float(pcSalAmount):#两个值相等时，pass
                            Log(i+":产品销售占比分析报表的销售数据：移动端销售金额与pc端销售金额相等")
                        else:
                            Log(i+":产品销售占比分析报表的销售数据：移动端销售金额与pc端销售金不相等")
                    else:
                        Log(i+":产品销售占比分析报表的销售数据：有元素不为数字，请检查数值") 
                elif salAmount==None and pcSalAmountList=='':
                    Log(i+"产品销售占比分析报表的销售数据：移动端、pc端均无数据")  
    elif pcList==0 and saleProReportVal==False:
       Log("产品销售占比分析报表的销售数据：pc端暂无数据，金额为0,金额相等")
    elif pcList==None:
        Log("产品销售占比分析报表的销售数据：有不存在的元素")
    elif pcList==0 and saleProReportVal!=False:
        Log("产品销售占比分析报表的销售数据：pc端数据为0，移动端有数据")
    elif pcList!=0 and saleProReportVal==False:
        Log("产品销售占比分析报表的销售数据：移动端数据为0，pc端有数据")
    pcDriver.find_element_by_css_selector('span[class=" k-i-close mainTabCloseButton"]').click()


    #一级用例启动
def saleRepfirstLeverTest(mobDriver,pcDriver,allOrgName):
    openSaleReport(mobDriver)
    #login_pc(pcDriver,USERNAME,PASSWORD)
    
    try:
        compareCustSaleProportionReport(mobDriver,pcDriver,allOrgName)
    finally:
        print("执行完毕")
        #mobDriver.close()
        #pcDriver.close()
    try:
        compareProSaleProportionReport(mobDriver,pcDriver,allOrgName)
    finally:
        print("执行完毕")
        #mobDriver.close()
        #pcDriver.close()
    try:
        compareSaleRecRankingReport(mobDriver,pcDriver,allOrgName)
    finally:
        print("执行完毕")
        #mobDriver.close()
        #pcDriver.close()














