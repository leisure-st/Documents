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
#from selenium import webdriver

SALAMOUNT_XPATH = '//*[@id="app"]/article/header/h2/span'#销售分析销售金额元素路径
#进入销售分析
def openSaleAnalysis(driver):
    driver.get("http://v-mobile-at/k3cloud/mobile/k3cloud.html?entryrole=XT&formId=KD_Sal_MobileBusinessAnalysis&formType=mobileform&appid=10703")
    Log("进入销售分析")
    time.sleep(10)

def get_salAmount(driver):
    if is_element_exist(driver, ".amount"):
        #salAmount = driver.find_element_by_xpath(SALAMOUNT_XPATH).text  #销售额
        salAmount=driver.find_element_by_css_selector(".amount").text
        return salAmount
    else:
        Log("移动端销售分析首页销售金额不存在")
        return None

#对比移动端和pcdaunt销售分析首页销售金额是否相等
def compareSaleAmount(mobdriver,pcDriver):
    saleAmount=get_salAmount(mobdriver)
    if saleAmount!=None:
        Log("获取到移动端首页销售金额为："+saleAmount)
        pcSaleAmount=get_pcsalAmount(pcDriver)
        if pcSaleAmount != None:
            if isNum(saleAmount) and isNum(pcSaleAmount):
                if float(saleAmount)==float(pcSaleAmount):#两个值相等时，pass，有等于0暂无数据以及不等于0数据大于0这两种情况
                    Log("移动端销售金额与pc端销售金额相等")
                else:
                    Log("移动端销售金额与pc端销售金额不相等")
            else:
                Log("移动端销售金额与pc端销售金额有元素不为数字，请检查数值")
    else:
         Log("移动端销售金额与pc端销售金额有不存在的元素")

#对比移动端、pc端收款金额是否相等
def compareCollectAmount(mobDriver,pcDriver):
    #获取移动端销售收款金额
    if is_element_exist(mobDriver, 'header[class="home-banner m-banner"]>p>span'):
        #获取移动端销售收款金额
        text=mobDriver.find_element_by_css_selector('header[class="home-banner m-banner"]>p>span').text
        mobCollectAmount=text[7:len(text)-1]#提取移动端收款金额
        #print(mobCollectAmount)
        Log("获取到移动端"+text)
        mobDriver.find_element_by_css_selector(".head-org").click()# 点击过滤方案下拉列表
        time.sleep(5)
        orgChkBoxEles=mobDriver.find_elements_by_css_selector('.mint-indexsection-item')#获取组织列表的元素list     
        time.sleep(2)
        orgSelectedList=[]
        for ele in orgChkBoxEles:
            if is_element_exist(ele,'i[class="m-checked checked"]'):
                orgSelectedList.append(ele.text)
            else:
                orgSelectedList=None
        time.sleep(2)
        mobDriver.find_element_by_css_selector(".confirm").click()#点击确定
        #打开销售收款单
        box=pcDriver.find_element_by_css_selector(".ui-poplistedit-displayname")
        if box.get_attribute('title'):
            pcDriver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").clear()#清空当前搜索框text内容
        pcDriver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").send_keys("收款单列表")
        time.sleep(8)
        #pcDriver.find_element_by_xpath("/html/body/div[3]/div/div/div/li/span[3]").click()
        pcDriver.find_element_by_css_selector('li[class="k-state-focused"]').click()
        time.sleep(8)
        select_PcFilterScheme(pcDriver,orgSelectedList)#按照移动端所选组织给pc端过滤方案设置组织
        time.sleep(4)
        pcList=int(pcDriver.find_element_by_css_selector("span[data-kdid='sp_2_pagerlist2']").text)#检查pc端是否有数据
        time.sleep(2)
        if pcList!=0 and mobCollectAmount!=0:
            collectList=pcDriver.find_elements_by_css_selector('span[data-field="FREALRECAMOUNT_H"]')#获取实收金额本位币的元素列表
            collectAmountList=[]
            collectAmount=0
            str1=''
            for i in range(0,len(collectList)):
                collect=collectList[i].text#金额文本
                #print(type(collect))
                #print(collect)
                if '$'in collect:#判断是否有币别符号
                    str1='$'
                elif '¥' in collect:
                    #print("/////////////////////////")
                    str1='¥'
                collectAmountList.append(collectList[i].text.split(str1)[1])#去掉币别字段
                collectAmount+=float(collectAmountList[i])#加总每一行订单的实收金额
                #print("++++++++++++++++++++++++++++++++++++++++++")
            #print(collectAmount)
            if float(mobCollectAmount)==float(collectAmount):#判断金额是否相等 shujuleixing????????????????????????????????????
                Log("移动端与pc端首页收款金额相等")
            else :
                Log("移动端与pc端首页收款金额不相等")
        elif pcList==0 and float(mobCollectAmount)==0:
            Log("移动端与pc端首页收款：pc端暂无数据，移动端金额为0,金额相等")
        else:
            Log("数据有误")
    else:
        Log("移动端收款金额元素定位不到")
    pcDriver.find_element_by_css_selector('span[class=" k-i-close mainTabCloseButton"]').click()

def select_MobFilterScheme(driver,orgName):
    print(orgName)
    time.sleep(3)
    driver.find_element_by_css_selector(".head-org").click()# 点击过滤方案下拉列表
    time.sleep(5)
    orgSelectedList=[]                        #find_element_by_xpath("//div[@id='C']/../..").text       .text.replace(' ','').split(',') 
    # orgSelectedEles=driver.find_elements_by_xpath("//p[class='m-checked checked']/..")#driver.execute_script('return $(".kd-grid-sumfooterdiv,div[data-field=\'FALLAMOUNT_LC\']").text()')
    orgChkBoxEles=driver.find_elements_by_css_selector('.mint-indexsection-item')#获取组织列表的元素list      driver.execute_script('return $(".kd-grid-sumfooterdiv,div[data-field=\'FALLAMOUNT_LC\']").text()')
    print(orgChkBoxEles)
    # if (driver.find_element_by_css_selector("#app > article > div > ul >li:nth-child(1) > ul > p > i[class='m-checked checked']"))!='':
    #     orgSelectedList.append(orgChkBoxEles[1].text)
    for ele in orgChkBoxEles:
        if is_element_exist(ele,'i[class="m-checked checked"]'):
            orgSelectedList.append(ele.text)
    MobChangeOrg(orgChkBoxEles, orgSelectedList, orgName)
    #Log("设置移动端的组织如下："+orgName)
    time.sleep(6)
    driver.find_element_by_css_selector(".confirm").click()#点击确定
    
    #orgSelectedBox=driver.find_element_by_css_selector(".head-org")# 获取已选组织下拉框对象

    #orgSelectedText = orgSelectedBox.text#.encode('gbk')#.replace(' ','').split(',')
    # #n=filter(str.isdigit, orgSelectedText)
    # n=re.findall(r"\d+\.?\d*", orgSelectedText)#\d+匹配1次或者多次数字，注意这里不要写成*，因为即便是小数，小数点之前也得有一个数字；\.?这个是匹配小数点的，可能有，也可能没有；\d*这个是匹配小数点之后的数字的，所以是0个或者多个
    # print(n[0])
    # print(n)
    #print(orgSelectedText)
    #for i in range(1,n):
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
    #print('filter:'+driver.find_element_by_css_selector('span[id$="BILLMENU_TOOLBAR-tbFilter"]').text)
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

