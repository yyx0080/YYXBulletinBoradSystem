#这是一个测试数据库的文件，仅仅作为测试使用
# 导入pymysql
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
#在数据库中执行sql语句
#这里创建完数据库后，要将这一段注释掉，改为下面一段
#cursor.execute("create database test")
#连接数据库
conn.select_db("test")
#创建用户表
#同样的，创建完就注释掉

# cursor.execute(
#     """
#     create table useryyxtest
#     (
#         id       int primary key auto_increment comment '用户身份标识',
#         username varchar(20) comment '用户名',
#         password varchar(20) comment '密码'
#     ) comment '用户表';
#     """
# )

# 增 
cursor.execute("insert into useryyxtest (username, password) values ('zhangsan', '123')")  # 添加用户1
cursor.execute("insert into useryyxtest (username, password) values ('lisi', '1234');")  # 添加用户2

# 删
#cursor.execute("delete from user where id = 1")  # 删除id为1的用户

# 改
#cursor.execute("update user set password = '123456'")  # 设置所有用户密码为123456

# 提交修改
conn.commit()


# 查！
cursor.execute("select * from useryyxtest")
#利用cursor.fetchall拿到结果
res:tuple = cursor.fetchall()

print(res)
for it in res:
    print(it)

#最后关闭连接
cursor.close()
conn.close()

print("hello world")