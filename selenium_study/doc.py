#Selenium 使用

#常用包
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

#浏览器对象

brower = webdriver.Chrome()
brower = webdriver.Firefox()
brower = webdriver.Edge()
brower = webdriver.PhantomJS() #无界面浏览器
brower = webdriver.Safari()
brower = webdriver.Opera()
brower = webdriver.Ie() #居然有IE
brower = webdriver.Android() #安卓自带浏览器
brower = webdriver.BlackBerry('') #树梅派

#访问页面
brower.get('https://www.baidu.com')
print(brower.page_source) #brower.page_source  获取页面源代码
brower.close()

#查找单节点
brower = webdriver.Chrome()
brower.get('https://www.taobao.com')
input_first = brower.find_element_by_id('q')
input_sec = brower.find_element_by_css_selector('#q')
input_third = brower.find_element_by_xpath('//*[@id="q"]')
brower.close()
#其中input_first、input_sec、input_third的类型都为  WebElement 类型

#所有获取单个节点的方法
#以下方法都是只能获取到第一个节点
brower.find_element()
brower.find_element_by_class_name('')
brower.find_element_by_css_selector('')
brower.find_element_by_id('')
brower.find_element_by_link_text('') #全文本匹配
brower.find_element_by_name('')
brower.find_element_by_partial_link_text('') #部分文本匹配
brower.find_element_by_tag_name('')
brower.find_element_by_xpath('')

#find_element()
#find_element()是find_element_by_class_name()这种方法的通用版本
#find_element()需要传两个参数： By和值
#find_element(By.ID, id) 等价于 find_element_by_id()
#用find_element()可以更加灵活
from selenium import webdriver
from selenium.webdriver.common.by import By

brower = webdriver.Chrome()
brower.get('https://www.baidu.com')
ele = brower.find_element(By.ID, 'q')
ele = brower.find_element(By.CLASS_NAME, 'classname')
ele = brower.find_element(By.XPATH, '//*[@id="q"]')
brower.close()

#获取多个节点
#其实就是在上述方法名中element后加上s，如find_elements()
#获取多个节点的方法都是返回一个WebElement数组，可以做遍历操作

#节点交互
from selenium import webdriver
import time

brower = webdriver.Chrome()
brower.get('https://www.taobao.com')

input = brower.find_element_by_id('q') #获取一个输入框对象
input.send_keys('iphone') #输入iphone
time.sleep(1) #暂停1s
input.clear() #清空输入框

button = brower.find_element_by_class_name('btn-search') #获取一个搜索按钮
button.click() #点击按钮

#以上是常用操作，更多操作可以参考官方文档 http://selenium-python.readthedocs.io/api.html

#动作链
#有一些交互动作，没有特定的执行对象，比如鼠标拖拽、键盘操作等等，这些动作要用另一种方式执行，这就是动作链
from selenium import webdriver
from selenium.webdriver import ActionChains

brower = webdriver.Chrome()
url = 'http://www.runoob.com/try/try.php?filename=jqueryui-api-droppable'
brower.get(url)
brower.switch_to.frame('iframeResult') #切换到指定的iframe元素中
source = brower.find_element_by_css_selector('#draggable') #首先找到一个开始节点
target = brower.find_element_by_css_selector('#droppable') #然后找到一个结束节点
actions = ActionChains(brower) #定义一个动作链对象
actions.drag_and_drop(source, target) #配置拖拽方法 从 source节点 拖拽到 target节点
actions.perform() #完成拖拽操作，定义动作链之后，总是要通过perform()方法来执行动作链

#更多的动作链操作可以参考官网文档：http://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.common.action_chains


#执行JS  execute_script()
#有些操作，selenium api 并没有提供，比如，下拉滚动条，他可以直接模拟运行JS
#这时就需要使用 execute_script()方法
from selenium import webdriver

brower = webdriver.Chrome()
brower.get('url')
brower.execute_script('window.scrollTo(0, document.body.scrollHeight)') #下拉滚动条到底部
brower.execute_script('alert("To Bottom")') #弹窗

#execute_script() 参数是js语句

#获取节点信息
#获取属性 get_attribute('class')
logo = brower.find_element_by_id('zh-top-link-logo') #获取节点
logo.get_attribute('class') #获取节点class属性的值
logo.get_attribute('id') #获取节点id的值
logo.get_attribute('data-*') #获取节点data-*的值

