import cv2

class Threshold:
    '''
    二值化
    使用固定阈值对图像进行二值化处理，将像素值分为两个类别
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "图像输入": ("CVIMAGE", {
                    "tooltip": "输入的openCV格式图像"
                }),
                "阈值": ("INT", {
                    "default": 127,
                    "min": 0,
                    "max": 255,
                    "step": 1,
                    "display": "number",
                    "tooltip": "二值化的阈值，像素值大于此值的设为最大值，否则设为0"
                }),
                "最大值": ("INT", {
                    "default": 255,
                    "min": 1,
                    "max": 255,
                    "step": 1,
                    "display": "number",
                    "tooltip": "分配给满足条件的像素值的最大值"
                }),
                "阈值类型": (["二值化", "反向二值化", "截断", "阈值归零", "反向阈值归零"], {
                    "default": "二值化",
                    "tooltip": "阈值处理类型：二值化、反向二值化、截断（大于阈值的设为阈值）、阈值归零（小于阈值归零）、反向阈值归零（大于阈值归零）"
                }),
            },
        }

    RETURN_TYPES = ("CVIMAGE",)
    RETURN_NAMES = ("图像输出",)
    OUTPUT_TOOLTIPS = ("一般二值化处理后的图像",)

    def process(self, 图像输入, 阈值, 最大值, 阈值类型):
        try:
            # 检查输入图像
            if 图像输入 is None:
                raise Exception("输入图像为空")
            
            # 转换为灰度图像（如果不是灰度图）
            if len(图像输入.shape) == 3:
                gray = cv2.cvtColor(图像输入, cv2.COLOR_BGR2GRAY)
            else:
                gray = 图像输入.copy()
            
            # 设置阈值类型
            if 阈值类型 == "二值化":
                thresh_type = cv2.THRESH_BINARY
            elif 阈值类型 == "反向二值化":
                thresh_type = cv2.THRESH_BINARY_INV
            elif 阈值类型 == "截断":
                thresh_type = cv2.THRESH_TRUNC
            elif 阈值类型 == "阈值归零":
                thresh_type = cv2.THRESH_TOZERO
            else:  # 反向阈值归零
                thresh_type = cv2.THRESH_TOZERO_INV
            
            # 应用一般二值化
            ret_val, binary_image = cv2.threshold(
                gray,
                阈值,
                最大值,
                thresh_type
            )
            
            # 转换回3通道图像以保持一致性
            if len(图像输入.shape) == 3:
                binary_image = cv2.cvtColor(binary_image, cv2.COLOR_GRAY2BGR)
            
            return (binary_image,)
            
        except Exception as e:
            print(f"一般二值化错误: {e}")
            return (图像输入,)