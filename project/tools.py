import os
import cv2
import numpy as np
from pathlib import Path

box_class = ['trans', 'bridge', 'res1', 'triode', 'gnd', 'power1', 'res2', 'cap1', 'diode', 'cap2', 'mos', 'switch', 'amplifier', 'inductance', 'power2']
TEST_PATH = ".\\data\\test"
TRAIN_PATH = ".\\data\\train"
# yolo_txt_to_box中的expand表示扩大box框的参数，可以保证与net有交集从而判断连接
# nets_analyse中的205行有参数，将像素点较少的连通域去掉，所以确保电路线的像素点大于文字的

def read_yolo_txt(path):
    '''将yolo格式的label文件读取到数组

    :param path: 存放yolo算法标记txt文件
    :return: 返回一个list<list<Double>>,存储每一行的每一个数据
    '''
    pos = []
    with open(path, 'r') as f:
        while True:
            lines = f.readline()  # 整行读取数据
            if not lines:
                break
            # 将整行数据分割处理，如果分割符是空格，括号里就不用传入参数，如果是逗号， 则传入‘，'字符。
            p_tmp = [float(i) for i in lines.split(' ')]
            pos.append(p_tmp)  # 添加新读取的数据
            pass
    return pos


def show_label_in_one_image(image_path, label_path, show_label=True):
    '''是标注文件在图像中显示

    :param image_path: 图像的路径
    :param label_path: 标注txt的路径
    :show_label: 是否展示类别标签，默认是
    :return:
    '''
    pos = read_yolo_txt(label_path)  # 读取txt的数据，每一行数据代表一个方框
    image = cv2.imread(image_path)  # 读取图片的数据
    # 遍历所有方框
    for i in range(len(pos)):
        # image.shape[0]表示图像的垂直高度H，image.shape[1]表示图像的水平宽度W
        # pos[i]表示第i行数据，也就是第i个矩形标注的数据。
        # (x, y)：矩形框中心点坐标   wb：矩形框的水平宽度    hb：矩形框的垂直高度
        # pos[i][0]:类别    pos[i][1]:x/W    pos[i][2]:y/H    pos[i][3]:wb/W    pos[i][4]:hb/H
        # (xmin, ymin)：矩形框左上角坐标    (xmax, ymax)：矩形框右下角坐标
        xmin = int((pos[i][1] - pos[i][3] / 2.) * image.shape[1])
        ymin = int((pos[i][2] - pos[i][4] / 2.) * image.shape[0])
        xmax = int((pos[i][1] + pos[i][3] / 2.) * image.shape[1])
        ymax = int((pos[i][2] + pos[i][4] / 2.) * image.shape[0])
        label = str(int(pos[i][0]))
        image = cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 0, 255), 2)  # 显示标记框
        if show_label == True:
            cv2.putText(image, label, (xmin, ymin - 2), 0, 0.75, [0, 0, 255], thickness=1, lineType=cv2.LINE_AA)  # 显示类别
        pass

    cv2.imshow(image_path, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def show_label(root_dir):
    '''展示标签

    :param root_dir:
    :return:
    '''
    image_dir = root_dir + "\\images"
    txt_dir = root_dir + "\\labels"
    img_list = os.listdir(image_dir)
    img_list.sort()
    label_list = os.listdir(txt_dir)
    label_list.sort()
    for i in range(len(img_list)):
        image_path = image_dir + "\\" + img_list[i]
        txt_path = txt_dir + "\\" + label_list[i]
        show_label_in_one_image(image_path, txt_path, True)

def show_label_of(dir="test"):
    if dir == "test":
        show_label(TEST_PATH)
    elif dir == "train":
        show_label(TRAIN_PATH)
    else:
        print("show_label_of的参数只能填写：test、train")

def yolo_txt_to_box(image_path, label_path):
    '''将一张图片标注数据转化为矩形框的二值图像

    :return:
    '''
    expand = 10  # 将box各个方向拉伸expand个像素点
    box_sub_dir = TEST_PATH + "\\box\\" + Path(image_path).stem
    if Path(image_path).stem not in os.listdir(TEST_PATH + "\\box\\"):
        os.mkdir(box_sub_dir)
        print(f"文件夹{box_sub_dir}成功创建")
    else:
        print(f"文件夹{box_sub_dir}已经存在，现在清空内部文件")
        for x in os.listdir(box_sub_dir):
            os.remove(box_sub_dir + "\\" + x)
    pos = read_yolo_txt(label_path)  # 读取txt的数据，每一行数据代表一个方框
    image = cv2.imread(image_path)  # 读取图片的数据
    map_ = {}
    # 遍历所有方框
    for i in range(len(pos)):
        # image.shape[0]表示图像的垂直高度H，image.shape[1]表示图像的水平宽度W
        # pos[i]表示第i行数据，也就是第i个矩形标注的数据。
        # (x, y)：矩形框中心点坐标   wb：矩形框的水平宽度    hb：矩形框的垂直高度
        # pos[i][0]:类别    pos[i][1]:x/W    pos[i][2]:y/H    pos[i][3]:wb/W    pos[i][4]:hb/H
        # (xmin, ymin)：矩形框左上角坐标    (xmax, ymax)：矩形框右下角坐标
        map_[pos[i][0]] = map_.get(pos[i][0], 0) + 1
        xmin = int((pos[i][1] - pos[i][3] / 2.) * image.shape[1]) - expand
        ymin = int((pos[i][2] - pos[i][4] / 2.) * image.shape[0]) - expand
        xmax = int((pos[i][1] + pos[i][3] / 2.) * image.shape[1]) + expand
        ymax = int((pos[i][2] + pos[i][4] / 2.) * image.shape[0]) + expand

        output = np.zeros((image.shape[0], image.shape[1]), np.uint8)
        output = cv2.rectangle(output, (xmin, ymin), (xmax, ymax), 255, 2)  # 显示标记框
        box_name = box_class[int(pos[i][0])] + "_" + str(map_[pos[i][0]])
        # print(box_name)
        save_path = box_sub_dir + "\\" + box_name + ".png"
        print(save_path)
        cv2.imwrite(save_path, output)
        # cv2.imshow(image_path, output)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
    for k, v in sorted(map_.items()):
        print(f"{box_class[int(k)]} == {v}")

def get_all_test_box():
    img_dir = TEST_PATH + "\\images"
    lab_dir = TEST_PATH + "\\labels"
    for i in os.listdir(img_dir):
        name = Path(i).stem
        img = img_dir + "\\" + name + ".jpg"
        lab = lab_dir + "\\" + name + ".txt"
        if os.path.exists(img) and os.path.exists(lab):
            print(f"get boxes of {i}")
            yolo_txt_to_box(img, lab)
        else:
            print(f"{name}文件缺失")

def make_all_test_box_white():
    '''抹白元器件，返回处理后的图片

    :return:
    '''
    image_dir = TEST_PATH + "\\images"
    txt_dir = TEST_PATH + "\\labels"
    save_dir = TEST_PATH + "\\white"
    img_list = os.listdir(image_dir)
    img_list.sort()
    label_list = os.listdir(txt_dir)
    label_list.sort()
    #遍历所有图片
    for j in range(len(img_list)):
        image_path = image_dir + "\\" + img_list[j]
        label_path = txt_dir + "\\" + label_list[j]
        pos = read_yolo_txt(label_path)  # 读取txt的数据，每一行数据代表一个方框
        image = cv2.imread(image_path)  # 读取图片的数据
        # 遍历所有方框
        for i in range(len(pos)):
            # image.shape[0]表示图像的垂直高度H，image.shape[1]表示图像的水平宽度W
            # pos[i]表示第i行数据，也就是第i个矩形标注的数据。
            # (x, y)：矩形框中心点坐标   wb：矩形框的水平宽度    hb：矩形框的垂直高度
            # pos[i][0]:类别    pos[i][1]:x/W    pos[i][2]:y/H    pos[i][3]:wb/W    pos[i][4]:hb/H
            # (xmin, ymin)：矩形框左上角坐标    (xmax, ymax)：矩形框右下角坐标
            xmin = int((pos[i][1] - pos[i][3] / 2.) * image.shape[1])
            ymin = int((pos[i][2] - pos[i][4] / 2.) * image.shape[0])
            xmax = int((pos[i][1] + pos[i][3] / 2.) * image.shape[1])
            ymax = int((pos[i][2] + pos[i][4] / 2.) * image.shape[0])
            image = cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (255, 255, 255), -1)  # 显示标记框，-1表示填充
            pass
        save_path = save_dir + "\\w_" + img_list[j]
        cv2.imwrite(save_path, image)
        # cv2.imshow(image_path, image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
    print("已得到所有抹白图片")

