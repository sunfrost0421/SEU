import tools
from pathlib import Path
import os

tools.show_label_of("test")

img = ".\\data\\test\\images\\0001.jpg"
lab = ".\\data\\test\\labels\\0001.txt"
white = ".\\data\\test\\white\\w_0002.jpg"
# box_sub_dir = tools.TEST_PATH + "\\box\\" + Path(img).stem
# if Path(img).stem not in os.listdir(tools.TEST_PATH + "\\box\\"):
#     os.mkdir(box_sub_dir)
# else:
#     print(f"文件夹{box_sub_dir}已经存在，现在清空内部文件")
#     for x in os.listdir(box_sub_dir):
#         os.remove(box_sub_dir + "\\" + x)

# tools.yolo_txt_to_box(img, lab)
tools.nets_analyse(white,"show")


# tools.get_all_test_box()
# tools.make_all_test_box_white()
# tools.get_all_test_img_nets()
# tools.get_all_test_netlist()
