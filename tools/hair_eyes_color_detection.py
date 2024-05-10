import cv2
import numpy as np
from sklearn.cluster import KMeans
import webcolors

def extract_features(image_path):
    # 加载图像
    image = cv2.imread(image_path)
    if image is None:
        return "Image not found"

    # 将图像转换到 RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # 使用OpenCV加载预训练的面部和眼部检测器
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    # 检测人脸
    faces = face_cascade.detectMultiScale(image, 1.3, 5)

    # 选择最大的人脸（最清晰）
    if len(faces) == 0:
        print("No face detected.")
        return
    main_face = max(faces, key=lambda rect: rect[2] * rect[3])  # width * height
    x, y, w, h = main_face

    # 提取人脸区域
    face = image[y:y+h, x:x+w]

    # 在人脸区域检测眼睛
    eyes = eye_cascade.detectMultiScale(face)
    labeled_eyes = {"left_eye": None, "right_eye": None}
    for (ex, ey, ew, eh) in eyes:
        eye_center = ex + ew // 2
        if eye_center < w / 2:
            labeled_eyes["left_eye_color"] = face[ey:ey+eh, ex:ex+ew]
        else:
            labeled_eyes["right_eye_color"] = face[ey:ey+eh, ex:ex+ew]

    datas = {}
    # 对每个眼睛进行颜色分析
    for eye_label, eye_region in labeled_eyes.items():
        if eye_region is not None:
            (title, color, name) = analyze_color(eye_region, eye_label)
            datas[title] = {"rgb": color, "web_color": name}

    # 提取发际线区域进行颜色分析
    hair_region = image[y:y+int(h*0.25), x:x+w]
    (title, color, name) = analyze_color(hair_region, "hair_color")
    datas[title] = {"rgb": color, "web_color": name}
    return datas

def closest_color(rgb):
    min_colors = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - rgb[0]) ** 2
        gd = (g_c - rgb[1]) ** 2
        bd = (b_c - rgb[2]) ** 2
        min_colors[(rd + gd + bd)] = name
    return min_colors[min(min_colors.keys())]

def analyze_color(region, title):
    # 将图像数据转换为二维数组
    data = region.reshape((-1,3))
    
    # 使用K-means算法找到最常见的颜色
    kmeans = KMeans(n_clusters=1)
    kmeans.fit(data)
    dominant_color = kmeans.cluster_centers_.astype(int)[0]

    # 尝试找到最接近的颜色名称
    try:
        closest_name = closest_color(dominant_color)
    except ValueError:
        closest_name = "No close color found"

    # 显示结果
    print(f"{title}: RGB{dominant_color} - Closest Color Name: {closest_name}")
    return (title, dominant_color, closest_name)

# # 测试函数
# extract_features("./../images/photo_4.jpg")
