import copy_random_images as cri
import detection

# 使用示例
source_folder = './input'  # 替换为源文件夹的路径
target_folder = './images'
cri.copy_random_images(source_folder=source_folder, target_folder=target_folder)
detection.traverse_folder_images(folder=target_folder)