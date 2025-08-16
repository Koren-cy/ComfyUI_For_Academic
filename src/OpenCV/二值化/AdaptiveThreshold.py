import cv2

class AdaptiveThreshold:
    '''
    局部自适应阈值二值化
    根据像素邻域的局部特征自动确定阈值，适用于光照不均匀的图像
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "图像输入": ("CVIMAGE", {
                    "tooltip": "输入的openCV格式图像"
                }),
                "最大值": ("INT", {
                    "default": 255,
                    "min": 1,
                    "max": 255,
                    "step": 1,
                    "display": "number",
                    "tooltip": "分配给满足条件的像素值的最大值"
                }),
                "自适应方法": (["均值", "高斯"], {
                    "default": "均值",
                    "tooltip": "自适应阈值算法：均值或高斯"
                }),
                "阈值类型": (["二值化", "反向二值化"], {
                    "default": "二值化",
                    "tooltip": "阈值类型：二值化或反向二值化"
                }),
                "邻域大小": ("INT", {
                    "default": 11,
                    "min": 3,
                    "max": 255,
                    "step": 2,
                    "display": "number",
                    "tooltip": "用于计算阈值的邻域大小，必须为奇数"
                }),
                "常数C": ("FLOAT", {
                    "default": 2.0,
                    "min": -50.0,
                    "max": 50.0,
                    "step": 0.1,
                    "display": "number",
                    "tooltip": "从均值或加权均值中减去的常数"
                }),
            },
        }

    RETURN_TYPES = ("CVIMAGE",)
    RETURN_NAMES = ("图像输出",)
    OUTPUT_TOOLTIPS = ("局部自适应阈值二值化处理后的图像",)

    def process(self, 图像输入, 最大值, 自适应方法, 阈值类型, 邻域大小, 常数C):
        try:
            # 检查输入图像
            if 图像输入 is None:
                raise Exception("输入图像为空")
            
            # 转换为灰度图像（如果不是灰度图）
            if len(图像输入.shape) == 3:
                gray = cv2.cvtColor(图像输入, cv2.COLOR_BGR2GRAY)
            else:
                gray = 图像输入.copy()
            
            # 确保邻域大小为奇数
            if 邻域大小 % 2 == 0:
                邻域大小 += 1
            
            # 设置自适应方法
            if 自适应方法 == "均值":
                adaptive_method = cv2.ADAPTIVE_THRESH_MEAN_C
            else:  # 高斯
                adaptive_method = cv2.ADAPTIVE_THRESH_GAUSSIAN_C
            
            # 设置阈值类型
            if 阈值类型 == "二值化":
                thresh_type = cv2.THRESH_BINARY
            else:  # 反向二进制
                thresh_type = cv2.THRESH_BINARY_INV
            
            # 应用局部自适应阈值二值化
            binary_image = cv2.adaptiveThreshold(
                gray,
                最大值,
                adaptive_method,
                thresh_type,
                邻域大小,
                常数C
            )
            
            # 转换回3通道图像以保持一致性
            if len(图像输入.shape) == 3:
                binary_image = cv2.cvtColor(binary_image, cv2.COLOR_GRAY2BGR)
            
            return (binary_image,)
            
        except Exception as e:
            print(f"局部自适应阈值二值化错误: {e}")
            return (图像输入,)