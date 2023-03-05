import cv2
import numpy as np

# 读入图片
img = cv2.imread(".\\img\\w_0002.jpg")
# 中值滤波，去噪
img = cv2.medianBlur(img, 3)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.namedWindow('original', cv2.WINDOW_AUTOSIZE)
cv2.imshow('original', gray)
cv2.waitKey()
# 阈值分割得到二值化图片
ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
binary = cv2.bitwise_not(binary)  # 对图像取反
# 膨胀操作
# kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
# bin_clo = cv2.dilate(binary, kernel2, iterations=2)

# 连通域分析
num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary, connectivity=8)

# 查看各个返回值
# 连通域数量
print('num_labels = ',num_labels)
# 连通域的信息：对应各个轮廓的x、y、width、height和面积
print('stats = ',stats)
# 连通域的中心点
print('centroids = ',centroids)
# 每一个像素的标签1、2、3.。。，同一个连通域的标签是一致的
print('labels = ',labels)
# 统计每一个标签的数量
map_ = {}
for i in labels:
    for j in i:
        map_[j] = map_.get(j, 0) + 1
for k,v in sorted(map_.items()):
    if v < img.shape[0]*img.shape[1]*0.001:  # 剔除像素点较少的连通域
        del map_[k]
    if v > img.shape[0]*img.shape[1]*0.8:   # 剔除背景元素
        del map_[k]
for k, v in sorted(map_.items()):
    print(f"{k} == {v}")
print(map_.keys())


# 不同的连通域赋予不同的颜色
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

# # 分割出不同的连通域
for i in map_.keys():
    output = np.zeros((img.shape[0], img.shape[1]), np.uint8)
    mask = labels == i
    output[:, :][mask] = 255
    subnet_name = ".\\subNet\\0002\\net_" + str(i) + ".png"
    cv2.imwrite(subnet_name, output)
    cv2.imshow(subnet_name, output)
    cv2.waitKey()
    cv2.destroyAllWindows()
