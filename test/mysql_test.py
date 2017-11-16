# # coding=utf-8
# import pymysql.cursors
# # connect to the database
# connection = pymysql.connect(host='127.0.0.1',
#                              user='root',
#                              password='root',
#                              db='test',
#                              charset='utf8mb4',
#                              cursorclass=pymysql.cursors.DictCursor)
# try:
#     with connection.cursor() as cursor:
# # Create a new record
#         sql = 'INSERT INTO sign_guest(realname,phone,email,sign,event_id,create_time)VALUES ("jack",18127813600,"jack@mail.com",0,1,NOW());'
#         cursor.execute(sql)
#
# # connection is not autocommit by default.so you must commit to save
# # your changes.
#         connection.commit()
#     with connection.cursor() as cursor:
#         sql = "SELECT realname ,phone,email,sign FROM sign_guest WHERE phone=%S"
#         cursor.execute(sql,('18127813600',))
#         result = cursor.fetchnoe()
#         print(result)
# finally:
#     connection.close()
#
# # connect() 建立数据库连接
# # execute() 执行 sql 语句
# # close() 关闭数据库连接