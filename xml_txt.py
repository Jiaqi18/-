# -*- coding: utf-8 -*-
"""
Created on Fri Mar  2 15:36:44 2018
@author: gg
"""

import xml.dom.minidom
import os

# save_dir = './data/xmltxt/xml/cn_negative.xml'

f = open('./data/xmltxt/txt/cn_neutral.txt', 'w')
# 读取xml文件
DOMTree = xml.dom.minidom.parse('./data/xmltxt/xml/cn_neutral.xml')
# 获取review节点
annotation = DOMTree.documentElement
bb = annotation.getElementsByTagName("review")
# 打印review节点的值
# print(annotation.nodeName)
# print(bb[0].firstChild.data)
n = 0
# 遍历所有的revierw节点并写入文件
for i in range(len(bb)):
    n = n + 1
    if bb[i].firstChild:
        result = bb[i].firstChild.data
        # 去掉原来的换行，重新读数据，并加入换行
        result = result.strip("\n")
        print(result)
        f.write(result+"\n")
print(n)
