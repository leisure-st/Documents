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
    #openHandHeldBursement(mobDriver)
    #saleAnafirstLeverTest(mobDriver,PCDriver,allOrgName)
    #openSaleAnalysis(mobDriver)
    #send_mailList(len(mailto_list),mailto_list,sub,content)#发送邮件
    #compareCollectAmount(mobDriver,PCDriver)
    #compareSaleAmount(mobDriver,PCDriver)
    #compareSalOrgReport_sale(mobDriver,PCDriver,allOrgName)
    #compareSalOrgReport_collect(mobDriver,PCDriver,allOrgName)
    #compareSalDepReport_sale(mobDriver,PCDriver)
    #mobSaleProfitsReport_income(mobDriver)
    #compareSaleProfitsReport_income(mobDriver,PCDriver,allOrgName)
    #mobSaleProfitsReport_cost(mobDriver)
    #compareSaleProfitsReport_cost(mobDriver,PCDriver,allOrgName)
    #mobSaleProportionReport(mobDriver)
    #compareSaleProportionReport(mobDriver,PCDriver,allOrgName)
    #mobNewCostReport(mobDriver)
    #compareNewCostReport(mobDriver,PCDriver,allOrgName)
    #mobSaleRankingReport(mobDriver)
    #compareSaleRankingReport(mobDriver,PCDriver,allOrgName)
    #mobCustSaleStateReport(mobDriver)
    #compareCustSaleStateReport(mobDriver,PCDriver,allOrgName)
    #compareSaleRecRankingReport(mobDriver,PCDriver,allOrgName)
    #openSaleReport(mobDriver)
    #compareSaleRecRankingReport(mobDriver,PCDriver,allOrgName,linkObject)
    #mobCustSaleProportionReport(mobDriver)
    #compareCustSaleProportionReport(mobDriver,PCDriver,allOrgName)
    #mobProSaleProportionReport(mobDriver)
    #compareProSaleProportionReport(mobDriver,PCDriver,allOrgName)
    #print(get_salAmount(mobDriver))
    # print(salAmount)
    # select_MobFilterScheme(mobDriver,orgName)
    #mobSalDepReport(mobDriver)
    #time.sleep(5)
    #mobSalOrgReport(mobDriver)
    #print(salAmount)
    #saleRepfirstLeverTest(mobDriver,PCDriver,allOrgName)
    #openHandHeldBursement(mobDriver)
    #billNumber=addExpenseRequest(mobDriver,PCDriver)
    #pushExpenseRequest(mobDriver,PCDriver,billNumber)
    #addExpReimbursement(mobDriver,PCDriver)
    #billNumber=addExpenseRequest_Travel(mobDriver,PCDriver)
    #pushExpenseRequest_Travel(mobDriver,PCDriver,billNumber)
    #addExpReimbursement_Travel(mobDriver,PCDriver)
    #openPlannerAssistant(mobDriver)
    #getPlannerMaterial(mobDriver)
    #comparePlannerMaterial(mobDriver,PCDriver)
    #openAmoeba(mobDriver)
    #setConfig(mobDriver)
    #flowQuery(mobDriver)
    #homePage(mobDriver)
    #compareHomePage(PCDriver,mobDriver)
    #compareFlowQuery(PCDriver,mobDriver)
    #setAmoeba(mobDriver)
    #addBill(mobDriver,2)
    #flowQuery(mobDriver)
    #balanceGroup(mobDriver)
    #compareBalanceGruop(PCDriver,mobDriver)
    #balanceList(mobDriver)
    #compareBalanceList(mobDriver,PCDriver)
    #profitRanking(mobDriver)
    #compareProRanking(mobDriver,PCDriver)
    openMobileReimb(mobDriver)
    #tempStorage(mobDriver,PCDriver)
    #appendExpenseRequest(mobDriver,PCDriver)
    #appendExpReimbursement(mobDriver,PCDriver)
    #appendExpenseRequest_Travel(mobDriver,PCDriver)
    appendExpReimbursement_Travel(mobDriver,PCDriver)


    # #登陆pc端
    #login_pc(PCDriver,USERNAME,PASSWORD)
    # pcSalAmount=get_pcsalAmount(PCDriver)
    # print(pcSalAmount)
    # # #print(pcSalAmount)
    # #select_PcFilterScheme(PCDriver,orgName)
    #Log("一级测试用例执行完毕")



    # pcSalOrgReport(PCDriver,mobDriver,allOrgName)
finally:
    Log("一级测试用例执行完毕")
    print("一级测试用例执行完毕")
    #mobDriver.close()
    #mobDriver.quit()
    #PCDriver.close()
    #PCDriver.close()

