import jieba
import jieba.posseg as psg

# 停用词表加载方法
def get_stopword_list():
    # 停用词表存储路径，每一行为一个词，按行读取进行加载
    # 进行编码转换确保匹配准确率
    stop_word_path = './data/fenci_zidian/哈工大停用词表扩展.txt'
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
def load_data(pos=False, corpus_path='./data/semi/test/baidu_neu.txt'):
    # 调用上面方式对数据集进行处理，处理后的每条数据仅保留非干扰词
    doc_list = []
    space = ' '
    l = []
    i = 0
    f = open('./data/semi/test/baidu_neu_fenci.txt', 'w',encoding='utf8')
    file_userdict = './data/fenci_zidian/user_dict.txt'
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

def qukonghang():
    # -*- coding:utf-8 -*-

    f = open('./data/semi/train/rengong_pos_fenci.txt', 'r', encoding='utf8')
    g = open('./data/semi/train/rengong_pos_fencii.txt', 'w',encoding='utf8')

    try:
        while True:
            line = f.readline()
            #print(len(line))
            if len(line) == 0:
                continue
            if line.count('\n') == len(line):
                continue
            g.write(line)
    finally:
        f.close()
        g.close()

if __name__ == "__main__":
    load_data()
    # qukonghang()