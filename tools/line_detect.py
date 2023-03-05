# coding=utf-8
import cv2
import numpy as np

# 读取输入图片
img0 = cv2.imread(".\\yolov5DetectShow\\white\\w_demo01.jpg")
# 将彩色图片转换为灰度图片
img = cv2.cvtColor(img0,cv2.COLOR_BGR2GRAY)

# 创建一个LSD对象
lsd = cv2.createLineSegmentDetector(0)
# 执行检测结果
dlines = lsd.detect(img)  # dline[0]存储着每条直线的坐标[[x01,y01,x11,y11]...[x0i,yoi,x1i,y1i]]  i表示第i条直线
# 绘制检测结果
for dline in dlines[0]:
    x0 = int(round(dline[0][0]))  # round四舍五入函数
    y0 = int(round(dline[0][1]))
    x1 = int(round(dline[0][2]))
    y1 = int(round(dline[0][3]))
    print(x0,y0,x1,y1)
    # cv2.line(img0, (x0, y0), (x1,y1), (0,255,0), 1, cv2.LINE_AA)  #BGR
    #
    # # 显示并保存结果
    # #cv2.imwrite('w_demo01.jpg', img0)
    # cv2.imshow("LSD", img0)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
