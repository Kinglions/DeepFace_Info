# DeepFace_Info
解析人脸信息，例如年龄、性别、肤色、情绪

# 环境配置

###### 可以直接通过 conda 创建环境，便于管理，没有安装 conda 请自行安装，如果不想创建虚拟环境也可跳过该步骤
 ```
 conda create -n py && conda activate py
 ```
 # 依赖说明
 ```
deepface
torch 
torchvision
opencv-python
 ```

# 使用说明

```
cd 到项目目录
pip install -r requirements.txt
python detection.py
```
可以将想要解析的图片放置到 `images` 目录下

# 运行效果

![image](./demo.png)
