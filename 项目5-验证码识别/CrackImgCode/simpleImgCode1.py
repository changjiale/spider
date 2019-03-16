'''
简单图形验证码识别
'''
import tesserocr
from PIL import Image

image = Image.open("code.jpg")
#利用Image对象的convert()方法参数传入L，转化为灰度图像
image = image.convert("L")
#进行二值化
#阈值127
threshold = 127
table = []
for i in range(256):
	if i < threshold:
		table.append(0)
	else:
		table.append(1)

image = image.point(table,'1')
image.show()
print (2)
result = tesserocr.image_to_text(image)
print(result)
print (1)