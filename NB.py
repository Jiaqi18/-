from time import time
from sklearn.datasets import load_files
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
# #步骤0，将文本问价处理成sklearn可以识别的文件格式
# # 读取总txt文件
# open_diff = open('data/rengong/rengong_neg.txt', 'r',encoding="utf8")
# diff_line = open_diff.readlines()
#
# line_list = []
# for line in diff_line:
#     line_list.append(line)
# # print(line_list)
#
# # 切分diff
# diff_match_split = [line_list[i:i + 1] for i in range(0, len(line_list))]
#
# # 将切分的写入多个txt中
# for i, j in zip(range(0, 2354), range(0, 2354)):
#     with open('data/rengong/rengong_neg/%d.txt' % j, 'w+') as temp:
#         for line in diff_match_split[i]:
#             temp.write(line)



# 步骤1：载入标注的训练语料
print("loading test dataset ...")
t = time()
# load file 专门用于载入分类的文档，每个分类一个单独的目录，目录名就是类名
news_train = load_files('data/rengong')
print("summary: {0} documents in {1} categories.".format(
    len(news_train.data), len(news_train.target_names)))
# news_train.target是长度为13180的一维向量，每个值代表相应文章的分类id
print('news_categories_names:\n{}, \nlen(target):{}, target:{}'.format(news_train.target_names,
                                                                       len(news_train.target), news_train.target))
print("done in {0} seconds\n".format(round(time() - t, 2)))

# 步骤2：将文档数据转化为TF-IDF向量
print("vectorizing test dataset ...")
t = time()
vectorizer = TfidfVectorizer(encoding='latin-1')
X_train = vectorizer.fit_transform((d for d in news_train.data))
print("n_samples: %d, n_features: %d" % X_train.shape)
# X_train每一行代表一篇文档，每个成员表示一个词的TF-IDF值，表示这个词对这个文章的重要性。
# X_train的形状是13180X130274
print("number of non-zero features in sample [{0}]: {1}".format(
    news_train.filenames[0], X_train[0].getnnz()))
print("done in {0} seconds\n".format(round(time() - t, 2)))

# 步骤3：使用多项式分布的朴素贝叶斯算法训练
print("traning models ...".format(time() - t))
t = time()
y_train = news_train.target
clf = MultinomialNB(alpha=0.0001)
clf.fit(X_train, y_train)
train_score = clf.score(X_train, y_train)
print("test score: {0}".format(train_score))
print("done in {0} seconds\n".format(round(time() - t, 2)))

# 步骤4：加载测试数据集
print("loading train dataset ...")
t = time()
news_test = load_files('data/NB/train')
print("summary: {0} documents in {1} categories.".format(
    len(news_test.data), len(news_test.target_names)))
print("done in {0} seconds\n".format(round(time() - t, 2)))

# 步骤5:把测试数据集向量化
print("vectorizing train dataset ...")
t = time()
# 注意这里调用的是transform而非上面的fit_transform。因为上面已经把数据统计好了
X_test = vectorizer.transform((d for d in news_test.data))
y_test = news_test.target
print("n_samples: %d, n_features: %d" % X_test.shape)
print("number of non-zero features in sample [{0}]: {1}".format(
    news_test.filenames[0], X_test[0].getnnz()))
print("done in %fs\n" % (time() - t))

# 步骤6：使用测试数据集测试。测试第一篇文章
print("predict for {} ...".format(news_test.filenames[1]))
pred = clf.predict(X_test[1])
print("predict: {0} is in category {1}".format(
    news_test.filenames[0], news_test.target_names[pred[0]]))
print("actually: {0} is in category {1}\n".format(
    news_test.filenames[1], news_test.target_names[news_test.target[1]]))

# 步骤7：评估算法的预测效果
print("predicting train dataset ...")
t = time()
pred = clf.predict(X_test)
print("done in %fs" % (time() - t))
print("classification report on train set for classifier:")
print(clf)
print(classification_report(y_test, pred,
                            target_names=news_test.target_names))

# 步骤8：生成混淆矩阵
cm = confusion_matrix(y_test, pred)
print("confusion matrix:")
print(cm)