import pymysql
import xml.dom.minidom
import sys, os
import re

import codecs

import string

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.AL32UTF8'


def data_pre():
    # 连接数据库获取数据
    sql_connet = pymysql.connect(
        host='127.0.0.1', port=3306, user='root', passwd='root', db='el',charset='gbk'
    )

    sql_mysql = "SELECT comment_content from answer_comments_2 order by comment_content desc "



    # 获取操作游标
    cur = sql_connet.cursor()
    # 从v_hcmedata表中查询字段
    try:
        # 执行sql语句
        cur.execute(sql_mysql)
        # 获取查询的所有记录 二维tuple
        results = cur.fetchall()
        row_list = []
        for row in results:

            for column in row:
                column = re.sub("[A-Za-z0-9\%\&\@]", "", column)
                row_list.append(column)

        names = 'review'

        # 二维tuple转换成列表嵌套字典


    except Exception as e:
        raise e
    finally:
        sql_connet.close()  # 关闭连接

    filename = open('./data/data_pre.txt', 'w', encoding='utf8')

    for result in row_list:
        filename.write(str(result) + '\n')

def yaci ():
    # -*- coding: utf-8 -*-
    inputfile = './data/data_pre.txt'  # 评论文件
    outputfile = './data/data_pre_yaci.txt' # 评论处理后保存路径
    f = codecs.open(inputfile, 'r', 'utf-8')
    f1 = codecs.open(outputfile, 'w', 'utf-8')
    fileList = f.readlines()
    f.close()
    for A_string in fileList:
        temp1 = A_string.strip('\n')  # 去掉每行最后的换行符'\n'
        temp2 = temp1.lstrip('\ufeff')
        temp3 = temp2.strip('\r')
        char_list = list(temp3)
        list1 = ['']
        list2 = ['']
        del1 = []
        flag = ['']
        i = 0
        while (i < len(char_list)):
            if (char_list[i] == list1[0]):
                if (list2 == ['']):
                    list2[0] = char_list[i]
                else:
                    if (list1 == list2):
                        t = len(list1)
                        m = 0
                        while (m < t):
                            del1.append(i - m - 1)
                            m = m + 1
                        list2 = ['']
                        list2[0] = char_list[i]
                    else:
                        list1 = ['']
                        list2 = ['']
                        flag = ['']
                        list1[0] = char_list[i]
                        flag[0] = i
            else:
                if (list1 == list2) and (list1 != ['']) and (list2 != ['']):
                    if len(list1) >= 2:
                        t = len(list1)
                        m = 0
                        while (m < t):
                            del1.append(i - m - 1)
                            m = m + 1
                        list1 = ['']
                        list2 = ['']
                        list1[0] = char_list[i]
                        flag[0] = i
                else:
                    if (list2 == ['']):
                        if (list1 == ['']):
                            list1[0] = char_list[i]
                            flag[0] = i
                        else:
                            list1.append(char_list[i])
                            flag.append(i)
                    else:
                        list2.append(char_list[i])
            i = i + 1
            if (i == len(char_list)):
                if (list1 == list2):
                    t = len(list1)
                    m = 0
                    while (m < t):
                        del1.append(i - m - 1)
                        m = m + 1
                    m = 0
                    while (m < t):
                        del1.append(flag[m])
                        m = m + 1
        a = sorted(del1)
        t = len(a) - 1
        while (t >= 0):
            # print(char_list[a[t]])
            del char_list[a[t]]
            t = t - 1
        str1 = "".join(char_list)
        str2 = str1.strip()  # 删除两边空格
        f1.writelines(str2 + '\r\n')
    f1.close()

def qukonghang():
    # -*- coding:utf-8 -*-

    f = open('./data/data_pre_yaci_wukonghang_fenci.txt', 'r', encoding='utf8')
    g = open('./data/data_pre_yaci_wukonghang_fenci.txt', 'w',encoding='utf8')

    try:
        while True:
            line = f.readline()
            #print(len(line))
            if len(line) == 2:
                continue
            if line.count('\n') == len(line):
                continue
            g.write(line)
    finally:
        f.close()
        g.close()


def count():
    num_words = []
    num_line = 0

    with open("./data/data_pre_yaci_wukonghang_fenci.txt", "r", encoding='utf-8') as f:
        while f.readline():
            line = f.readline()
            print(line)
            counter = len(line.split())
            num_words.append(counter)
            num_line = num_line + 1

    print('文件总数', num_line)
    print('所有的词的数量', sum(num_words))
    print('平均文件词的长度', sum(num_words) / len(num_words))

    import matplotlib
    matplotlib.use('TkAgg')
    import matplotlib.pyplot as plt

    # 指定默认字体
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']
    matplotlib.rcParams['font.family'] = 'sans-serif'
    plt.hist(num_words, 50, facecolor='g')
    plt.xlabel('文本长度')
    plt.ylabel('频次')
    plt.axis([0, 120, 0, 10000])
    plt.show()