def nets_analyse(w_img_path, option="segment"):
    ''' 分析一张图片的所有网络

    :param w_img_path:
    :param option:
    :return:
    '''
    img = cv2.imread(w_img_path,0)
    # 中值滤波，去噪
    img = cv2.medianBlur(img, 3)
    cv2.namedWindow('original', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('original', img)
    cv2.waitKey()
    # 阈值分割得到二值化图片
    ret, binary = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    binary = cv2.bitwise_not(binary)  # 对图像取反，背景色为黑
    # 连通域分析
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary, connectivity=8)
    # 统计每一个连通域的数量
    map_ = {}
    for i in labels:
        for j in i:
            map_[j] = map_.get(j, 0) + 1
    for k, v in sorted(map_.items()):
        if v < img.shape[0] * img.shape[1] * 0.0008:  # 剔除像素点较少的连通域
            del map_[k]
        if v > img.shape[0] * img.shape[1] * 0.8:  # 剔除背景元素连通域
            del map_[k]
    # for k, v in sorted(map_.items()):
    #     print(f"{k} == {v}")
    # print(map_.keys())
    # 不同的连通域赋予不同的颜色,并展示
    if option == "show":
        output = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
        for i in range(1, num_labels):
            mask = labels == i
            if i in map_.keys():
                output[:, :, 0][mask] = np.random.randint(0, 255)
                output[:, :, 1][mask] = np.random.randint(0, 255)
                output[:, :, 2][mask] = np.random.randint(0, 255)
        cv2.imshow('oginal', output)
        cv2.waitKey()
        cv2.destroyAllWindows()
    elif option == "segment":  # 分割出不同的连通域
        s = Path(w_img_path).stem
        dir_name = s.split("_")[1]
        root_path = TEST_PATH + "\\subnet"
        dir_path = root_path + "\\" + dir_name
        if dir_name not in os.listdir(root_path):
            os.mkdir(dir_path)
            print(f"文件夹{dir_path}成功创建")
        else:
            print(f"文件夹{dir_path}已经存在，现在清空内部文件")
            for x in os.listdir(dir_path):
                os.remove(dir_path + "\\" + x)
        j = 1
        for i in map_.keys():
            output = np.zeros((img.shape[0], img.shape[1]), np.uint8)
            mask = labels == i
            output[:, :][mask] = 255
            subnet_name = dir_path + "\\net" + str(j) + ".png"
            cv2.imwrite(subnet_name, output)
            j = j + 1
            cv2.imshow(subnet_name, output)
            cv2.waitKey()
            cv2.destroyAllWindows()
    else:
        print("option的参数只能填写：segment、show")