def get_pcsalAmount(driver):
    time.sleep(2)
    #wait = WebDriverWait(driver, 20) #实例化一个等待对象 wait              3hangzhushi?????????
    #searchBox = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[@id=\"FSEARCH\"]/span/span/span[2]")))
    #searchBox[0].click()
    # driver.implicitly_wait(2)
    # searchBox[0].send_keys('销售订单列表')       ui-poplistedit-displayname
    #driver.implicitly_wait(5)
    #driver.find_element_by_xpath("//input[@style='width: 120px; padding: 0px; font-size: 12px; height: 24px; margin-left: 30px; border-radius: 2px; opacity: 1; background: rgb(255, 255, 255);']").send_keys('销售订单列表')
    box=driver.find_element_by_css_selector(".ui-poplistedit-displayname")
    if box.get_attribute('title'):
        driver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").clear()#清空当前搜索框text内容
    driver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").send_keys('销售订单列表')
    time.sleep(8)
    driver.find_element_by_css_selector('li[class="k-state-focused"]').click()
    #pcList=driver.find_element_by_css_selector(".ui-poplistedit-displayname").text
    #pcList=driver.find_element_by_xpath('//*[@id="9d69f105-1c89-4e3d-aa2f-8d1377b6327c-FLIST-pager"]/ul/li[8]/span[1]/span/span/span/span[2]').text
    time.sleep(6)
    pcList=int(driver.find_element_by_css_selector("span[data-kdid='sp_2_pagerlist2']").text)#定位有多少行数据，为0则数据为空
    time.sleep(5)
    if pcList == 0:
        return 0
    else:
        pcSalAmount = driver.execute_script('return $(".kd-grid-sumfooterdiv,div[data-field=\'FALLAMOUNT_LC\']").text()')#这里通过js的方式获取元素还需要多加练习，当有多个数字在表尾时如何定位待解决
        if pcSalAmount == "":
            Log("pcSalAmount不存在")
            return None
        else:
            return pcSalAmount
    driver.find_element_by_css_selector('span[class=" k-i-close mainTabCloseButton"]').click()
    # return pcSalAmount    #pcsalAmount = driver.find_element_by_css_selector(".kd-grid-sumfooterdiv,div[data-field='FALLAMOUNT_LC']").text  #销售订单价税合计数值

#销售组织收入分析报表销售金额
def mobSalOrgReport_sale(driver):
    time.sleep(3)
    #driver.find_element_by_css_selector(".hairlines-bottom").click()#点击进入销售组织分析报表
    driver.get("http://v-mobile-at/k3cloud/KDMobile/BusinessAnalysis/index.html#/SaleNewsOrgIncome")
    time.sleep(4)
    driver.find_element_by_css_selector("#saleAmount").click()  #点击销售金额
    time.sleep(4)
    if is_element_exist(driver, 'div[class="item-content"]'):
        orgListEles=driver.find_elements_by_css_selector('div[class="item-content"]')#销售组织及金额
    else:
        orgListEles=None
    print(orgListEles)
    time.sleep(2)
    orgList=[]
    salAmount=[]
    salOrgReportVal={}
    if orgListEles!=None:
        for ele in orgListEles:
            orgList.append(ele.find_element_by_css_selector("p").text)#销售组织
            salAmount.append(ele.find_element_by_css_selector("span>span").text)#销售金额
        salOrgReportVal=dict(zip(orgList,salAmount))#生成销售组织：金额的键值对
        Log("移动端销售组织分析报表销售金额有数据")
        return salOrgReportVal#返回销售组织以及对应的金额
    else:
        Log("移动端销售组织分析报表销售金额暂无数据")
        return False

#对比移动端和pc端销售组织分析报表的销售金额数据是否相等
def compareSalOrgReport_sale(mobDriver,pcDriver,allOrgName):
    mobDriver.get("http://v-mobile-at/k3cloud/KDMobile/BusinessAnalysis/index.html#/SaleNewsOrgIncome")
    time.sleep(4)
    select_MobFilterScheme(mobDriver,allOrgName)#设置移动端组织列表
    time.sleep(5)
    salOrgReportVal=mobSalOrgReport_sale(mobDriver)#调用移动端访问销售组织分析报表
    time.sleep(2)
    mobDriver.find_element_by_css_selector(".head-org").click()# 点击过滤方案下拉列表
    time.sleep(2)
    orgChkBoxEles=mobDriver.find_elements_by_css_selector('.mint-indexsection-item')#获取组织列表的元素list     
    time.sleep(2)
    orgSelectedList=[]
    for ele in orgChkBoxEles:
        if is_element_exist(ele,'i[class="m-checked checked"]'):
            orgSelectedList.append(ele.text)
        else:
            orgSelectedList=None
    time.sleep(2)
    mobDriver.find_element_by_css_selector(".confirm").click()#点击确定
    time.sleep(2)
    box=pcDriver.find_element_by_css_selector(".ui-poplistedit-displayname")
    if box.get_attribute('title'):
        pcDriver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").clear()#清空当前搜索框text内容
    pcDriver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").send_keys('销售订单列表')#打开销售订单
    time.sleep(8)
    pcDriver.find_element_by_css_selector('li[class="k-state-focused"]').click()
    time.sleep(10)
    select_PcFilterScheme(pcDriver,orgSelectedList)#按照移动端报表所选组织设置pc端组织    kanwenti?????????
    pcList=int(pcDriver.find_element_by_css_selector("span[data-kdid='sp_2_pagerlist2']").text)#检查pcdaunt是否有数据????????????????????????????1第？页/共n页
    #Log("pc端共有"+pcList+"页数据")
    time.sleep(2)
    if salOrgReportVal and orgSelectedList!=None and pcList!=0:
        #orgList=list(salOrgReportVal.keys())
        #tempList=[]
        #salAmount=salOrgReportVal[1]
        for i in orgSelectedList:#依次让pc端等于移动端所选组织，检查金额是否相等
            tempList=[]
            tempList.append(i)
            select_PcFilterScheme(pcDriver,tempList)#依次设置pcdaunt组织为移动端的组织之一，
            time.sleep(5)
            if is_element_exist(pcDriver,'span[data-field="FALLAMOUNT_LC"]'):
                pcSalAmount = pcDriver.execute_script('return $(".kd-grid-sumfooterdiv,div[data-field=\'FALLAMOUNT_LC\']").text()')#依次获取每个组织在pc端的金额
            else:
                pcSalAmount=None
            salAmount=salOrgReportVal.get(i)
            if salAmount!= None and pcSalAmount != None:
                if isNum(salAmount) and isNum(pcSalAmount):
                    if float(salAmount)==float(pcSalAmount):#两个值相等时，pass
                        Log(tempList[0]+"销售组织分析报表销售金额：移动端销售金额与pc端销售金额相等")
                    else:
                        Log(tempList[0]+"销售组织分析报表销售金额：移动端销售金额与pc端销售金不相等")
                else:
                    Log(tempList[0]+"销售组织分析报表销售金额：有元素不为数字，请检查数值") 
            elif salAmount==None and pcSalAmount==None:
                Log(tempList[0]+"销售组织分析报表销售金额：移动端、pc端均无数据")   
    elif pcList==0 and salOrgReportVal==False:
       Log("销售组织分析报表销售金额：pc端暂无数据，金额为0,金额相等")
    elif pcList==None:
        Log("销售组织分析报表销售金额：有不存在的元素")
    elif pcList==0 and salOrgReportVal!=False:
        Log("销售组织分析报表销售金额：pc端数据为0，移动端有数据")
    elif pcList!=0 and salOrgReportVal==False:
        Log("销售组织分析报表销售金额：移动端数据为0，pc端有数据")
    pcDriver.find_element_by_css_selector('span[class=" k-i-close mainTabCloseButton"]').click()

#销售组织收入分析报表收款金额
def mobSalOrgReport_collect(driver):
    time.sleep(3)
    #driver.find_element_by_css_selector(".hairlines-bottom").click()#点击进入销售组织分析报表
    driver.get("http://v-mobile-at/k3cloud/KDMobile/BusinessAnalysis/index.html#/SaleNewsOrgIncome")
    time.sleep(4)
    driver.find_element_by_css_selector("#receiveAmount").click()  #点击收款金额
    time.sleep(4)
    if is_element_exist(driver, 'div[class="item-content"]'):
        orgListEles=driver.find_elements_by_css_selector('div[class="item-content"]')#销售组织及金额
    else:
        orgListEles=None
    print(orgListEles)
    time.sleep(2)
    orgList=[]
    salAmount=[]
    salOrgReportVal={}
    if orgListEles!=None:
        for ele in orgListEles:
            orgList.append(ele.find_element_by_css_selector("p").text)#销售组织
            salAmount.append(ele.find_element_by_css_selector("span>span").text)#收款金额
        salOrgReportVal=dict(zip(orgList,salAmount))#生成销售组织：金额的键值对
        Log("移动端销售组织分析报表收款金额有数据")
        return salOrgReportVal#返回销售组织以及对应的金额
    else:
        Log("移动端销售组织分析报表收款金额暂无数据")
        return False

