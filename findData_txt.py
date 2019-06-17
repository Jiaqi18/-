# coding=utf-8
import pymysql
import re
import xml.dom.minidom
import sys, os

#reload(sys)
#sys.setdefaultencoding('utf8')
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.AL32UTF8'


def write_xml():
    # 连接数据库获取数据
    sql_connet = pymysql.connect(
        host='127.0.0.1', port=3306, user='root', passwd='root', db='el',charset='gbk'
    )
    sql_mysql = "SELECT text from baidu_result WHERE  sentiment = 0  and confidence > 0.8 "
    # sql_mysql = "SELECT text from baidu_result WHERE  sentiment = 2 and confidence > 0.9 "
    # sql_mysql = "SELECT text from baidu_result WHERE  sentiment = 1 and confidence > 0.9"
    # sql_mysql = "SELECT text from baidu_result WHERE  sentiment = 1 "
    # sql_mysql = "SELECT comment_content from answer_comments_2_copy WHERE  polarity = 1 "
    # sql_mysql =  "SELECT comment_content from answer_comments_2_copy WHERE polarity != ' ' and polarity = 0 "
    #sql_mysql = "SELECT text from baidu_result WHERE  sentiment = 0 "
    #sql_mysql = "SELECT text from baidu_result WHERE  sentiment = 2 "
    # sql_mysql = "SELECT text from baidu_result WHERE  sentiment = 1 "



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
                column = re.sub("[A-Za-z0-9\%\[\]\。\.\:\&\!\@\◆\_\&quot;]", "", column)
                row_list.append(column)

    except Exception as e:
        raise e
    finally:
        sql_connet.close()  # 关闭连接

    filename = open('./data/baidu_neg.txt', 'w', encoding='utf8')

    for result in row_list:
        filename.write(str(result) + '\n')

if __name__ == '__main__':
    write_xml()