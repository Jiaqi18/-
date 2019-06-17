# coding=utf-8
import pymysql
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
    #sql_mysql = "SELECT text from baidu_result WHERE  sentiment = 0 "
    #sql_mysql = "SELECT text from baidu_result WHERE  sentiment = 2 "
    sql_mysql = "SELECT text from baidu_result WHERE  sentiment = 1 "


    # 获取操作游标
    cur = sql_connet.cursor()
    # 从v_hcmedata表中查询字段
    try:
        # 执行sql语句
        cur.execute(sql_mysql)
        # 获取查询的所有记录 二维tuple
        results = cur.fetchall()
        l = list(results)
        #   字段处理
        #names = 'node_id node_name node_ipaddress res_id res_name  dd_name  mitem_id  mitem_name tablename'.split()
        names = 'review'

        # 二维tuple转换成列表嵌套字典
        managerList = [dict(zip(names, t)) for t in l]
    except Exception as e:
        raise e
    finally:
        sql_connet.close()  # 关闭连接
    # 数据转化成xml格式
    # 在内存中创建一个空的文档
    doc = xml.dom.minidom.Document()
    # 创建一个根节点Managers对象
    #root = doc.createElement('Managers')
    root = doc.createElement('reviews')
    # 设置根节点的属性
    #root.setAttribute('company', '00')
    #root.setAttribute('address', '00')
    # 将根节点添加到文档对象中
    doc.appendChild(root)
    for i in managerList:
        #nodeManager = doc.createElement('Manager')
        print(i)
        node_id = doc.createElement('review')
        node_id.appendChild(doc.createTextNode(str(i['r'])))


        #node_name = doc.createElement("node_name")
        #node_name.appendChild(doc.createTextNode(str(i["node_name"])))

        #node_ipaddress = doc.createElement("node_ipaddress")
        #node_ipaddress.appendChild(doc.createTextNode(str(i["node_ipaddress"])))

        #res_id = doc.createElement('res_id')
        #res_id.appendChild(doc.createTextNode(str(i['res_id'])))

        #res_name = doc.createElement("res_name")
        #res_name.appendChild(doc.createTextNode(str(i["res_name"])))

        #dd_name = doc.createElement("dd_name")
        #dd_name.appendChild(doc.createTextNode(str(i["dd_name"])))

        #mitem_id = doc.createElement('mitem_id')
        #mitem_id.appendChild(doc.createTextNode(str(i['mitem_id'])))

        #mitem_name = doc.createElement("mitem_name")
        #mitem_name.appendChild(doc.createTextNode(str(i["mitem_name"])))

        #tablename = doc.createElement("tablename")
        #tablename.appendChild(doc.createTextNode(str(i["tablename"])))

        # 将各叶子节点添加到父节点Manager中，
        # 最后将Manager添加到根节点Managers中
        root.appendChild(node_id)
    """
        nodeManager.appendChild(node_name)
        nodeManager.appendChild(node_ipaddress)
        nodeManager.appendChild(res_id)
        nodeManager.appendChild(res_name)
        nodeManager.appendChild(dd_name)
        nodeManager.appendChild(mitem_id)
        nodeManager.appendChild(mitem_name)
        nodeManager.appendChild(tablename)
        root.appendChild(nodeManager)
    """
    # 开始写xml文档
    fp1 = open('data\cn_neutral.xml', 'w')
    #fp1 = open('data\cn_positive.xml', 'w')
    #fp1 = open('data\cn_negative.xml', 'w')


    doc.writexml(fp1, indent='\t', addindent='\t', newl='\n',encoding="gbk")
    fp1.close()

if __name__ == '__main__':
    write_xml()