#对比移动端和pc端销售部门分析报表的收款金额数据是否相等
def compareSalOrgReport_collect(mobDriver,pcDriver,allOrgName):
    mobDriver.get("http://v-mobile-at/k3cloud/KDMobile/BusinessAnalysis/index.html#/SaleNewsOrgIncome")
    time.sleep(4)
    select_MobFilterScheme(mobDriver,allOrgName)#设置移动端组织列表
    time.sleep(5)
    salOrgReportVal=mobSalOrgReport_collect(mobDriver)#调用移动端访问销售组织分析报表
    time.sleep(2)
    mobDriver.find_element_by_css_selector(".head-org").click()# 点击过滤方案下拉列表
    time.sleep(2)
    orgChkBoxEles=mobDriver.find_elements_by_css_selector('.mint-indexsection-item')#获取组织列表的元素list     
    time.sleep(2)
    orgSelectedList=[]
    for ele in orgChkBoxEles:
        if is_element_exist(ele,'i[class="m-checked checked"]'):
            orgSelectedList.append(ele.text)
        else:
            orgSelectedList=None
    time.sleep(2)
    mobDriver.find_element_by_css_selector(".confirm").click()#点击确定
    time.sleep(2)
    box=pcDriver.find_element_by_css_selector(".ui-poplistedit-displayname")
    if box.get_attribute('title'):
        pcDriver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").clear()#清空当前搜索框text内容
    pcDriver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").send_keys('收款单列表')#打开收款单
    time.sleep(8)
    pcDriver.find_element_by_css_selector('li[class="k-state-focused"]').click()
    time.sleep(8)
    select_PcFilterScheme(pcDriver,orgSelectedList)#按照移动端报表所选组织设置pc端组织
    pcList=int(pcDriver.find_element_by_css_selector("span[data-kdid='sp_2_pagerlist2']").text)#检查pcdaunt是否有数据????????????????????????????1第？页/共n页
    #Log("pc端共有"+pcList+"页数据")
    time.sleep(2)
    if salOrgReportVal and orgSelectedList!=None and pcList!=0:
        for i in orgSelectedList:
            tempList=[]
            tempList.append(i)
            select_PcFilterScheme(pcDriver,tempList)#依次设置pcdaunt组织为移动端的组织之一，
            time.sleep(5)
            #依次获取每个组织在pc端的金额
            #collectAmount=0
            if is_element_exist(pcDriver,'span[data-field="FREALRECAMOUNT_H"]'):
                collectList=pcDriver.find_elements_by_css_selector('span[data-field="FREALRECAMOUNT_H"]')#获取实收金额本位币的元素列表
                collectAmountList=[]
                collectAmount=0
                str1=''
                for a in range(0,len(collectList)):
                    collect=collectList[a].text#金额文本
                    #print(type(collect))
                    #print(collect)
                    if '$'in collect:#判断是否有币别符号
                        str1='$'
                    elif '¥' in collect:
                        #print("/////////////////////////")
                        str1='¥'
                    collectAmountList.append(collectList[a].text.split(str1)[1])#去掉币别字段
                    collectAmount+=float(collectAmountList[a])#加总每一行订单的实收金额
            else :
                collectAmount=None
            salAmount=salOrgReportVal.get(i)
            if salAmount!= None and collectAmount != None:#collectAmount为none时即该组织下，pc端无数据
                if isNum(salAmount) and isNum(collectAmount):
                    if float(salAmount)==float(collectAmount):#两个值相等时，pass  检查当前组织下，移动端、pc端数据是否相等
                        Log(tempList[0]+"销售组织分析报表：移动端收款金额与pc端收款金额相等")
                    else:
                        Log(tempList[0]+"销售组织分析报表：移动端收款金额与pc端收款金额不相等")
                else:
                    Log(tempList[0]+"销售组织分析报表收款金额：有元素不为数字，请检查数值") 
            elif collectAmount==None and salAmount==None:
                Log(tempList[0]+"移动端、pc端均无数据！")
    elif pcList==0 and salOrgReportVal==False:#选取所有组织时，依然无数据
       Log("销售组织分析报表收款金额：pc端暂无数据，金额为0,金额相等")
    elif pcList==None:
        Log("销售组织分析报表收款金额：有不存在的元素")
    elif pcList==0 and salOrgReportVal!=False:
        Log("销售组织分析报表收款金额：pc端数据为0，移动端有数据")
    elif pcList!=0 and salOrgReportVal==False:
        Log("销售组织分析报表收款金额：移动端数据为0，pc端有数据")
    pcDriver.find_element_by_css_selector('span[class=" k-i-close mainTabCloseButton"]').click()



#销售部门分析报表
def mobSalDepReport_sale(driver):#这里先默认是销售公司所有部门
    time.sleep(2)
    #driver.find_element_by_xpath("//*[@id='app']/article/section[2]/ol[1]/li[1]").click()
    driver.get("http://v-mobile-at/k3cloud/KDMobile/BusinessAnalysis/index.html#/SaleNewsDeptIncome")#进入销售部门分析报表
    time.sleep(4)
    driver.find_element_by_css_selector('h3[class="table-head"]>label').click()  #点击销售金额
    time.sleep(4)
    if is_element_exist(driver, 'div[class="item-content"]'):
        orgListEles=driver.find_elements_by_css_selector('div[class="item-content"]')#销售部门及金额
    else:
        orgListEles=None
    print(orgListEles)
    time.sleep(2)
    orgList=[]
    salAmount=[]
    salDepReportVal={}
    if orgListEles!=None:
        for ele in orgListEles:
            orgList.append(ele.find_element_by_css_selector("p").text)#销售部门
            salAmount.append(ele.find_element_by_css_selector("span>span").text)#销售金额
        salDepReportVal=dict(zip(orgList,salAmount))#生成销售部门：金额的键值对
        Log("移动端销售部门分析报表销售金额有数据")
        return salDepReportVal#返回销售部门以及对应的金额
    else:
        Log("移动端销售部门分析报表销售金额暂无数据")
        return False

