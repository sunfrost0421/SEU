import os
import torch

imgs_path = "D:\\workplace\\data\\newdata"
imgs_list = os.listdir(imgs_path)  # 返回一个文件夹内容的列表
imgs_list.sort()
print(imgs_list)
index = 1
for img in imgs_list:
    new_name = "qrc"+str(index)+".jpg"
    os.rename(imgs_path+"/"+img, imgs_path+"/"+new_name)
    index = index+1
index = 1
imgs_list = os.listdir(imgs_path)  # 返回一个文件夹内容的列表
for img in imgs_list:
    new_name = str(index).zfill(4)+".jpg"
    os.rename(imgs_path+"/"+img, imgs_path+"/"+new_name)
    index = index+1
print("转换成功")