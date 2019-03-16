from PIL import Image
import pytesseract
import tesserocr
from PIL import Image

import re
'''
获取图片
'''
def getImage():
    fileName = 'vcode.jpg'
    img = Image.open(fileName)
    # 打印当前图片的模式以及格式
    print('未转化前的: ', img.mode, img.format)
    # 使用系统默认工具打开图片
    img.show()
    return img

'''
1) 将图片进行降噪处理, 通过二值化去掉后面的背景色并加深文字对比度
'''
def convert_Image(img, standard=127.5):
    '''
    【灰度转换】
    '''
    image = img.convert('L')

    '''
    【二值化】
    根据阈值 standard , 将所有像素都置为 0(黑色) 或 255(白色), 便于接下来的分割
    '''
    pixels = image.load()
    for x in range(image.width):
        for y in range(image.height):
            if pixels[x, y] > standard:
                pixels[x, y] = 255
            else:
                pixels[x, y] = 0
    return image


'''
使用 pytesseract 库来识别图片中的字符
'''
def change_Image_to_text(img):
    '''
    如果出现找不到训练库的位置, 需要我们手动自动
    语法: tessdata_dir_config = '--tessdata-dir "<replace_with_your_tessdata_dir_path>"'
    '''
    print(1)
    # CHANGE THIS IF TESSERACT IS NOT IN YOUR PATH, OR IS NAMED DIFFERENTLY
    testdata_dir_config = '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR"'
    textCode = pytesseract.image_to_string(img, lang='eng', config=testdata_dir_config)
    # 去掉非法字符，只保留字母数字
    textCode = re.sub("\W", "", textCode)
    return textCode

def main():
    img = convert_Image(getImage())
    print(2)
    print('识别的结果：', change_Image_to_text(img))

if __name__ == '__main__':
    main()