#获取文本值
input = brower.find_element_by_id('zh-top-add-question') #获取节点
input.text #获取节点文本值

#获取id、位置、标签名和大小
#WebElement节点有些属性可以不通过get_attribute来获取，可以直接点出来
input.id #id
input.location #location获取当前节点在页面中的位置
input.tag_name #tag_name获取标签名
input.size #size获取节点大小，也就是宽高

#切换frame   switch_to.frame()
#在网页中有一种节点叫 iframe， 也就是子frame,相当于页面的子页面，他的结构和外面的网页的结构完全一样
#selenium打开页面后，他默认是在父级frame里面操作，此时如果页面中有子frame, 他是无法获取到子frame中的节点的
#这时就需要 switch_to.frame() 方法来切换frame
brower.switch_to.frame('iframeResult') #切换到 name 等于iframeResult的frame
brower.switch_to.parent_frame() #切换到父级frame

#延时等待
#隐式等待，等待一个固定的时间
brower.implicitly_wait(10) #等待10s
#显式等待
#可以指定一个最长等待时间
#在这段时间内如果加载出来节点信息之后，则继续执行
#如果没有加载出来，则抛出一个超时异常
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(brower, 10) #实例化一个等待对象 wait
qinput = wait.until(EC.presence_of_element_located((By.ID，'q'))) #监听页面是否已经加载出 ID=q 的节点，加载出来之后获取节点
button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn-search'))) #监听页面元素是否加载出 class='btn-search' 按钮或者是这个按钮是否可以点击

#EC点出来的等待条件，还有很多等待条件，以下是比较常用的等待条件
EC.title_is             #标题是某内容
EC.title_contains       #标题包含某内容
EC.presence_of_element_located      #节点加载出来，传入定位元组，如(By.ID,'q')
EC.visibility_of        #可见，传入节点对象
EC.visibility_of_element_located    #节点可见，传入定位元组
EC.presence_of_all_elements_located #所有节点加载出来
EC.text_to_be_present_in_element    #某个节点文本包含某文字
EC.text_to_be_present_in_element_value #某个节点值包含某文字
EC.frame_to_be_available_and_switch_to_it   #加载并切换
EC.invisibility_of_element_located  #节点不可见
EC.element_to_be_clickable      #节点可点击
EC.staleness_of         #判断一个节点是否仍在DOM, 可判断页面是否已经刷新
EC.element_to_be_selected   #节点可选择，传节点对象
EC.element_located_to_be_selected   #节点可选择， 传入定位元组
EC.element_selection_state_to_be    #传入节点对象以及状态， 相等返回true, 否则返回false
EC.element_located_selection_state_to_be    #传入定位元组以及状态， 相等返回true, 否则返回false
EC.alert_is_present     #是否出现警告

#更多的等待条件参见官网文档：http://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.support.expected_conditions

#前进和后退 forwart()和back()
#平时使用浏览器的时候都有前进和后退功能
import time
from selenium import webdriver

brower = webdriver.Chrome()
#连续访问三个网站
brower.get('http://www.baidu.com')
brower.get('http://www.taobao.com')
brower.get('http://www.python.org')

brower.back() #返回到第二个页面 www.taobao.com
time.sleep(1)
brower.forward() #前进到第三个页面  www.python.org
brower.close()

#Cookies操作
#使用selenium 还可以操作Cookies
brower.get_cookies() #获取所有Cookies
brower.add_cookie({'name':'name', 'domain':'www.baidu.com'}) #添加cookie, 参数是一个json对象
brower.delete_all_cookies() #删除所有cookie
brower.delete_cookie('name') #删除指定名称的cookie

#选项卡管理
#selenium还可以操作浏览器的选项卡
brower.window_handles #获取当前已经打开的浏览器选项卡数组
brower.switch_to_window(brower.window_handles[0]) #切换到第一个选项卡  参数是window_handles中元素

#异常处理
#常用到的两个异常 TimeOutException和NoSuchElementException

from selenium.common.exceptions import TimeoutException, NoSuchElementException

try:
    brower.get('http://www.baidu.com')
except TimeoutException:
    print('Time Out')
try:
    brower.find_element_by_id('id')
except NoSuchElementException:
    print('No Element')
finally:
    brower.close()

#更多的异常类可以参考官网文档：http://selenium-python.readthedocs.io/api.html#module-selenium.common.exceptions
