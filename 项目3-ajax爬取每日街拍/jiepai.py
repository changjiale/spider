import requests
from urllib.parse import urlencode
from requests import codes
import os
from hashlib import md5
from multiprocessing.pool import Pool
import re

#拼接url获取响应的ajax内容
def get_page(offset):
    params = {
        'aid': '24',
        'offset': offset,
        'format': 'json',
        #'keyword': '街拍',
        'autoload': 'true',
        'count': '20',
        'cur_tab': '1',
        'from': 'search_tab',
        'pd': 'synthesis'
    }
    base_url = 'https://www.toutiao.com/api/search/content/?keyword=%E8%A1%97%E6%8B%8D'
    url = base_url + urlencode(params)
    try:
        resp = requests.get(url)
        print(url)
        if 200  == resp.status_code:
            print(resp.json())
            return resp.json()
    except requests.ConnectionError:
        return None

#获取图片url和名称
def get_images(json):
    if json.get('data'):
        data = json.get('data')
        for item in data:
            if item.get('cell_type') is not None:
                continue
            title = item.get('title')
            images = item.get('image_list')
            for image in images:
                origin_image = re.sub("list", "origin", image.get('url'))
                #print(image.get('url'))
                #print(re.sub("list", "origin", image.get('url')))
                yield {
                    'image':  origin_image,
                    # 'iamge': image.get('url'),
                    'title': title
                }

print('succ')

#将图片保存到本地
def save_image(item):
    #创建目录信息  img-> item.get('title')
    img_path = 'img' + os.path.sep + item.get('title')
    print('succ2')
    if not os.path.exists(img_path):
        os.makedirs(img_path)
    try:
        resp = requests.get(item.get('image'))
        if codes.ok == resp.status_code:
            #拼接文件名称文件，并用md5打散
            file_path = img_path + os.path.sep + '{file_name}.{file_suffix}'.format(
                file_name=md5(resp.content).hexdigest(),
                file_suffix='jpg')
            if not os.path.exists(file_path):
                print('succ3')
                with open(file_path, 'wb') as f:
                    #写入信息
                    f.write(resp.content)
                print('Downloaded image path is %s' % file_path)
                print('succ4')
            else:
                print('Already Downloaded', file_path)
    except requests.ConnectionError:
        print('Failed to Save Image，item %s' % item)


def main(offset):
    json = get_page(offset)
    for item in get_images(json):
        print(item)
        save_image(item)


GROUP_START = 0
GROUP_END = 7

if __name__ == '__main__':
    pool = Pool()
    groups = ([x * 20 for x in range(GROUP_START, GROUP_END + 1)])
    pool.map(main, groups)
    pool.close()
    pool.join()