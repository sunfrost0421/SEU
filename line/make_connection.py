import cv2
import numpy as np
import os


def is_all_black(image):
    if cv2.countNonZero(image) == 0:  # 计算图片中像素不为0的个数
        return True
    else:
        return False

# 输入背景色为黑色的图片，对应像素相乘，如果超过255就变成255，这样就能求交集
def is_connected(box, net):
    # box = cv2.bitwise_not(box)  # 对图像取反
    # cv2.imshow("LSD", box)
    # cv2.waitKey(0)
    # net = cv2.bitwise_not(net)  # 对图像取反
    # cv2.imshow("LSD", net)
    # cv2.waitKey(0)
    out = box * net
    # out = cv2.multiply(box, net)
    # cv2.imshow("LSD", out)
    # cv2.waitKey(0)
    return not is_all_black(out)


def creat_netlist(box_dir, net_dir):
    box_list = os.listdir(box_dir)
    net_list = os.listdir(net_dir)
    for b in box_list:
        box = cv2.imread(box_dir + "\\" + b, 0)
        for n in net_list:
            net = cv2.imread(net_dir + "\\" + n, 0)
            if is_connected(box, net):
                print(f"{b}--->{n}")
    print("success")

creat_netlist(".\\box\\0002", ".\\subNet\\0002")


# box = ".\\box/res2_1.png"
# net = ".\\subNet/net_4.png"
# rr = is_connected(box, net)
# print(rr)
