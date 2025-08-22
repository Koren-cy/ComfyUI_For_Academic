import cv2
import numpy as np
import torch

class CVToIMAGE:
    '''
    OpenCV图像转IMAGE
    将OpenCV(ndarray)格式的图像转换为ComfyUI的IMAGE格式
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "图像输入": ("CVIMAGE", {
                    "tooltip": "OpenCV格式的图像(ndarray)"
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("图像输出",)
    OUTPUT_TOOLTIPS = ("ComfyUI IMAGE格式的图片",)

    def process(self, 图像输入):
        # 确保输入是numpy数组
        if not isinstance(图像输入, np.ndarray):
            raise Exception("输入必须是numpy数组格式")
        
        # 处理不同的图像格式
        if len(图像输入.shape) == 2:  # 灰度图像 (H, W)
            # 转换为RGB格式
            rgb_image = cv2.cvtColor(图像输入, cv2.COLOR_GRAY2RGB)
        elif len(图像输入.shape) == 3:
            if 图像输入.shape[2] == 1:  # 单通道灰度 (H, W, 1)
                rgb_image = cv2.cvtColor(图像输入, cv2.COLOR_GRAY2RGB)
            elif 图像输入.shape[2] == 3:  # BGR图像 (H, W, 3)
                rgb_image = cv2.cvtColor(图像输入, cv2.COLOR_BGR2RGB)
            elif 图像输入.shape[2] == 4:  # BGRA图像 (H, W, 4)
                rgb_image = cv2.cvtColor(图像输入, cv2.COLOR_BGRA2RGB)
            else:
                raise Exception(f"不支持的通道数: {图像输入.shape[2]}")
        else:
            raise Exception(f"不支持的图像维度: {图像输入.shape}")
        
        # 确保数据类型为uint8
        if rgb_image.dtype != np.uint8:
            # 如果是浮点数，假设范围是0-1，转换为0-255
            if rgb_image.dtype in [np.float32, np.float64]:
                if rgb_image.max() <= 1.0:
                    rgb_image = (rgb_image * 255).astype(np.uint8)
                else:
                    rgb_image = rgb_image.astype(np.uint8)
            else:
                rgb_image = rgb_image.astype(np.uint8)
        
        # 转换为torch tensor并归一化到[0,1]
        image_tensor = torch.from_numpy(rgb_image.astype(np.float32) / 255.0)
        
        # 添加batch维度 (1, H, W, C)
        image_tensor = image_tensor.unsqueeze(0)
        
        return (image_tensor,)