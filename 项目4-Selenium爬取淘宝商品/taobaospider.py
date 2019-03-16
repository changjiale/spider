import pymongo
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq
from urllib.parse import quote


'''
参数设置
'''
#采用无头的chrome去运行谷歌浏览器
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options)


#mongo地址
MONGO_URL = 'localhost'
#mongo数据库名称
MONGO_DB = 'taobao'
#指定数据库中的COLLECTION
MONGO_COLLECTION = 'products'
#指定搜索关键字
KEYWORD = '女装'
#设置最大爬取页面
MAX_PAGE = 2
#SERVICE_ARGS = ['--load-images=false', '--disk-cache=true']

#设置请求超时时间
wait = WebDriverWait(browser, 10)
#连接数据库
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

'''
抓取索引页面的信息
'''
def index_page(page):

	print('正在爬取第',page,'页')
	try:
		#quote解决中文传递url编码
		url = 'https://s.taobao.com/search?q='+quote(KEYWORD)
		browser.get(url)
		if page >1:
			#获取input标签
			input = wait.until(
					EC.presence_of_element_locationd((By.CSS_SELECTOR,'#mainsrp-pager div.form > input'))
				)
			#获取提交标签
			submit = wait.until(
            		EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager div.form > span.btn.J_Submit'))
                )
			#清空input标签内容
			input.clear()
			#设置页数
			input.send_keys(page)
			submit.click()

		#等待验证高亮页面标签是否为当前页
		wait.until(
           EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager li.item.active > span'), str(page)))
		#等待页面成功显示出标签内的内容
		wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemlist .items .item')))
		get_products()
	except TimeoutException as e:
		#超时重新请求
		index_page(page)

"""
提取商品数据
"""
def get_products():
	#获得源码
    html = browser.page_source
    #pyquery解析
    doc = pq(html)
    #获取解析列表
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'image': item.find('.pic .img').attr('data-src'),
            'price': item.find('.price').text(),
            'deal': item.find('.deal-cnt').text(),
            'title': item.find('.title').text(),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text()
        }
        print(product)
        save_to_mongo(product)

"""
保存至MongoDB
"""
def save_to_mongo(result):
    
    try:
        if db[MONGO_COLLECTION].insert(result):
            print('存储到MongoDB成功')
    except Exception:
        print('存储到MongoDB失败')

'''
构造分页
'''
def main():
    for i in range(1, MAX_PAGE + 1):
        index_page(i)
    browser.close()

if __name__ == '__main__':
    main()