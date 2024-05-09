import os
from tools.detection_add_chart import traverse_folder_images

# 使用示例
target_folder = './images'
os.makedirs(target_folder, exist_ok=True)
traverse_folder_images(folder=target_folder)