#对比移动端和pc端销售部门分析报表的销售金额数据是否相等
def compareSalDepReport_sale(mobDriver,pcDriver):
    mobDriver.get("http://v-mobile-at/k3cloud/KDMobile/BusinessAnalysis/index.html#/SaleNewsDeptIncome")#进入销售部门分析报表
    time.sleep(4)
    salDepReportVal=mobSalDepReport_sale(mobDriver)#调用移动端访问销售部门分析报表
    time.sleep(2)
    mobDriver.find_element_by_css_selector(".head-org").click()# 点击过滤方案下拉列表
    time.sleep(2)
    orgChkBoxEles=mobDriver.find_elements_by_css_selector('.mint-indexsection-item')#获取组织列表的元素list，这里应该只有一个
    time.sleep(2)
    orgSelectedList=[]
    for ele in orgChkBoxEles:
        if is_element_exist(ele,'i[class="m-checked checked"]'):#为什么找不到了？？？？？？？？？？？？？？？？
            orgSelectedList.append(ele.text)
        else:
            continue
    if len(orgSelectedList)==0:
        orgSelectedList=None
    print(len(orgSelectedList))
    Log("销售部门分析报表，组织选择列表已选中"+str(len(orgSelectedList))+"个组织")  #检查是否默认选中了一个 
    time.sleep(2)
    box=pcDriver.find_element_by_css_selector(".ui-poplistedit-displayname")
    if box.get_attribute('title'):
        pcDriver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").clear()#清空当前搜索框text内容
    pcDriver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").send_keys('销售订单列表')#打开销售订单
    time.sleep(8)
    pcDriver.find_element_by_css_selector('li[class="k-state-focused"]').click()
    time.sleep(8)
    select_PcFilterScheme(pcDriver,orgSelectedList)#按照移动端报表所选组织设置pc端组织
    pcList=int(pcDriver.find_element_by_css_selector("span[data-kdid='sp_2_pagerlist2']").text)#检查pcdaunt是否有数据????????????????????????????1第？页/共n页
    #Log("pc端共有"+pcList+"页数据")
    time.sleep(2)
    if salDepReportVal and orgSelectedList!=None and pcList!=0:
        for i in orgSelectedList:#依次让pc端等于移动端所选组织，检查金额是否相等
            tempList=[]
            tempList.append(i)
            select_PcFilterScheme(pcDriver,tempList)#依次设置pcdaunt组织为移动端的组织之一，
            time.sleep(5)
            if is_element_exist(pcDriver,'span[data-field="FALLAMOUNT_LC"]'):#价税合计字段是否存在，存在证明有数据行
                pcSalAmount = pcDriver.execute_script('return $(".kd-grid-sumfooterdiv,div[data-field=\'FALLAMOUNT_LC\']").text()')#依次获取每个组织在pc端的金额
            else:
                pcSalAmount=None
            salAmount=salDepReportVal.get(i)
            if salAmount!= None and pcSalAmount != None:
                if isNum(salAmount) and isNum(pcSalAmount):
                    if float(salAmount)==float(pcSalAmount):#两个值相等时，pass
                        Log(tempList[0]+"销售部门分析报表销售金额：移动端销售金额与pc端销售金额相等")
                    else:
                        Log(tempList[0]+"销售部门分析报表销售金额：移动端销售金额与pc端销售金不相等")
                else:
                    Log(tempList[0]+"销售部门分析报表销售金额：有元素不为数字，请检查数值") 
            elif salAmount==None and pcSalAmount==None:
                Log(tempList[0]+"销售部门分析报表销售金额：移动端、pc端均无数据")   
    elif pcList==0 and salDepReportVal==False:
       Log("销售部门分析报表销售金额：pc端暂无数据，金额为0,金额相等")
    elif pcList==None:
        Log("销售部门分析报表销售金额：有不存在的元素")
    elif pcList==0 and salDepReportVal!=False:
        Log("销售部门分析报表销售金额：pc端数据为0，移动端有数据")
    elif pcList!=0 and salDepReportVal==False:
        Log("销售部门分析报表销售金额：移动端数据为0，pc端有数据")
    pcDriver.find_element_by_css_selector('span[class=" k-i-close mainTabCloseButton"]').click()

#销售利润分析报表销售收入
def mobSaleProfitsReport_income(driver):
    time.sleep(2)
    driver.get("http://v-mobile-at/K3Cloud/KDMobile/BusinessAnalysis/index.html#/SaleProfitsAnalysis")
    time.sleep(5)
    if is_element_exist(driver, 'li[class="hairlines-bottom"]'):
        orgListEles=driver.find_elements_by_css_selector('li[class="hairlines-bottom"]')#销售数量、销售输入、销售成本
    else:
        orgListEles=None
    print(orgListEles)
    time.sleep(2)
    proList=[]
    incomeAmount=[]
    salProfitsReportVal={}
    if orgListEles!=None:
        for ele in orgListEles:
            proList.append(ele.find_element_by_css_selector('div[class="item-content"]>p').text)#销售收入   div#B div:nth-child(1)
            text=ele.find_element_by_css_selector('sub span:nth-child(2)').text
            incomeAmount.append(text[4:len(text)])#销售金额
        salProfitsReportVal=dict(zip(proList,incomeAmount))#生成产品名称：收入金额的键值对
        Log("移动端产品销售利润分析报表销售收入金额有数据")
        return salProfitsReportVal#返回销售部门以及对应的金额
    else:
        Log("移动端产品销售利润分析报表销售收入金额暂无数据")
        return False

#对比移动端和pc端产品销售利润分析报表的销售的收入数据是否相等
def compareSaleProfitsReport_income(mobDriver,pcDriver,allOrgName):
    mobDriver.get("http://v-mobile-at/K3Cloud/KDMobile/BusinessAnalysis/index.html#/SaleProfitsAnalysis")#进入产品销售利润分析报表
    time.sleep(4)
    select_MobFilterScheme(mobDriver,allOrgName)#设置移动端组织列表
    time.sleep(5)
    salProfitsReportVal=mobSaleProfitsReport_income(mobDriver)#调用移动端访问销售组织分析报表
    time.sleep(2)
    mobDriver.find_element_by_css_selector(".head-org").click()# 点击过滤方案下拉列表
    time.sleep(2)
    orgChkBoxEles=mobDriver.find_elements_by_css_selector('.mint-indexsection-item')#获取组织列表的元素list     
    time.sleep(2)
    orgSelectedList=[]
    for ele in orgChkBoxEles:
        if is_element_exist(ele,'i[class="m-checked checked"]'):
            orgSelectedList.append(ele.text)
        else:
            orgSelectedList=None
    time.sleep(2)
    mobDriver.find_element_by_css_selector(".confirm").click()#点击确定
    time.sleep(2)
    box=pcDriver.find_element_by_css_selector(".ui-poplistedit-displayname")
    if box.get_attribute('title'):
        pcDriver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").clear()#清空当前搜索框text内容
    pcDriver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").send_keys('应收单列表')#打开应收单列表
    time.sleep(8)
    pcDriver.find_element_by_css_selector('li[class="k-state-focused"]').click()
    time.sleep(8)
    select_PcFilterScheme(pcDriver,orgSelectedList)#按照移动端报表所选组织设置pc端组织
    pcList=int(pcDriver.find_element_by_css_selector("span[data-kdid='sp_2_pagerlist2']").text)#检查pcdaunt是否有数据????????????????????????????1第？页/共n页
    time.sleep(2)
    if salProfitsReportVal and orgSelectedList!=None and pcList!=0:
        proList=[]
        proEles=pcDriver.find_elements_by_css_selector('span[data-field="FMATERIALNAME"]')#物料元素列表
        for ele in proEles:
            proList.append(ele.text)
        pcSalAmountList=[]
        pcIncomeEles=pcDriver.find_elements_by_css_selector('span[data-field="FNOTAXAMOUNT"]')#物料金额元素列表
        for ele in pcIncomeEles:
            pcSalAmountList.append(ele.text)
        pcIncomeProVal=dict(zip(proList,pcSalAmountList))#生成pc端的物料：收入金额的键值对
        for i in proList:#依次让pc端等于移动端所选组织，检查金额是否相等
            salAmount=salProfitsReportVal.get(i)#i产品对应的收入金额
            pcSalAmount=pcIncomeProVal.get(i)#i产品对应的收入金额
            if salAmount!= None and pcSalAmountList != '':
                if isNum(salAmount) and isNum(pcSalAmount):
                    if float(salAmount)==float(pcSalAmount):#两个值相等时，pass
                        Log(i+":产品销售利润分析报表销售收入金额：移动端销售收入金额与pc端销售金额相等")
                    else:
                        Log(i+":产品销售利润分析报表销售收入金额：移动端销售收入金额与pc端销售金不相等")
                else:
                    Log(i+":产品销售利润分析报表销售收入金额：有元素不为数字，请检查数值") 
            elif salAmount==None and pcSalAmountList=='':
                Log(i+"产品销售利润分析报表销售收入金额：移动端、pc端均无数据")  
    elif pcList==0 and salProfitsReportVal==False:
       Log("产品销售利润分析报表销售收入金额：pc端暂无数据，金额为0,金额相等")
    elif pcList==None:
        Log("产品销售利润分析报表销售收入金额：有不存在的元素")
    elif pcList==0 and salProfitsReportVal!=False:
        Log("产品销售利润分析报表销售收入金额：pc端数据为0，移动端有数据")
    elif pcList!=0 and salProfitsReportVal==False:
        Log("产品销售利润分析报表销售收入金额：移动端数据为0，pc端有数据")
    pcDriver.find_element_by_css_selector('span[class=" k-i-close mainTabCloseButton"]').click()

