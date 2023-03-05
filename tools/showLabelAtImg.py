import cv2
import os
import numpy as np

box_class = ['trans', 'bridge', 'res1', 'triode', 'gnd', 'power1', 'res2', 'cap1', 'diode', 'cap2', 'mos', 'switch', 'amplifier', 'inductance', 'power2']


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


def make_box_white(image_dir=".\\yolov5DetectShow\\images", txt_dir=".\\yolov5DetectShow\\labels", save_dir=".\\yolov5DetectShow\\white"):
    '''抹白方框，便于识别导线

    :param save_dir: 保存路径
    :param image_dir: 图像的路径
    :param txt_dir: 标注txt的路径
    :return:
    '''
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
        cv2.imshow(image_path, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def show_label(image_dir, txt_dir):
    '''

    :param image_dir:
    :param txt_dir:
    :param class_list:
    :return:
    '''
    img_list = os.listdir(image_dir)
    img_list.sort()
    label_list = os.listdir(txt_dir)
    label_list.sort()
    for i in range(len(img_list)):
        image_path = image_dir + "\\" + img_list[i]
        txt_path = txt_dir + "\\" + label_list[i]
        show_label_in_one_image(image_path, txt_path, False)


def yolo_txt_to_box(image_path, label_path, save_dir):
    '''将标注数据转化为矩形框的二值图像

    :return:
    '''
    expand = 10  # 将box各个方向拉伸expand个像素点
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
        xmin = int((pos[i][1] - pos[i][3] / 2.) * image.shape[1]) - 3
        ymin = int((pos[i][2] - pos[i][4] / 2.) * image.shape[0]) - 3
        xmax = int((pos[i][1] + pos[i][3] / 2.) * image.shape[1]) + 3
        ymax = int((pos[i][2] + pos[i][4] / 2.) * image.shape[0]) + 3

        output = np.zeros((image.shape[0], image.shape[1]), np.uint8)
        output = cv2.rectangle(output, (xmin, ymin), (xmax, ymax), 255, 2)  # 显示标记框
        box_name = box_class[int(pos[i][0])] + "_" + str(map_[pos[i][0]])
        print(box_name)
        save_path = save_dir + "//" + box_name + ".png"
        print(save_path)

        cv2.imwrite(save_path, output)


        cv2.imshow(image_path, output)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    for k, v in sorted(map_.items()):
        print(f"{k} == {v}")
# img_folder = "C:\\Users\\a\\Desktop\\circuit\\test\\images"
# label_folder = "C:\\Users\\a\\Desktop\\circuit\\test\\labels"
# white_folder = ".\\yolov5DetectShow\\white"
# show_label(img_folder, label_folder)
# make_box_white(".\\test\\images",".\\test\\labels",".\\test\\white")  # 得到抹白图片
yolo_txt_to_box(".\\test\\images\\0002.jpg", ".\\test\\labels\\0002.txt", ".\\test\\box")


# img_list = os.listdir(img_folder)
# img_list.sort()
# label_list = os.listdir(label_folder)
# label_list.sort()
#
# for i in range(len(img_list)):
#     image_path = img_folder + "\\" + img_list[i]
#     txt_path = label_folder + "\\" + label_list[i]
#     draw_box_in_single_image(image_path, txt_path)
