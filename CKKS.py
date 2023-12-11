import tenseal as ts
import numpy as np
import os
import glob
from PIL import Image
import time


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
    pow_ = sub_ * sub_
    ans = pow_.decrypt()
    return ans


def SUB(m1, m2):
    sub_ = m1 - m2
    ans = sub_.decrypt()
    return ans


if __name__ == '__main__':
    start_time = time.time()
    image_list = import_jpg_files("./ImageNet64")
    context = context()

    # 查询图像
    random_query = np.random.randint(0, len(image_list))
    query_image = image_list[random_query]
    query_image = query_image.flatten()
    query_image = query_image / 255.0
    encrypted_query_image = ts.ckks_vector(context, query_image)

    # 加密并存储图像
    encrypted_images = []
    for i, img in enumerate(image_list):
        img = img.flatten()
        img = img / 255.0
        encrypted_image = ts.ckks_vector(context, img)
        encrypted_images.append(encrypted_image)

    # 对比查询图像与数据库中的加密图像
    mse_list = []

    for i, encrypted_image in enumerate(encrypted_images):
        mse = sum(MSE(encrypted_query_image, encrypted_image))
        print("查询图像与数据库中第" + str(i + 1) + "个图像的MSE：" + str(mse))
        mse_list.append(mse)

    print("查询图像在数据库中索引：" + str(random_query + 1))
    min_mse = min(mse_list)
    min_index = mse_list.index(min_mse)
    print("最佳匹配索引：" + str(min_index + 1))
    if random_query == min_index:
        print("匹配成功！")

    print("CKKS方法总耗时: " + str(time.time() - start_time))