#销售利润分析报表销售成本
def mobSaleProfitsReport_cost(driver):
    time.sleep(2)
    driver.get("http://v-mobile-at/K3Cloud/KDMobile/BusinessAnalysis/index.html#/SaleProfitsAnalysis")
    time.sleep(5)
    if is_element_exist(driver, 'li[class="hairlines-bottom"]'):
        orgListEles=driver.find_elements_by_css_selector('li[class="hairlines-bottom"]')#销售数量、销售输入、销售成本
    else:
        orgListEles=None
    print(orgListEles)
    time.sleep(2)
    proList=[]
    incomeAmount=[]
    salProfitsReportVal={}
    if orgListEles!=None:
        for ele in orgListEles:
            proList.append(ele.find_element_by_css_selector('div[class="item-content"]>p').text)#销售收入   div#B div:nth-child(1)
            text=ele.find_element_by_css_selector('sub span:nth-child(3)').text#获取销售成本字段
            incomeAmount.append(text[4:len(text)])#销售金额，也可以不写第二个参数，就是截取到结尾的意思
        salProfitsReportVal=dict(zip(proList,incomeAmount))#生成产品名称：收入金额的键值对
        Log("移动端产品销售利润分析报表销售成本金额有数据")
        return salProfitsReportVal#返回销售部门以及对应的金额
    else:
        Log("移动端产品销售利润分析报表销售成本金额暂无数据")
        return False

#对比移动端和pc端产品销售利润分析报表的销售成本数据是否相等
def compareSaleProfitsReport_cost(mobDriver,pcDriver,allOrgName):
    mobDriver.get("http://v-mobile-at/K3Cloud/KDMobile/BusinessAnalysis/index.html#/SaleProfitsAnalysis")#进入产品销售利润分析报表
    time.sleep(4)
    select_MobFilterScheme(mobDriver,allOrgName)#设置移动端组织列表
    time.sleep(5)
    salProfitsReportVal=mobSaleProfitsReport_cost(mobDriver)#调用移动端访问销售组织分析报表
    time.sleep(2)
    mobDriver.find_element_by_css_selector(".head-org").click()# 点击过滤方案下拉列表
    time.sleep(2)
    orgChkBoxEles=mobDriver.find_elements_by_css_selector('.mint-indexsection-item')#获取组织列表的元素list     
    time.sleep(2)
    orgSelectedList=[]
    for ele in orgChkBoxEles:
        if is_element_exist(ele,'i[class="m-checked checked"]'):
            orgSelectedList.append(ele.text)
        else:
            orgSelectedList=None
    time.sleep(2)
    mobDriver.find_element_by_css_selector(".confirm").click()#点击确定
    time.sleep(2)
    box=pcDriver.find_element_by_css_selector(".ui-poplistedit-displayname")
    if box.get_attribute('title'):
        pcDriver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").clear()#清空当前搜索框text内容
    pcDriver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").send_keys('销售出库单列表')#打开销售出库                                                                                                                                                                       单列表
    time.sleep(8)
    pcDriver.find_element_by_css_selector('li[class="k-state-focused"]').click() 
    time.sleep(8)
    select_PcFilterScheme(pcDriver,orgSelectedList)#按照移动端报表所选组织设置pc端组织
    pcList=int(pcDriver.find_element_by_css_selector("span[data-kdid='sp_2_pagerlist2']").text)#检查pcdaunt是否有数据????????????????????????????1第？页/共n页
    time.sleep(2)
    if salProfitsReportVal and orgSelectedList!=None and pcList!=0:
        proList=[]
        proEles=pcDriver.find_elements_by_css_selector('span[data-field="FMATERIALNAME"]')#物料元素列表
        for ele in proEles:
            proList.append(ele.text)
        pcSalAmountList=[]
        pcIncomeEles=pcDriver.find_elements_by_css_selector('span[data-field="FCOSTAMOUNT_LC"]')#物料金额元素列表     多了个币别符号？？？？？？？？
        for ele in pcIncomeEles:
            pcSalAmountList.append((ele.text)[1:])#截取从第二位到结尾字符
        pcCostProVal=dict(zip(proList,pcSalAmountList))#生成pc端的物料：收入金额的键值对
        for i in proList:#依次让pc端等于移动端所选组织，检查金额是否相等
            salAmount=salProfitsReportVal.get(i)#i产品对应的收入金额
            pcSalAmount=pcCostProVal.get(i)#i产品对应的收入金额
            if salAmount!= None and pcSalAmountList != '':
                if isNum(salAmount) and isNum(pcSalAmount):
                    if float(salAmount)==float(pcSalAmount):#两个值相等时，pass
                        Log(i+":产品销售利润分析报表销售成本金额：移动端销售收入金额与pc端销售金额相等")
                    else:
                        Log(i+":产品销售利润分析报表销售成本金额：移动端销售收入金额与pc端销售金不相等")
                else:
                    Log(i+":产品销售利润分析报表销售成本金额：有元素不为数字，请检查数值") 
            elif salAmount==None and pcSalAmountList=='':
                Log(i+"产品销售利润分析报表销售成本金额：移动端、pc端均无数据")  
    elif pcList==0 and salProfitsReportVal==False:
       Log("产品销售利润分析报表销售成本金额：pc端暂无数据，金额为0,金额相等")
    elif pcList==None:
        Log("产品销售利润分析报表销售成本金额：有不存在的元素")
    elif pcList==0 and salProfitsReportVal!=False:
        Log("产品销售利润分析报表销售成本金额：pc端数据为0，移动端有数据")
    elif pcList!=0 and salProfitsReportVal==False:
        Log("产品销售利润分析报表销售成本金额：移动端数据为0，pc端有数据")
    pcDriver.find_element_by_css_selector('span[class=" k-i-close mainTabCloseButton"]').click()

#销售占比分析报表
def mobSaleProportionReport(driver):
    time.sleep(2)
    driver.get("http://v-mobile-at/K3Cloud/KDMobile/BusinessAnalysis/index.html#/SaleProportionAnalysis")#进入销售占比分析报表
    time.sleep(5)
    if is_element_exist(driver, 'div[class="item-content"]'):
        orgListEles=driver.find_elements_by_css_selector('div[class="item-content"]')#物料名称、数量、价税合计本位币等
    else:
        orgListEles=None
    print(orgListEles)
    time.sleep(2)
    proList=[]
    salAmount=[]
    salProfitsReportVal={}
    if orgListEles!=None:
        for ele in orgListEles:
            proList.append(ele.find_element_by_css_selector('h3').text)#产品名称   div#B div:nth-child(1)
            text=ele.find_element_by_css_selector('p span:nth-child(2)>span').text#获取销售金额字段
            salAmount.append(text)#销售金额，也可以不写第二个参数，就是截取到结尾的意思
        salProfitsReportVal=dict(zip(proList,salAmount))#生成产品名称：收入金额的键值对
        Log("移动端产品销售占比分析报表销售金额有数据")
        return salProfitsReportVal#返回销售部门以及对应的金额
    else:
        Log("移动端产品销售占比分析报表销售金额暂无数据")
        return False 
# 当一种物料有多条订单对应时，需要加总金额，这里还没有处理？？？？？？？？？？？？

