import easyocr
from mmocr.utils.ocr import MMOCR
IMAGE_PATH = 'D:\workplace\qrc\picture\images\ele.PNG'

# easyocr
reader = easyocr.Reader(['ch_sim','en'])
result1 = reader.readtext(IMAGE_PATH,paragraph="False")
print(result1)

# mmocr
# ocr = MMOCR()
# results2 = ocr.readtext(IMAGE_PATH, print_result=True, imshow=True)