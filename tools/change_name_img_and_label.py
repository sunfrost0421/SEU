import os
import torch


root_path = "C:\\Users\\a\\Desktop\\circuit\\test"
imgs_path = root_path+"\\images"
label_path = root_path+"\\labels"
imgs_list = os.listdir(imgs_path)  # 返回一个文件夹内容的列表
label_list = os.listdir(label_path)
imgs_list.sort()
label_list.sort()
print(imgs_list)
print(label_list)
index = 376
for img in imgs_list:
    new_name = "qrc"+str(index)+".jpg"
    os.rename(imgs_path+"/"+img, imgs_path+"/"+new_name)
    index = index+1
index = 376
imgs_list = os.listdir(imgs_path)  # 返回一个文件夹内容的列表
for img in imgs_list:
    new_name = str(index).zfill(4)+".jpg"
    os.rename(imgs_path+"/"+img, imgs_path+"/"+new_name)
    index = index+1
print("转换成功")

index = 376
for lab in label_list:
    new_name = "qrc"+str(index)+".txt"
    os.rename(label_path+"/"+lab, label_path+"/"+new_name)
    index = index+1
index = 376
label_list = os.listdir(label_path)  # 返回一个文件夹内容的列表
for lab in label_list:
    new_name = str(index).zfill(4)+".txt"
    os.rename(label_path+"/"+lab, label_path+"/"+new_name)
    index = index+1
print("转换成功")
print(imgs_list)
print(label_list)