#对比移动端和pc端产品销售占比分析报表的销售数据是否相等
def compareSaleProportionReport(mobDriver,pcDriver,allOrgName):
    mobDriver.get("http://v-mobile-at/K3Cloud/KDMobile/BusinessAnalysis/index.html#/SaleProportionAnalysis")#进入产品销售利润分析报表
    time.sleep(4)
    select_MobFilterScheme(mobDriver,allOrgName)#设置移动端组织列表
    time.sleep(5)
    salProReportVal=mobSaleProportionReport(mobDriver)#调用移动端访问销售组织分析报表
    time.sleep(2)
    mobDriver.find_element_by_css_selector(".head-org").click()# 点击过滤方案下拉列表
    time.sleep(2)
    orgChkBoxEles=mobDriver.find_elements_by_css_selector('.mint-indexsection-item')#获取组织列表的元素list     
    time.sleep(2)
    orgSelectedList=[]
    for ele in orgChkBoxEles:
        if is_element_exist(ele,'i[class="m-checked checked"]'):
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
    time.sleep(8)
    select_PcFilterScheme(pcDriver,orgSelectedList)#按照移动端报表所选组织设置pc端组织
    pcList=int(pcDriver.find_element_by_css_selector("span[data-kdid='sp_2_pagerlist2']").text)#检查pcdaunt是否有数据????????????????????????????1第？页/共n页
    time.sleep(2)
    if salProReportVal and orgSelectedList!=None and pcList!=0:
        proList=[]
        proEles=pcDriver.find_elements_by_css_selector('span[data-field="FMATERIALNAME"]')#物料元素列表
        for ele in proEles:
            proList.append(ele.text)
        pcSalAmountList=[]
        pcIncomeEles=pcDriver.find_elements_by_css_selector('span[data-field="FALLAMOUNT_LC"]')#物料价税合计本位币元素列表     多了个币别符号？？？？？？？？
        for ele in pcIncomeEles:
            pcSalAmountList.append((ele.text)[1:])#截取从第二位到结尾字符
        pcProVal=dict(zip(proList,pcSalAmountList))#生成pc端的物料：收入金额的键值对
        for i in proList:#依次让pc端等于移动端所选组织，检查金额是否相等
            salAmount=salProReportVal.get(i)#i产品对应的收入金额
            pcSalAmount=pcProVal.get(i)#i产品对应的收入金额
            if salAmount!= None and pcSalAmountList != '':
                if isNum(salAmount) and isNum(pcSalAmount):
                    print(float(salAmount))
                    print(float(pcSalAmount))
                    if float(salAmount)==float(pcSalAmount):#两个值相等时，pass
                        Log(i+":产品销售占比分析报表销售金额：移动端销售收入金额与pc端销售金额相等")
                    else:
                        Log(i+":产品销售占比分析报表销售金额：移动端销售收入金额与pc端销售金不相等")
                else:
                    Log(i+":产品销售占比分析报表销售金额：有元素不为数字，请检查数值") 
            elif salAmount==None and pcSalAmountList=='':
                Log(i+"产品销售占比分析报表销售金额：移动端、pc端均无数据")  
    elif pcList==0 and salProReportVal==False:
       Log("产品销售占比分析报表销售金额：pc端暂无数据，金额为0,金额相等")
    elif pcList==None:
        Log("产品销售占比分析报表销售金额：有不存在的元素")
    elif pcList==0 and salProReportVal!=False:
        Log("产品销售占比分析报表销售金额：pc端数据为0，移动端有数据")
    elif pcList!=0 and salProReportVal==False:
        Log("产品销售占比分析报表销售金额：移动端数据为0，pc端有数据")
    pcDriver.find_element_by_css_selector('span[class=" k-i-close mainTabCloseButton"]').click()

#移动端新增客户分析报表
def mobNewCostReport(driver):
    time.sleep(2)
    driver.get("http://v-mobile-at/K3Cloud/KDMobile/BusinessAnalysis/index.html#/SaleNewsNewCustAnalysis")#进入新增客户分析报表
    time.sleep(5)
    if is_element_exist(driver, 'div[class="bottom"]'):  #新增客户分析报表下方的新增客户/总客户销售额区域
        orgListEles=driver.find_elements_by_css_selector('div[class="bottom"]')
    else:
        orgListEles=None
    print(orgListEles)
    time.sleep(2)
    newCost=0
    allCost=0
    newCostReportVal=[]
    if orgListEles!=None:
        for ele in orgListEles:
            newCost=float(ele.find_element_by_css_selector('div span:nth-child(3)>span').text)#新增客户销售额
            allCost=float(ele.find_element_by_css_selector('div:nth-child(2)>span:nth-child(3)>span').text)#获取所有客户销售额字段
        newCostReportVal.append(newCost)
        newCostReportVal.append(allCost)#生成新增客户销售额,所有客户销售额的列表[新增客户销售额，所有客户销售额]
        print(newCostReportVal)
        Log("移动端新增客户分析报表销售金额有数据")
        return newCostReportVal#返回新增客户销售额：所有客户销售额的键值对
    else:
        Log("移动端新增客户分析报表销售金额暂无数据")
        return None

#对比移动端、pc端新增客户/所有客户销售额数值是否相等
def compareNewCostReport(mobDriver,pcDriver,allOrgName):
    mobDriver.get("http://v-mobile-at/K3Cloud/KDMobile/BusinessAnalysis/index.html#/SaleNewsNewCustAnalysis")#进入新增客户分析报表
    time.sleep(4)
    select_MobFilterScheme(mobDriver,allOrgName)#设置移动端组织列表
    time.sleep(5)
    newCostReportVal=mobNewCostReport(mobDriver)#调用移动端访问销售组织分析报表
    time.sleep(2)
    mobDriver.find_element_by_css_selector(".head-org").click()# 点击过滤方案下拉列表
    time.sleep(2)
    orgChkBoxEles=mobDriver.find_elements_by_css_selector('.mint-indexsection-item')#获取组织列表的元素list     
    time.sleep(2)
    orgSelectedList=[]
    for ele in orgChkBoxEles:
        if is_element_exist(ele,'i[class="m-checked checked"]'):
            orgSelectedList.append(ele.text)
        else:
            orgSelectedList=None
    time.sleep(2)
    mobDriver.find_element_by_css_selector(".confirm").click()#点击确定
    time.sleep(2)
    box=pcDriver.find_element_by_css_selector(".ui-poplistedit-displayname")
    if box.get_attribute('title'):
        pcDriver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").clear()#清空当前搜索框text内容
    pcDriver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").send_keys('客户列表')#打开客户列表，获取新增客户名称                                                                                                                                                                       单列表
    time.sleep(6)
    pcDriver.find_element_by_css_selector('li[class="k-state-focused"]').click() 
    time.sleep(9)
    select_PcFilterScheme(pcDriver,orgSelectedList)#按照移动端报表所选组织设置pc端组织
    newCostName=[]
    time.sleep(3)
    if is_element_exist(pcDriver,'span[data-field="FNAME"]'):
        newCostEles=pcDriver.find_elements_by_css_selector('span[data-field="FNAME"]')
        for ele in newCostEles:
            newCostName.append(ele.text)
            newCostName=list(set(newCostName))#去重
    pcDriver.find_element_by_css_selector('span[class=" k-i-close mainTabCloseButton"]').click()
    time.sleep(3)
    pcDriver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").clear()#清空当前搜索框text内容

    pcDriver.find_element_by_css_selector("input[class='k-input kd-appplat-search']").send_keys('销售订单列表')#打开销售订单，获取新增客户与所有客户的销售额                                                                                                                                                                       单列表
    time.sleep(8)
    pcDriver.find_element_by_css_selector('li[class="k-state-focused"]').click() 
    time.sleep(8)
    select_PcFilterScheme(pcDriver,orgSelectedList)#按照移动端报表所选组织设置pc端组织
    pcList=int(pcDriver.find_element_by_css_selector("span[data-kdid='sp_2_pagerlist2']").text)#检查pcdaunt是否有数据????????????????????????????1第？页/共n页
    time.sleep(2)
    
    if orgSelectedList!=None and pcList!=0:#pc端有数据才进行pc端新增客户等的获取判断
        costName=[]
        costNameElses=pcDriver.find_elements_by_css_selector('span[data-field="FCUSTID_FNAME"]')
        for ele in costNameElses:
            costName.append(ele.text)
        #costName=list(set(costName))
        saleList=[]   #价税合计列表
        saleEles=pcDriver.find_elements_by_css_selector('span[data-field="FALLAMOUNT_LC"]')
        for ele in saleEles:
            saleList.append(ele.text)
        
        pcCostSaleList=[]
        for i in range(0,len(costName)):#逐个组装客户名：价税合计键值对再封装成列表的元素
            name=costName[i]
            sale=saleList[i]
            dict1={name:sale}
            pcCostSaleList.append(dict1)
        #pcCostZip=dict(zip(costName,sale))
        pcNewCost=0
        for a in range(0,len(pcCostSaleList)):       #可以判断多个新增客户的时候   遍历客户：价税合计键值对组成的列表
            cost=costName[a]#取出客户名称
            #if cost.__contains__(newCostName[0]):
            if cost in newCostName:
                #name=pcCostSaleList[a]
                temp=float((pcCostSaleList[a].get(cost))[1:])
                pcNewCost+=temp   #把所有新增客户的价税合计金额加总
            else:
                continue    

        pcAllCost=0
        if is_element_exist(pcDriver,'span[data-field="FALLAMOUNT_LC"]'):
            pcAllCost = pcDriver.execute_script('return $(".kd-grid-sumfooterdiv,div[data-field=\'FALLAMOUNT_LC\']").text()')#获取总销售额
        newCost=newCostReportVal[0]#新增客户销售金额值
        allCost=newCostReportVal[1]#所有客户销售金额值
        if pcAllCost!=0 and pcNewCost!=0 and newCostReportVal!=None:
            if isNum(pcNewCost) and isNum(newCost):
                if float(pcNewCost)==float(newCost):#两个值相等时，pass
                    Log("新增客户分析报表销售金额：移动端新增客户销售金额与pc端销售金额相等")
                else:
                    Log("新增客户分析报表销售金额：移动端新增客户销售金额与pc端销售金额不相等")
            else:
                Log("新增客户分析报表销售金额：新增客户销售金额有元素不为数字，请检查数值") 
            if isNum(pcAllCost) and isNum(allCost):
                if float(pcAllCost)==float(allCost):#两个值相等时，pass
                    Log("新增客户分析报表销售金额：移动端所有客户销售金额与pc端销售金额相等")
                else:
                    Log("新增客户分析报表销售金额：移动端所有客户销售金额与pc端销售金额不相等")
            else:
                Log("新增客户分析报表销售金额：所有客户有元素不为数字，请检查数值")
        elif newCostReportVal==None and pcAllCost!=0 and pcNewCost!=0:
            Log("新增客户分析报表销售金额：pc端有数据，请检查")
        elif newCostReportVal!=None and pcAllCost==0:
            Log("新增客户分析报表销售金额：pc端暂无数据，请检查")
    elif newCostReportVal==None and pcList==0:
        Log("新增客户分析报表销售金额：移动端、pc端新增客户均无数据")
    pcDriver.find_element_by_css_selector('span[class=" k-i-close mainTabCloseButton"]').click()
    
