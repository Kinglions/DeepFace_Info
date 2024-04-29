import os
import cv2
import numpy as np
from deepface import DeepFace
import classify
import re

def predictionPersonInfo(image_path):
    image = cv2.imread(image_path)
    # 检测人脸
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_image, 1.3, 5)

    # 分析每个检测到的脸部
    for (x, y, w, h) in faces:
        face = image[y:y+h, x:x+w]
        
        file_name = os.path.basename(image_path)
        print(f"\n\n------------- 正在预测 {file_name} 图片的数据 -------------")
        try:
            # 使用deepface来预测性别和年龄
            predictions = DeepFace.analyze(face, actions=['age', 'gender', 'race', 'emotion'], enforce_detection=False)[0]
        except Exception as e:
            print(f"An error occurred: {e}")
       
        age = predictions["age"]
        gender = predictions["dominant_gender"]
        race = predictions["dominant_race"]
        emotion = predictions["dominant_emotion"]
        print("\n年龄:", age)
        print("性别:", gender)
        print("肤色:", race)
        print("情绪:", emotion)

        # 肤色分析 (简单示例：计算平均色调)
        avg_color_per_row = np.average(face, axis=0)
        avg_color = np.average(avg_color_per_row, axis=0)
        avg_color = np.round(avg_color).astype(int)
        print("肤色均值:", avg_color)

def numeric_sort_key(s):
    """
    This function extracts all numbers from the filename and converts them to integers.
    """
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

def traverse_folder_images(folder):
    # 读取目录中的所有文件名，忽略隐藏文件
    files = [f for f in os.listdir(folder) if not f.startswith('.')]
    
    # 使用自定义的排序键进行排序
    files = sorted(files, key=numeric_sort_key)

    print(f"\n------------- 正在遍历图片 -------------\n {files} \n-----------------------")
    for file in files:
        if file.endswith(".jpg") or file.endswith(".png"):
            image_path = os.path.join(folder, file)
            predictionPersonInfo(image_path)
            classify.task_classify(image_path)

# 加载图像
folder = './images'
traverse_folder_images(folder)
