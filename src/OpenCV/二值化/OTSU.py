import cv2

class OTSU:
    '''
    OTSU自适应二值化
    使用OTSU算法根据直方图，自动确定最佳阈值进行二值化处理
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "图像输入": ("CVIMAGE", {
                    "tooltip": "输入的openCV格式图像"
                }),
                "反转": (["否", "是"], {
                    "default": "否",
                    "tooltip": "是否反转二值化结果（黑白互换）"
                }),
            },
        }

    RETURN_TYPES = ("CVIMAGE",)
    RETURN_NAMES = ("图像输出",)
    OUTPUT_TOOLTIPS = ("OTSU二值化处理后的图像",)

    def process(self, 图像输入, 反转):
        try:
            # 检查输入图像
            if 图像输入 is None:
                raise Exception("输入图像为空")
            
            # 转换为灰度图像（如果不是灰度图）
            if len(图像输入.shape) == 3:
                gray = cv2.cvtColor(图像输入, cv2.COLOR_BGR2GRAY)
            else:
                gray = 图像输入.copy()
            
            # 应用OTSU二值化
            if 反转 == "是":
                # 反转二值化：背景变白，前景变黑
                threshold_value, binary_image = cv2.threshold(
                    gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
                )
            else:
                # 正常二值化：背景变黑，前景变白
                threshold_value, binary_image = cv2.threshold(
                    gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
                )
            
            # 转换回3通道图像以保持一致性
            if len(图像输入.shape) == 3:
                binary_image = cv2.cvtColor(binary_image, cv2.COLOR_GRAY2BGR)
            
            return (binary_image,)
            
        except Exception as e:
            print(f"OTSU二值化错误: {e}")
            return (图像输入,)