#移动端销售员业绩排名报表
def mobSaleRankingReport(driver):
    time.sleep(2)
    driver.get("http://v-mobile-at/K3Cloud/KDMobile/BusinessAnalysis/index.html#/SaleRanking")#进入销售员业绩排名报表
    time.sleep(5)
    if is_element_exist(driver, 'div[class="item-content"]'):  #获取数据元素列表
        orgListEles=driver.find_elements_by_css_selector('div[class="item-content"]')
    else:
        orgListEles=None
    print(orgListEles)
    time.sleep(2)
    saleRankingReportVal={}

    if orgListEles!=None:
        saleName=[]
        saleAmount=[]
        for ele in orgListEles:
            saleName.append(ele.find_element_by_css_selector('p').text)#获取销售员名称
            saleAmount.append(ele.find_element_by_css_selector('span>span').text)#获销售员对应的销售额字段
        saleRankingReportVal=dict(zip(saleName,saleAmount))#生成销售员：销售额键值对
        print(saleRankingReportVal)
        Log("移动端销售员业绩排名报表有数据")
        return saleRankingReportVal#返回销售员：销售额的键值对
    else:
        Log("移动端销售员业绩排名报表暂无数据")
        return None

#对比移动端和pc端销售员业绩排名报表的销售数据是否相等
def compareSaleRankingReport(mobDriver,pcDriver,allOrgName):
    mobDriver.get("http://v-mobile-at/K3Cloud/KDMobile/BusinessAnalysis/index.html#/SaleRanking")#进入销售员业绩排名报表
    time.sleep(4)
    select_MobFilterScheme(mobDriver,allOrgName)#设置移动端组织列表
    time.sleep(5)
    salProReportVal=mobSaleRankingReport(mobDriver)#调用移动端访问销售员业绩排名报表
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
    time.sleep(8)
    select_PcFilterScheme(pcDriver,orgSelectedList)#按照移动端报表所选组织设置pc端组织
    pcList=int(pcDriver.find_element_by_css_selector("span[data-kdid='sp_2_pagerlist2']").text)#检查pcdaunt是否有数据????????????????????????????1第？页/共n页
    time.sleep(2)
    if salProReportVal and orgSelectedList!=None and pcList!=0:
        saleNameList=[]
        nameEles=pcDriver.find_elements_by_css_selector('span[data-field="FSALERID_FNAME"]')#销售员元素列表
        for ele in nameEles:
            saleNameList.append(ele.text)
        noRepeatName=list(set(saleNameList))#不重复的销售员名称
        #noRepeatSale=[]
        pcSalAmountList=[]
        pcIncomeEles=pcDriver.find_elements_by_css_selector('span[data-field="FALLAMOUNT_LC"]')#物料价税合计本位币元素列表     多了个币别符号？？？？？？？？
        for ele in pcIncomeEles:
            pcSalAmountList.append((ele.text)[1:])#截取从第二位到结尾字符
        #pcSaleVal=dict(zip(saleNameList,pcSalAmountList))#生成pc端的物料：收入金额的键值对


        # for i in range(0,len(saleNameList)):#逐个组装客户名：价税合计键值对再封装成列表的元素
        #     name=saleNameList[i]
        #     sale=pcSalAmountList[i]
        #     dict1={name:sale}
        #     pcCostSaleList.append(dict1)
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


        #pcProVal=dict(zip(saleNameList,pcSalAmountList))#生成pc端的物料：收入金额的键值对
        for i in noRepeatName:#依次让pc端等于移动端所选组织，检查金额是否相等
            salAmount=salProReportVal.get(i)#i产品对应的收入金额
            pcSalAmount=noRepeatDict.get(i)#i产品对应的收入金额
            if salAmount!= None and pcSalAmountList != '':
                if isNum(salAmount) and isNum(pcSalAmount):
                    print(float(salAmount))
                    print(float(pcSalAmount))
                    if float(salAmount)==float(pcSalAmount):#两个值相等时，pass
                        Log(i+":销售员业绩排名报表的销售数据：移动端销售金额与pc端销售金额相等")
                    else:
                        Log(i+":销售员业绩排名报表的销售数据：移动端销售金额与pc端销售金不相等")
                else:
                    Log(i+":销售员业绩排名报表的销售数据：有元素不为数字，请检查数值") 
            elif salAmount==None and pcSalAmountList=='':
                Log(i+"销售员业绩排名报表的销售数据：移动端、pc端均无数据")  
    elif pcList==0 and salProReportVal==False:
       Log("销售员业绩排名报表的销售数据：pc端暂无数据，金额为0,金额相等")
    elif pcList==None:
        Log("销售员业绩排名报表的销售数据：有不存在的元素")
    elif pcList==0 and salProReportVal!=False:
        Log("销售员业绩排名报表的销售数据：pc端数据为0，移动端有数据")
    elif pcList!=0 and salProReportVal==False:
        Log("销售员业绩排名报表的销售数据：移动端数据为0，pc端有数据")
    pcDriver.find_element_by_css_selector('span[class=" k-i-close mainTabCloseButton"]').click()

