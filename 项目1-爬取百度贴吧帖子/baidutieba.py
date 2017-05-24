#调用requests库
import requests
#调用bs4库中的BeautifulSoup， 并起别名sp
from bs4 import BeautifulSoup as sp

#神盾局吧url
yurl = "http://tieba.baidu.com/f?kw=%E7%A5%9E%E7%9B%BE%E5%B1%80&ie=utf-8"
#建立一个空列表， 存储需要抓取的n页帖子
urlist = []

#设置页数为3
n = 3

#用一个列表存放三页的url
for i in range(0,n):
    urlist.append("http://tieba.baidu.com/f?kw=%E7%A5%9E%E7%9B%BE%E5%B1%80&ie=utf-8&pn="+str(i*50))

for url in urlist:
    # 初始化一个列表来保存所有的帖子信息：
    contents = []

    #浏览器的header
    header = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
              'User - Agent': 'Mozilla / 5.0(Windows NT 6.1;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 56.0.2924.87Safari / 537.36'}

    #用requests的get()方法获取url 并转换为text格式
    html = requests.get(url, headers = header).text

    #用beautifulsoup的html.parser方法 解析源码
    soup = sp(html, "html.parser")

    #找到所有信息所在的父标签 - 具有j_thread_list clearfix’属性的li标签
    father = soup.find_all('li', attrs={'class': ' j_thread_list clearfix'})

    for body in father:
        #初始化一个字典来存储帖子的信息
        news = {}

        #异常处理
        try:
            #标题信息在父标签下的 具有'j_th_tit ’属性的a标签
            news['title'] = body.find('a',
                                    attrs={'class': 'j_th_tit '})['title']
            #print (count,news['title'])
            #链接信息在父标签下的 具有'j_th_tit’属性的a标签
            news['link'] = "http://tieba.baidu.com" + body.find('a',
                                    attrs={'class': 'j_th_tit '})['href']
            #用户名信息在父标签下的 具有'tb_icon_author ’属性的span标签
            news['name'] = body.find('span',
                                    attrs={'class': 'tb_icon_author '})['title']
            #id信息在父标签下的 具有'tb_icon_author ’属性的span标签 ,虽然输出看着像dict但是是str型
            news['id'] = body.find('span',
                                    attrs={'class': 'tb_icon_author '})['data-field']
            # 回复数量信息在父标签下的 具有'threadlist_rep_num center_text’属性的span标签，并用.string方法取出文本
            news['reply'] = body.find('span',
                                    attrs={'class': 'threadlist_rep_num center_text'}).string

            #将每个个帖子的信息都放入 contents的列表中
            contents.append(news)

        except:
            print ('信息无法显示')

    #建立文本，并用utf-8编码
    with open('shendunju.txt', 'a+',encoding='utf-8') as f:
        for  content in contents:
            #print('标题:%s    链接:%s     作者:%s     ID:%s    回复数量:%s'%(
                    #(content['title'],content['link'],content['name'][5:-1],content['id'][11:-1],content['reply'])))
            #写入到txt文本，并将内容做切片处理
            f.write('标题:%s\t 链接:%s\t 作者:%s\t ID:%s\t 回复数量:%s\t\n' % (
                (content['title'], content['link'], content['name'][5:-1], content['id'][11:-1], content['reply'])))