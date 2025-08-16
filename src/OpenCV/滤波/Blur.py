import cv2

class Blur:
    '''
    均值滤波
    均值滤波是一种线性滤波技术，通过计算邻域像素的平均值来平滑图像
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "图像输入": ("CVIMAGE", {
                    "tooltip": "输入的openCV格式图像"
                }),
                "核大小X": ("INT", {
                    "default": 5,
                    "min": 1,
                    "max": 99,
                    "step": 1,
                    "display": "number",
                    "tooltip": "均值滤波核在X方向的大小"
                }),
                "核大小Y": ("INT", {
                    "default": 5,
                    "min": 1,
                    "max": 99,
                    "step": 1,
                    "display": "number",
                    "tooltip": "均值滤波核在Y方向的大小"
                }),
            },
        }

    RETURN_TYPES = ("CVIMAGE",)
    RETURN_NAMES = ("图像输出",)
    OUTPUT_TOOLTIPS = ("均值滤波处理后的图像",)

    def process(self, 图像输入, 核大小X, 核大小Y):
        try:
            # 检查输入图像
            if 图像输入 is None:
                raise Exception("输入图像为空")
            
            # 应用均值滤波
            filtered_image = cv2.blur(
                图像输入,
                (核大小X, 核大小Y)
            )
            
            return (filtered_image,)
            
        except Exception as e:
            print(f"均值滤波错误: {e}")
            return (图像输入,)