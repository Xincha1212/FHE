import sqlite3

# 打开数据库连接
conn = sqlite3.connect('encrypted_images_bfv.db')

# 创建游标对象
cur = conn.cursor()

# 执行SQL查询语句
cur.execute('SELECT * FROM encrypted_images;')
results = cur.fetchall()
r1 = results[0]
l = len(r1[1])
# 输出结果
print(results)
print(l)
# 关闭游标和连接
cur.close()
conn.close()
