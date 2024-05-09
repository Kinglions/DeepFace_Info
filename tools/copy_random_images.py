import os
import shutil
import random
from PIL import Image

target_folder = './images'  # 设定目标文件夹路径

def compress_and_convert_image(source_path, target_path):
    with Image.open(source_path) as img:
        # 如果原始图片不是JPEG，或者需要压缩，转换格式并保存为JPEG
        if img.format != 'JPEG' or os.path.splitext(source_path)[1].lower() != '.jpg':
            target_path = os.path.splitext(target_path)[0] + '.jpg'
        
        # 调整图片保存的质量，quality 参数为保存的质量，范围从 1（最差）到 95（最佳）
        img.save(target_path, 'JPEG', quality=60)

def copy_random_images(source_folder, target_folder, num_images=3000):
    # 确保目标文件夹存在，如果不存在，则创建它
    os.makedirs(target_folder, exist_ok=True)

    # 获取所有图片文件列表
    files = [f for f in os.listdir(source_folder) if f.endswith(tuple(Image.registered_extensions().keys()))]

    # 如果文件数量超过要求的数量，则随机挑选
    if len(files) > num_images:
        files = random.sample(files, num_images)

    # 复制和重命名图片
    for i, filename in enumerate(files, start=1):
        print(f"正在复制第 {i} 张图片..., 原图名称: {filename}")
        source_path = os.path.join(source_folder, filename)
        target_path = os.path.join(target_folder, f'photo_{i}.jpg')
        compress_and_convert_image(source_path, target_path)

    print(f"已成功复制 {len(files)} 张图片到 {target_folder}。")
