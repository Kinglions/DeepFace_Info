import cv2
import os
import numpy as np
from deepface import DeepFace
from tools import hair_eyes_color_detection as hecd

def predictionPersonInfo(image_path):
    image = cv2.imread(image_path)
    
    current_file_path = __file__  # 获取当前文件的路径
    directory = os.path.dirname(current_file_path)  # 获取文件所在目录
    # 加载预训练的模型和配置文件
    modelFile = os.path.join(directory, "res10_300x300_ssd_iter_140000.caffemodel")
    configFile = os.path.join(directory, "deploy.prototxt.txt")
    net = cv2.dnn.readNetFromCaffe(configFile, modelFile)
    
    # 构造一个blob从图片
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0,
        (300, 300), (104.0, 177.0, 123.0))

    # 输入blob到网络并获得检测结果
    net.setInput(blob)
    detections = net.forward()

    # 确保至少检测到一个脸
    if detections.shape[2] == 0:
        print("No face detected.")
        return None
    
    # 处理检测结果
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:  # 确定置信度阈值
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            face = image[startY:endY, startX:endX]
            break
    
    file_name = os.path.basename(image_path)
    print(f"\n\n------------- 正在预测 {file_name} 图片的数据 -------------")
    try:
        predictions = DeepFace.analyze(face, actions=['age', 'gender', 'race', 'emotion'], enforce_detection=False)[0]
        print(f"predictions: \n{predictions}")
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    datas = hecd.extract_features(image_path)
    print(f"---------datas: \n{datas}")
    predictions["hair_eyes_color"] = datas

    age = predictions["age"]
    gender = predictions["dominant_gender"]
    race = predictions["dominant_race"]
    emotion = predictions["dominant_emotion"]
    left_eye_color = datas["left_eye_color"]["web_color"]
    right_eye_color = datas["right_eye_color"]["web_color"]
    hair_color = datas["hair_color"]["web_color"]
    print("\n年龄:", age)
    print("性别:", gender)
    print("肤色:", race)
    print("情绪:", emotion)
    print("左眼:", left_eye_color)
    print("右眼:", right_eye_color)
    print("发色:", hair_color)
    
    return (file_name, age, gender, race, emotion, left_eye_color, right_eye_color, hair_color, predictions)