def shortDel():
    num_words = []
    num_line = 0
    g = open('./data/data_pre_yaci_wukonghang_wuduanjv.txt', 'w', encoding='utf8')
    with open("./data/data_pre_yaci_wukonghang.txt", "r", encoding='utf-8') as f:
        while f.readline():
            line = f.readline()
            #print(line)
            #counter = len(line.split())
            counter = len(line)
            if (counter) > 6:
                num_words.append(counter)
                g.write(line)

            num_line = num_line + 1

    #print('文件总数', num_line)
    print('所有的词的数量', sum(num_words))
    print('平均句子的长度', sum(num_words) / len(num_words))

    import matplotlib
    matplotlib.use('TkAgg')
    import matplotlib.pyplot as plt

    # 指定默认字体
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']
    matplotlib.rcParams['font.family'] = 'sans-serif'
    plt.hist(num_words, 50, facecolor='g')
    plt.xlabel('文本长度')
    plt.ylabel('频次')
    plt.axis([0, 200, 0, 10000])
    plt.show()


import jieba
import jieba.posseg as psg

# 停用词表加载方法
def get_stopword_list():
    # 停用词表存储路径，每一行为一个词，按行读取进行加载
    # 进行编码转换确保匹配准确率
    stop_word_path = './data/哈工大停用词表扩展.txt'
    stopword_list = [sw.replace('\n', '') for sw in open(stop_word_path,encoding='utf-8').readlines()]
    return stopword_list


# 分词方法，调用结巴接口
def seg_to_list(sentence, pos=False):
    if not pos:
        # 不进行词性标注的分词方法
        seg_list = jieba.cut(sentence)
    else:
        # 进行词性标注的分词方法
        seg_list = psg.cut(sentence)
    return seg_list


# 去除干扰词
def word_filter(seg_list, pos=False):
    stopword_list = get_stopword_list()
    filter_list = []
    # 根据POS参数选择是否词性过滤
    ## 不进行词性过滤，则将词性都标记为n，表示全部保留
    for seg in seg_list:
        if not pos:
            word = seg
            flag = 'n'
        else:
            word = seg.word
            flag = seg.flag
        if not flag.startswith('n'):
            continue
        # 过滤停用词表中的词
        #if not word in stopword_list and len(word) > 1:
        if not word in stopword_list:
            filter_list.append(word)

    return filter_list


# 数据加载，pos为是否词性标注的参数，corpus_path为数据集路径
def load_data(pos=False, corpus_path='./data/data_pre_yaci_wukonghang.txt'):
    # 调用上面方式对数据集进行处理，处理后的每条数据仅保留非干扰词
    doc_list = []
    space = ' '
    l = []
    i = 0
    f = open('./data/data_pre_yaci_wukonghang_fenci.txt', 'w',encoding='utf8')
    file_userdict = './data/userdict.txt'
    jieba.load_userdict(file_userdict)
    for line in open(corpus_path, 'rb'):
        content = line.strip()
        seg_list = seg_to_list(content, pos)
        filter_list = word_filter(seg_list, pos)
        for temp_term in filter_list:
            l.append(temp_term)
        l.append('\n')
    f.write(space.join(l) + '\n')
    i = i + 1
    if (i % 200 == 0):
        print('Saved ' + str(i) + ' articles')

    f.close()

def rengong_dataSelect():
    # 连接数据库获取数据
    sql_connet = pymysql.connect(
        host='127.0.0.1', port=3306, user='root', passwd='root', db='el',charset='gbk'
    )

    sql_mysql = "SELECT comment_content from answer_comments_2_copy WHERE polarity != ' ' and polarity = 0 or polarity = 2"



    # 获取操作游标
    cur = sql_connet.cursor()
    # 从v_hcmedata表中查询字段
    try:
        # 执行sql语句
        cur.execute(sql_mysql)
        # 获取查询的所有记录 二维tuple
        results = cur.fetchall()
        row_list = []
        for row in results:

            for column in row:
                column = re.sub("[A-Za-z0-9\%\&\@]", "", column)
                row_list.append(column)

        names = 'review'

        # 二维tuple转换成列表嵌套字典


    except Exception as e:
        raise e
    finally:
        sql_connet.close()  # 关闭连接

    filename = open('./data/rengong_youqinggan.txt', 'w', encoding='utf8')

    for result in row_list:
        filename.write(str(result) + '\n')

import re
def quguanggao():
    f = open('./data/answer_comments_2.txt', 'r', encoding='utf8')
    g = open('./data/answer_comments_quguanggao.txt', 'w', encoding='utf8')

    try:
        while True:
            line = f.readline()
            line = "" + line
            if re.findall("公众号",line):
                print(line)
                g.write(line)
            elif re.findall("微信",line):
                print(line)
                g.write(line)
    finally:
        f.close()
        g.close()


if __name__ == '__main__':
    #yaci()
    #qukonghang()
    #count()
    # shortDel()
    # rengong_dataSelect()
    # quguanggao()
    rengong_dataSelect()


