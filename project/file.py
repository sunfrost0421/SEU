import os
import tools
name = "0001"
b_name = "res1_1"
head = name + ".TITLE\n\n"
netlist = tools.TEST_PATH + "\\netlist\\" + name + ".net"
f = open(netlist, "w")  # w 表示如果文件不存在创建，如果文件存在重新写入
f.write(head)
f.close()

fa = open(netlist, "a")  # a 表示在文件后面继续输入
fa.write("new1\n")
fa.write(b_name.title() + " ")

fa.write("net1")

fa.close()

# 网表SPICE语法