def get_all_test_img_nets():
    white_dir = TEST_PATH + "\\white"
    for w_img in os.listdir(white_dir):
        print(f"分割{w_img}的网络")
        nets_analyse(white_dir + "\\" + w_img)
    print("所有图片的网络分割完毕")

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
    '''分析一张图片所有的网表连接关系

    :param box_dir:
    :param net_dir:
    :return:
    '''
    box_list = os.listdir(box_dir)
    net_list = os.listdir(net_dir)
    name = Path(box_dir).stem  # 这张图片的名字0001
    netlist = TEST_PATH + "\\netlist\\" + name + ".net"


    for b in box_list:

        box = cv2.imread(box_dir + "\\" + b, 0)
        for n in net_list:

            net = cv2.imread(net_dir + "\\" + n, 0)
            if is_connected(box, net):
                print(f"{b}--->{n}")
    print("success")

def get_all_test_netlist():
    box_root = TEST_PATH + "\\box"
    subnet_root = TEST_PATH + "\\subnet"
    for name in os.listdir(box_root):
        boxes = box_root + "\\" + name
        nets = subnet_root + "\\" + name
        if os.path.exists(boxes) and os.path.exists(nets):
            print("====================================================")
            print(f"分析{name}的网表")
            creat_netlist(boxes, nets)
        else:
            print(f"{name}文件缺失")
# creat_netlist(".\\box\\0002", ".\\subNet\\0002")