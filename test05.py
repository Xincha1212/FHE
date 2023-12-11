import sqlite3
import tenseal as ts
from PIL import Image
import numpy as np
import os
import glob


def context():
    context_ = ts.context(ts.SCHEME_TYPE.CKKS, 8192, coeff_mod_bit_sizes=[40, 21, 21, 21, 21, 40])
    context_.global_scale = pow(2, 21)
    context_.generate_galois_keys()
    return context_


image_list = np.array([[1, 2, 3], [2, 3, 4]])
context = context()

encrypted_images = []
for i, img in enumerate(image_list):
    img = img.flatten()

    encrypted_image = ts.ckks_vector(context, img)
    encrypted_images.append(encrypted_image)

# 连接到SQLite数据库
db_connection = sqlite3.connect("exp1.db")
cursor = db_connection.cursor()

# 创建数据库表
cursor.execute('''CREATE TABLE IF NOT EXISTS encrypted_images
(id INTEGER PRIMARY KEY AUTOINCREMENT, encrypted_vector TEXT)''')

# 将加密的图像向量插入数据库表
for enc_vector in encrypted_images:
    encrypted_data = ','.join(map(str, enc_vector.serialize()))  # 将向量序列化为字符串
    cursor.execute('INSERT INTO encrypted_images (encrypted_vector) VALUES (?)', (encrypted_data,))

# 提交更改并关闭连接
db_connection.commit()
db_connection.close()
