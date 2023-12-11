import tenseal as ts
import numpy as np
import os
import glob
from PIL import Image
import time
import sqlite3


def import_jpg_files(folder_path):
    jpg_files = glob.glob(os.path.join(folder_path, '*.jpg'))

    images = []
    for jpg_file in jpg_files:
        try:
            img_ = Image.open(jpg_file)
            img_ = np.array(img_)
            images.append(img_)
        except Exception as e:
            print(f"Error loading image {jpg_file}: {e}")

    return images


def context():
    context_ = ts.context(ts.SCHEME_TYPE.CKKS, 8192, coeff_mod_bit_sizes=[40, 21, 21, 21, 21, 40])
    context_.global_scale = pow(2, 21)
    context_.generate_galois_keys()
    return context_


def MSE(m1, m2):
    sub_ = m1 - m2
    pow_ = sub_.pow(2)
    ans = pow_.decrypt()
    return ans


if __name__ == '__main__':
    start_time = time.time()
    image_list = import_jpg_files("./ImageNet64")
    context = context()

    # 查询图像
    random_query = np.random.randint(0, len(image_list))
    query_image = image_list[random_query]
    query_image = query_image.flatten()
    # query_image = query_image / 255.0
    encrypted_query_image = ts.ckks_vector(context, query_image)

    # 打开数据库连接
    conn = sqlite3.connect('encrypted_images.db')

    # 创建游标对象
    cur = conn.cursor()

    # 执行SQL查询语句
    cur.execute('SELECT * FROM encrypted_images;')
    results = cur.fetchall()

    # 关闭游标和连接
    cur.close()
    conn.close()

    # 对比查询图像与数据库中的加密图像
    print(random_query + 1)
    for i, encrypted_image in enumerate(results):
        encrypted_image = list(encrypted_image)
        mse = sum(MSE(encrypted_query_image, encrypted_image)) / (64 * 64 * 3)
        print(mse)

    print("time:" + str(time.time() - start_time))
