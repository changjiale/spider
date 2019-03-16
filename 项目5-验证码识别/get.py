'''
获取接口的验证码图片
'''
import requests
import os
url = "http://acm.pdsu.edu.cn/vcode.php"

dir_path = 'img'
if not os.path.exists(dir_path):
    os.makedirs(dir_path)

for i in range(10):
	code = requests.get(url)
	img_path = dir_path + os.path.sep + str(i)+"image.jpg";
	with open(img_path,"wb") as f:
		f.write(code.content)
		f.close()