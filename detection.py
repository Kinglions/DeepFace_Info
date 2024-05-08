import os
import cv2
import numpy as np
from deepface import DeepFace
import classify
import re
import pandas as pd
from openpyxl import Workbook
from openpyxl.chart import PieChart, Reference
from pandas import ExcelWriter
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

def predictionPersonInfo(image_path):
    image = cv2.imread(image_path)
    # 检测人脸
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_image, 1.3, 5)
    if len(faces) == 0:
        print("No face detected.")
        return None
    
    (x, y, w, h) = faces[0]
    # 分析每个检测到的脸部
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

    # # 肤色分析 (简单示例：计算平均色调)
    # avg_color_per_row = np.average(face, axis=0)
    # avg_color = np.average(avg_color_per_row, axis=0)
    # avg_color = np.round(avg_color).astype(int)
    # print("肤色均值:", avg_color)

    print("\n------------- 数据保存成功 -------------")
    return (file_name, age, gender, race, emotion)

def numeric_sort_key(s):
    """
    This function extracts all numbers from the filename and converts them to integers.
    """
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]


# 为 result 数据添加图表数据
def add_chart_data(df):
    print(f"\n------------- 正在添加图表数据 -------------")
    print(f"\n df: \n {df} \n")
    # 将 DataFrame 写入 CSV 文件
    resultFolder = './results'
    os.makedirs(resultFolder, exist_ok=True)
    csv_file = os.path.join(resultFolder,'result.csv')
    df.to_csv(csv_file, index=False)
    # 设置中文支持，假设字体文件名为 'SimHei.ttf'，路径根据实际情况调整
    font_path = '/System/Library/Fonts/SFNS.ttf'  # 示例路径，请根据实际情况修改
    prop = FontProperties(fname=font_path)
    def save_pie_chart(data, labels, title, file_name):
        fig, ax = plt.subplots(figsize=(10, 8))
        wedges, texts, autotexts = ax.pie(data, labels=labels, autopct='%1.1f%%', startangle=90, counterclock=False)
        ax.legend(wedges, labels, title="Category", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), prop=prop)
        plt.setp(autotexts, size=8, weight="bold", fontproperties=prop)
        plt.setp(texts, fontproperties=prop)
        ax.set_title(title, fontproperties=prop)
        plt.subplots_adjust(top=0.85)
        plt.savefig(file_name, bbox_inches='tight')
        plt.close()

    # 年龄段占比
    age_bins = [0, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    age_labels = [f'{i}-{i+9}' for i in age_bins[:-1]]
    df['年龄段'] = pd.cut(df['年龄'], bins=age_bins, labels=age_labels, right=False)
    age_counts = df['年龄段'].value_counts().sort_index()
    # 过滤掉计数为0的年龄段
    age_counts = age_counts[age_counts > 0]
    if not age_counts.empty:
        save_pie_chart(age_counts, age_counts.index, 'Age Distribution', './results/age_distribution.png')
    else:
        print("没有有效的年龄段数据进行图表展示。")
    
    # 性别占比
    gender_counts = df['性别'].value_counts()
    save_pie_chart(gender_counts, gender_counts.index, 'Gender', './results/gender_distribution.png')

    # 肤色占比
    race_counts = df['肤色'].value_counts()
    save_pie_chart(race_counts, race_counts.index, 'Race', './results/race_distribution.png')

def traverse_folder_images(folder="./images"):
    # 读取目录中的所有文件名，忽略隐藏文件
    files = [f for f in os.listdir(folder) if not f.startswith('.')]
    
    # 使用自定义的排序键进行排序
    files = sorted(files, key=numeric_sort_key)

    print(f"\n------------- 正在遍历图片 -------------\n")

    # 创建空的DataFrame
    df = pd.DataFrame(columns=['图片名称', '年龄', '性别', '肤色', '情绪'])
    for file in files:
        if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png"):
            image_path = os.path.join(folder, file)
            result = predictionPersonInfo(image_path)
            if result is not None:  # 检查返回结果是否为None
                (file_name, age, gender, race, emotion) = result
                classify.task_classify(image_path)
                # 性别分类 (简单示例：男性为0，女性为1)
                df = pd.concat([df, pd.DataFrame([[file_name, age, gender, race, emotion]], columns=['图片名称', '年龄', '性别', '肤色', '情绪'])], ignore_index=True)
            else:
                print(f"No valid face data to process for image {file}. Skipping...")
    
    add_chart_data(df)


traverse_folder_images()