#移动端客户销售动态报表
def mobCustSaleStateReport(driver):
    time.sleep(2)
    driver.get("http://v-mobile-at/K3Cloud/KDMobile/BusinessAnalysis/index.html#/SaleNewsCustSaleState")#客户销售动态报表
    time.sleep(5)
    driver.find_element_by_css_selector('span[id="totalSale"]').click()
    time.sleep(4)
    if is_element_exist(driver, 'div[class="item-content"]'):  #获取数据元素列表
        orgListEles=driver.find_elements_by_css_selector('div[class="item-content"]')
    else:
        orgListEles=None
    print(orgListEles)
    time.sleep(2)
    custSaleStateReport={}

    if orgListEles!=None:
        custName=[]
        saleAmount=[]
        for ele in orgListEles:
            custName.append(ele.find_element_by_css_selector('h3').text)#获取客户名称
            saleAmount.append(ele.find_element_by_css_selector('p>span>span').text)#获取客户对应的销售额字段
        custSaleStateReport=dict(zip(custName,saleAmount))#生成客户：销售额键值对
        print(custSaleStateReport)
        Log("移动端客户销售动态报表有数据")
        return custSaleStateReport#返回销售员：销售额的键值对
    else:
        Log("移动端客户销售动态报表暂无数据")
        return None


#对比移动端和pc端客户销售动态报表的销售数据是否相等
def compareCustSaleStateReport(mobDriver,pcDriver,allOrgName):
    mobDriver.get("http://v-mobile-at/K3Cloud/KDMobile/BusinessAnalysis/index.html#/SaleNewsCustSaleState")#进入客户销售动态报表
    time.sleep(4)
    select_MobFilterScheme(mobDriver,allOrgName)#设置移动端组织列表
    time.sleep(5)
    custSaleStateReportVal=mobCustSaleStateReport(mobDriver)#调用移动端访问销售员业绩排名报表
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
    time.sleep(8)
    select_PcFilterScheme(pcDriver,orgSelectedList)#按照移动端报表所选组织设置pc端组织
    pcList=int(pcDriver.find_element_by_css_selector("span[data-kdid='sp_2_pagerlist2']").text)#检查pcdaunt是否有数据????????????????????????????1第？页/共n页
    time.sleep(2)
    if custSaleStateReportVal and orgSelectedList!=None and pcList!=0:
        custNameList=[]
        nameEles=pcDriver.find_elements_by_css_selector('span[data-field="FCUSTID_FNAME"]')#客户元素列表
        for ele in nameEles:
            custNameList.append(ele.text)
        noRepeatName=list(set(custNameList))#不重复的客户名称
        #noRepeatSale=[]
        pcSalAmountList=[]
        pcIncomeEles=pcDriver.find_elements_by_css_selector('span[data-field="FALLAMOUNT_LC"]')#物料价税合计本位币元素列表     多了个币别符号？？？？？？？？
        for ele in pcIncomeEles:
            pcSalAmountList.append((ele.text)[1:])#截取从第二位到结尾字符
       
        noRepeatDict={}

        for i in range(0,len(custNameList)):
            name=custNameList[i]
            if noRepeatDict.__contains__(name):
                temp=float(noRepeatDict[name])
                temp+=float(pcSalAmountList[i])
                noRepeatDict[name]=temp
            else:
                noRepeatDict[name]=pcSalAmountList[i]
        print(noRepeatDict)

        for i in noRepeatName:#依次检查不重复的客户名称，检查其对应金额是否相等
            salAmount=custSaleStateReportVal.get(i)#i产品对应的收入金额
            pcSalAmount=noRepeatDict.get(i)#i产品对应的收入金额
            if salAmount!= None and pcSalAmountList != '':
                if isNum(salAmount) and isNum(pcSalAmount):
                    print(float(salAmount))
                    print(float(pcSalAmount))
                    if float(salAmount)==float(pcSalAmount):#两个值相等时，pass
                        Log(i+":客户销售动态报表的销售数据：移动端销售金额与pc端销售金额相等")
                    else:
                        Log(i+":客户销售动态报表的销售数据：移动端销售金额与pc端销售金不相等")
                else:
                    Log(i+":客户销售动态报表的销售数据：有元素不为数字，请检查数值") 
            elif salAmount==None and pcSalAmountList=='':
                Log(i+"客户销售动态报表的销售数据：移动端、pc端均无数据")  
    elif pcList==0 and custSaleStateReportVal==False:
       Log("客户销售动态报表的销售数据：pc端暂无数据，金额为0,金额相等")
    elif pcList==None:
        Log("客户销售动态报表的销售数据：有不存在的元素")
    elif pcList==0 and custSaleStateReportVal!=False:
        Log("客户销售动态报表的销售数据：pc端数据为0，移动端有数据")
    elif pcList!=0 and custSaleStateReportVal==False:
        Log("客户销售动态报表的销售数据：移动端数据为0，pc端有数据")
    pcDriver.find_element_by_css_selector('span[class=" k-i-close mainTabCloseButton"]').click()

#移动端销售员收款排名报表    
def mobSaleRecRankingReport(driver):
    time.sleep(2)
    driver.get("http://v-mobile-at/K3Cloud/KDMobile/BusinessAnalysis/index.html#/SaleRecRanking")#销售员收款排名报表
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
    mobDriver.get("http://v-mobile-at/K3Cloud/KDMobile/BusinessAnalysis/index.html#/SaleRecRanking")#销售员收款排名报表
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
    time.sleep(8)
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

#一级用例启动
def saleAnafirstLeverTest(mobDriver,pcDriver,allOrgName):
    openSaleAnalysis(mobDriver)
    #login_pc(pcDriver,USERNAME,PASSWORD)
    
    try:
        compareCollectAmount(mobDriver,pcDriver)
    finally:
        print("执行完毕")
        #mobDriver.close()
        #pcDriver.close()
    try:
        compareSaleAmount(mobDriver,pcDriver)
    finally:
        print("执行完毕")
        #mobDriver.close()
        #pcDriver.close()
    try:
        compareSalOrgReport_sale(mobDriver,pcDriver,allOrgName)
    finally:
        print("执行完毕")
        #mobDriver.close()
        #pcDriver.close()
    try:
        #login_pc(pcDriver,USERNAME,PASSWORD)
        compareSalOrgReport_collect(mobDriver,pcDriver,allOrgName)
    finally:
        print("执行完毕")
        #mobDriver.close()
        #pcDriver.close()
    try:
        #login_pc(pcDriver,USERNAME,PASSWORD)
        compareSalDepReport_sale(mobDriver,pcDriver)
    finally:
        print("执行完毕")
        #mobDriver.close()
        #pcDriver.close()
    try:
        #login_pc(pcDriver,USERNAME,PASSWORD)
        compareSaleProfitsReport_income(mobDriver,pcDriver,allOrgName)
    finally:
        print("执行完毕")
        #mobDriver.close()
        #pcDriver.close()
    try:
        #login_pc(pcDriver,USERNAME,PASSWORD)
        compareSaleProfitsReport_cost(mobDriver,pcDriver,allOrgName)
    finally:
        print("执行完毕")
        #mobDriver.close()
        #pcDriver.close()
    try:
        #login_pc(pcDriver,USERNAME,PASSWORD)
        compareSaleProportionReport(mobDriver,pcDriver,allOrgName)
    finally:
        print("执行完毕")
        #mobDriver.close()
        #pcDriver.close()
    try:
        #login_pc(pcDriver,USERNAME,PASSWORD)
        compareNewCostReport(mobDriver,pcDriver,allOrgName)
    finally:
        print("执行完毕")
        #mobDriver.close()
        #pcDriver.close()
    try:
        #login_pc(pcDriver,USERNAME,PASSWORD)
        compareSaleRankingReport(mobDriver,pcDriver,allOrgName)
    finally:
        print("执行完毕")
        #mobDriver.close()
        #pcDriver.close()
    try:
        #login_pc(pcDriver,USERNAME,PASSWORD)
        compareCustSaleStateReport(mobDriver,pcDriver,allOrgName)
    finally:
        print("执行完毕")
        #mobDriver.close()
        #pcDriver.close()
    try:
        #login_pc(pcDriver,USERNAME,PASSWORD)
        compareSaleRecRankingReport(mobDriver,pcDriver,allOrgName)
    finally:
        print("执行完毕")
        #mobDriver.close()
        #pcDriver.close()

    
    
    
    
    
    
    
    
    


