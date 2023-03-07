import os

def count_labelimg_data(path):
    '''
    使用labelimg标记完数据后，求出里面各个类别的数目：
    :param path: label文件夹路径
    :return: null
    '''
    class_dict = {}  # 创建一个存放结果的字典
    files = os.listdir(path)  # 该目录下所有文件的名字：'0001.txt', '0002.txt'。。。。
    # 分析类别
    class_file = path + "/" + "classes.txt"
    with open(class_file) as o:
        for line in o:
            class_dict[line.strip()] = 0
    count = [0 for _ in range(len(class_dict))]
    for file in files:
        if file != "classes.txt":
            with open(path + "/" + file) as o:
                for line in o:
                    index = int(line.split()[0])
                    count[index] += 1
    print(count)
    n = 0
    for name in class_dict.keys():
        print(f"{name}:{count[n]}")
        n = n+1





def count_yolo_data(path, classList):
    '''统计yolo数据集目录格式下各个类别的数量
    Parameters
    ----------
    path : str
        yolo数据集路径
    classList: list
        数据集类别名组成的列表， 名字顺序与Yolo标签的顺序一致
    Returns : none
    -------
    '''
    train_path = path + "/train/labels"
    valid_path = path + "/valid/labels"
    train_labels = os.listdir(train_path)
    valid_labels = os.listdir(valid_path)
    train_dir = {}
    train_count = [0 for _ in range(len(classList))]
    for file in train_labels:
        # print(train_path + "/" + file)
        with open(train_path + "/" + file) as o:
            for line in o:
                index = int(line.split()[0])
                train_count[index] += 1
    for i in range(len(classList)):
        train_dir[classList[i]] = train_count[i]
    print(f"train_dir:{train_dir}")
    valid_dir = {}
    valid_count = [0 for _ in range(len(classList))]
    for file in valid_labels:
        # print(valid_path + "/" + file)
        with open(valid_path + "/" + file) as o:
            for line in o:
                index = int(line.split()[0])
                valid_count[index] += 1
    for i in range(len(classList)):
        valid_dir[classList[i]] = valid_count[i]
    print(f"valid_dir:{valid_dir}")
    

data_path = "C:\\Users\\qrc\\Desktop\\newdata"
classList = ['trans', 'bridge', 'res1', 'triode', 'gnd', 'power1', 'res2', 'cap1', 'diode', 'cap2', 'mos', 'switch', 'amplifier', 'inductance', 'power2']
count_yolo_data(data_path,classList)

# path = "D:\workplace\data\DATA2-2\label"
# count_labelimg_data(path)


