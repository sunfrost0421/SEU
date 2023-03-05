import torch
import matplotlib.pyplot as plt
import cv2
import os
import torchvision.transforms as transforms

import numpy as np
imgs_path = ".\images"
imgs_list = os.listdir(imgs_path)  # 返回一个文件夹内容的列表
print(imgs_list)
img1_path = os.path.join(imgs_path,imgs_list[0])
print(img1_path)
img = cv2.imread(img1_path)
print(img)
row, col, channel = img.shape  # 250,374,3
print(row,col,channel)
cv2.imshow("img",img)
cv2.waitKey(0) #等待按键
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)   ##要二值化图像，必须先将图像转为灰度图
cv2.imshow("gray",gray)
cv2.waitKey(0) #等待按键
print(gray)
# 大律法,全局自适应阈值 参数0可改为任意数字但不起作用
ret, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
print(ret)
cv2.imshow("binary", binary)  # 二值化之后黑色为0 白色为255
cv2.waitKey(0) #等待按键
cv2.imwrite("./images/binary.PNG", binary)
print(binary)



# b = transforms.ToTensor()(binary)//转为张量并且归一化
# print(b)
# print(b.size())

#img = img[:,:,::-1]
#plt.imshow(img)
# plt.show()

# img = img.copy()
# img = np.numpy(img)
# gray = transforms.Grayscale()(img)
# print(gray)
# img = transforms.ToTensor()(img)

# data_transform = transforms.Compose([
#  transforms.Resize(32), # 缩放图片(Image)，保持长宽比不变，最短边为32像素
#  transforms.CenterCrop(32), # 从图片中间切出32*32的图片
#  transforms.ToTensor(), # 将图片(Image)转成Tensor，归一化至[0, 1]
#  transforms.Normalize(mean=[0.492, 0.461, 0.417], std=[0.256, 0.248, 0.251]) # 标准化至[-1, 1]，规定均值和标准差
# ])
