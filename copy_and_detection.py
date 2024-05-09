import os
from tools import copy_random_images as cri
from tools import detection_add_chart as dac

# 使用示例
source_folder = './input'  # 替换为源文件夹的路径
target_folder = './images'
os.makedirs(target_folder, exist_ok=True)
cri.copy_random_images(source_folder=source_folder, target_folder=target_folder)
dac.traverse_folder_images(folder=target_folder)