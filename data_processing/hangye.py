import csv
import pymysql
import time


def do_save(data_list):
    # 连接数据库
    config = {
        "host": "127.0.0.1",
        "user": "root",
        "password": "123456",
        "database": "esg_news"
    }
    db = pymysql.connect(**config)

    # 使用cursor()方法创建一个游标对象
    cursor = db.cursor()

    # 使用execute()方法执行SQL语句
    # sql = "INSERT INTO news ('title', 'content', 'publish_time', 'add_time', 'industry', 'esg', 'label', 'url') VALUES ('广东能源局发文要求保障2019年竞价项目与配套接网工程同步建设', '近日，广东省能源局发布《关于加快推进可再生能源项目配套接网工程建设有关工作的通知》。', '2019-11-18 16:47:54', '2019-11-25 16:48:00', '1', '1', '1', '123'); "
    # sql = "select * from news"
    # cursor.execute(sql)
    for l in data_list:
        sql_news = "INSERT INTO news (title,content,publish_time,add_time,industry,esg,label,url) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
        t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # 获取当前时间
        cursor.execute(sql_news, (l[0], l[3], l[2], t, 1, 1, 1, l[1]))
        new_id = db.insert_id()  # 获取自动增长的id
        sql_relation = "INSERT INTO label_relation (new_id,label_id) VALUES(%s,%s)"
        cursor.execute(sql_relation, (new_id, 1))
    # # 使用fetall()获取全部数据(读取成功)
    # data = cursor.fetchall()
    # print(data)
    db.commit()  # 提交数据
    # 关闭游标和数据库的连接
    cursor.close()
    db.close()


def get_csv_date():
    with open(
            r'C:\Users\hwangnuozhong\Downloads\2020-1-6-17-22-58-24503269695399-保险行业动态-保险频道-金融界-采集的数据-后羿采集器.csv', 'r',
            errors='ignore', encoding='gbk') as csvfile:
        reader = csv.reader(csvfile)
        data_list = []
        for l in reader:
            data_list.append(l)
        # print(data_list[1:])
    return data_list[1:2]


if __name__ == "__main__":
    data_list = get_csv_date()
    # print(data_list)
    do_save(data_list)
