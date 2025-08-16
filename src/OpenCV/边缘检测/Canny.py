import cv2
import numpy as np

class Canny:
    '''
    Canny边缘检测
    Canny算法是一种经典的边缘检测算法，能够检测图像中的边缘信息
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "图像输入": ("CVIMAGE", {
                    "tooltip": "输入的openCV格式图像"
                }),
                "低阈值": ("INT", {
                    "default": 50,
                    "min": 0,
                    "max": 255,
                    "step": 1,
                    "display": "number",
                    "tooltip": "Canny算法的低阈值，用于连接边缘"
                }),
                "高阈值": ("INT", {
                    "default": 150,
                    "min": 0,
                    "max": 255,
                    "step": 1,
                    "display": "number",
                    "tooltip": "Canny算法的高阈值，用于检测强边缘"
                }),
                "核大小": ([3, 5, 7], {
                    "default": 3,
                    "tooltip": "Sobel算子的核大小，用于计算梯度"
                }),
                "L2梯度": (["否", "是"], {
                    "default": "否",
                    "tooltip": "是否使用L2梯度计算方式（更精确但计算量大）"
                }),
            },
        }

    RETURN_TYPES = ("CVIMAGE",)
    RETURN_NAMES = ("图像输出",)
    OUTPUT_TOOLTIPS = ("Canny边缘检测处理后的图像",)

    def process(self, 图像输入, 低阈值, 高阈值, 核大小, L2梯度):
        try:
            # 检查输入图像
            if 图像输入 is None:
                raise Exception("输入图像为空")
            
            # 转换为灰度图像（如果不是灰度图）
            if len(图像输入.shape) == 3:
                gray = cv2.cvtColor(图像输入, cv2.COLOR_BGR2GRAY)
            else:
                gray = 图像输入.copy()
            
            # 确保高阈值大于低阈值
            if 高阈值 <= 低阈值:
                高阈值 = 低阈值 + 50
                if 高阈值 > 255:
                    高阈值 = 255
                    低阈值 = 205
            
            # 设置L2梯度参数
            use_l2_gradient = True if L2梯度 == "是" else False
            
            # 应用Canny边缘检测
            edges = cv2.Canny(
                gray,
                低阈值,
                高阈值,
                apertureSize=核大小,
                L2gradient=use_l2_gradient
            )
            
            # 转换回3通道图像以保持一致性
            if len(图像输入.shape) == 3:
                edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
            
            return (edges,)
            
        except Exception as e:
            print(f"Canny边缘检测错误: {e}")
            return (图像输入,)