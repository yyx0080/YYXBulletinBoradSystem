#初始化数据库表格
#只需要初始化时使用一次即可
import pymysql
# 提供相关参数建立数据库连接
conn = pymysql.connect(
                        host='localhost',
                        port=3306,
                        user='root',
                        password='123456789',
                        autocommit=True,
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor)

#获取数据库对象
cursor = conn.cursor()
#这里初始化有两种方式，要么自己建立一个数据库
#要么这里直接建立一个数据库，任意选择一种，注释掉另一种即可
#自己建立数据库
#1.连接数据库
conn.select_db("db")
#2.这里直接建立数据库
#cursor.execute("create database test")

#创建表格
#1.用户表
cursor.execute(
    """
    CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(20) NOT NULL UNIQUE,
    password VARCHAR(20) NOT NULL,
    point INT,
    last_login_date DATE
);
    """
)
#2.留言表
cursor.execute(
    """
    CREATE TABLE board (
    bid INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(20),
    content VARCHAR(800),
    boarddate DATE
);
    """
)

#最后关闭连接
cursor.close()
conn.close()
print("数据库初始化完成")



