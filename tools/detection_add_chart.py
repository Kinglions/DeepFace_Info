import os
import re
import logging
import pandas as pd
import matplotlib.pyplot as plt
from tools.prediction import prediction

def numeric_sort_key(s):
    """
    This function extracts all numbers from the filename and converts them to integers.
    """
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]


# 为 result 数据添加图表数据
def add_chart_data(df):
    logging.getLogger('matplotlib').setLevel(logging.WARNING)
    def save_pie_chart(data, labels, title, file_name):
        fig, ax = plt.subplots(figsize=(10, 8))
        wedges, texts, autotexts = ax.pie(data, labels=labels, autopct='%1.1f%%', startangle=90, counterclock=False)
        ax.legend(wedges, labels, title="Category", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        plt.setp(autotexts, size=8, weight="bold")
        ax.set_title(title)
        plt.subplots_adjust(top=0.85)
        plt.savefig(file_name, bbox_inches='tight')
        plt.close()

    print(f"\n------------- 正在添加图表数据 -------------")
    print(f"\n df: \n {df} \n")
    # 将 DataFrame 写入 CSV 文件
    resultFolder = '../../results'
    os.makedirs(resultFolder, exist_ok=True)
    csv_file = os.path.join(resultFolder,'result.csv')
    df.to_csv(csv_file, index=False)

    # 年龄段占比
    age_bins = [0, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    age_labels = [f'{i}-{i+9}' for i in age_bins[:-1]]
    df['年龄段'] = pd.cut(df['年龄'], bins=age_bins, labels=age_labels, right=False)
    age_counts = df['年龄段'].value_counts().sort_index()
    # 过滤掉计数为0的年龄段
    print(f"年龄图表绘制中...")
    age_counts = age_counts[age_counts > 0]
    if not age_counts.empty:
        save_pie_chart(age_counts, age_counts.index, 'Age Distribution', f'{resultFolder}/age_distribution.png')
    else:
        print("没有有效的年龄段数据进行图表展示。")
    
    # 性别占比
    print(f"性别图表绘制中......")
    gender_counts = df['性别'].value_counts()
    save_pie_chart(gender_counts, gender_counts.index, 'Gender', f'{resultFolder}/gender_distribution.png')

    # 肤色占比
    print(f"肤色图表绘制中.........")
    race_counts = df['肤色'].value_counts()
    save_pie_chart(race_counts, race_counts.index, 'Race', f'{resultFolder}/race_distribution.png')

def traverse_folder_images(folder):
    # 读取目录中的所有文件名，忽略隐藏文件
    files = [f for f in os.listdir(folder) if not f.startswith('.')]
    
    # # 使用自定义的排序键进行排序
    # files = sorted(files, key=numeric_sort_key)
    # # 创建空的DataFrame
    # df = pd.DataFrame(columns=['图片名称', '年龄', '性别', '肤色', '情绪', '预测结果'])
    # for file in files:
    #     if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png"):
    #         image_path = os.path.join(folder, file)
    #         result = prediction.predictionPersonInfo(image_path)
    #         if result is not None:  # 检查返回结果是否为None
    #             (file_name, age, gender, race, emotion, predictions) = result
    #             # 性别分类 (简单示例：男性为0，女性为1)
    #             df = pd.concat([df, pd.DataFrame([[file_name, age, gender, race, emotion, predictions]], columns=['图片名称', '年龄', '性别', '肤色', '情绪', '预测结果'])], ignore_index=True)
    #         else:
    #             print(f"No valid face data to process for image {file}. Skipping...")
    
    # add_chart_data(df)