import cv2
import time
import numpy as np


class CAM:
    '''
    摄像头输入
    从摄像头设备捕获实时图像
    '''
    
    def __init__(self):
        self.cap = None
        CAM.time = time.time()
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "摄像头索引": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 10,
                    "step": 1,
                    "display": "number",
                    "tooltip": "摄像头设备索引，通常0为默认摄像头"
                }),
                "宽度": ("INT", {
                    "default": 640,
                    "min": 320,
                    "max": 3840,
                    "step": 1,
                    "display": "number",
                    "tooltip": "图像宽度"
                }),
                "高度": ("INT", {
                    "default": 480,
                    "min": 240,
                    "max": 2160,
                    "step": 1,
                    "display": "number",
                    "tooltip": "图像高度"
                }),
            },
        }

    RETURN_TYPES = ("CVIMAGE","FLOAT")
    RETURN_NAMES = ("图像输出","时间戳")

    OUTPUT_TOOLTIPS = ("openCV(ndarray)格式的图片","当前的时间戳")

    def process(self, 摄像头索引, 宽度, 高度):
        try:
            # 如果摄像头未初始化或索引改变，重新初始化
            if self.cap is None or not self.cap.isOpened():
                if self.cap is not None:
                    self.cap.release()
                self.cap = cv2.VideoCapture(摄像头索引)
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 宽度)
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 高度)
                
            if not self.cap.isOpened():
                raise Exception(f"无法打开摄像头 {摄像头索引}")
            
            # 捕获一帧
            ret, frame = self.cap.read()
            
            if not ret:
                raise Exception("无法从摄像头读取图像")
            
            return (frame,CAM.time)
            
        except Exception as e:
            print(f"摄像头错误: {e}")
            # 返回一个黑色图像作为错误处理
            error_image = np.zeros((高度, 宽度, 3), dtype=np.uint8)
            cv2.putText(error_image, "Camera Error", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            return (error_image,CAM.time)
    
    @classmethod
    def IS_CHANGED(s, 摄像头索引, 宽度, 高度):
        CAM.time = time.time()
        return CAM.time
    
    def __del__(self):
        """析构函数，释放摄像头资源"""
        if hasattr(self, 'cap') and self.cap is not None:
            self.cap.release()
