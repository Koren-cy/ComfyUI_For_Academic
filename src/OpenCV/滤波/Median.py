import cv2

class Median:
    '''
    中值滤波
    中值滤波是一种非线性滤波技术，特别适用于去除椒盐噪声
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "图像输入": ("CVIMAGE", {
                    "tooltip": "输入的openCV格式图像"
                }),
                "核大小": ("INT", {
                    "default": 5,
                    "min": 3,
                    "max": 99,
                    "step": 2,
                    "display": "number",
                    "tooltip": "中值滤波核的大小，必须为奇数。值越大，滤波效果越强"
                }),
            },
        }

    RETURN_TYPES = ("CVIMAGE",)
    RETURN_NAMES = ("图像输出",)
    OUTPUT_TOOLTIPS = ("中值滤波处理后的图像",)

    def process(self, 图像输入, 核大小):
        try:
            # 检查输入图像
            if 图像输入 is None:
                raise Exception("输入图像为空")
            
            # 确保核大小为奇数
            if 核大小 % 2 == 0:
                核大小 += 1
            
            # 应用中值滤波
            filtered_image = cv2.medianBlur(
                图像输入,
                核大小
            )
            
            return (filtered_image,)
            
        except Exception as e:
            print(f"中值滤波错误: {e}")
            return (图像输入,)