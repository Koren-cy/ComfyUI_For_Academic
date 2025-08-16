import cv2

class Bilateral:
    '''
    双边滤波
    双边滤波是一种非线性滤波技术，能够在平滑图像的同时保持边缘信息
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "图像输入": ("CVIMAGE", {
                    "tooltip": "输入的openCV格式图像"
                }),
                "滤波直径": ("INT", {
                    "default": 9,
                    "min": 3,
                    "max": 50,
                    "step": 2,
                    "display": "number",
                    "tooltip": "滤波器的直径，必须为奇数。值越大，滤波效果越强"
                }),
                "颜色标准差": ("FLOAT", {
                    "default": 75.0,
                    "min": 1.0,
                    "max": 200.0,
                    "step": 1.0,
                    "display": "number",
                    "tooltip": "颜色空间的标准差，值越大，颜色差异越大的像素会被平均"
                }),
                "空间标准差": ("FLOAT", {
                    "default": 75.0,
                    "min": 1.0,
                    "max": 200.0,
                    "step": 1.0,
                    "display": "number",
                    "tooltip": "坐标空间的标准差，值越大，距离越远的像素会相互影响"
                }),
            },
        }

    RETURN_TYPES = ("CVIMAGE",)
    RETURN_NAMES = ("图像输出",)
    OUTPUT_TOOLTIPS = ("双边滤波处理后的图像",)

    def process(self, 图像输入, 滤波直径, 颜色标准差, 空间标准差):
        try:
            # 检查输入图像
            if 图像输入 is None:
                raise Exception("输入图像为空")
            
            # 确保滤波直径为奇数
            if 滤波直径 % 2 == 0:
                滤波直径 += 1
            
            # 应用双边滤波
            filtered_image = cv2.bilateralFilter(
                图像输入, 
                滤波直径, 
                颜色标准差, 
                空间标准差
            )
            
            return (filtered_image,)
            
        except Exception as e:
            print(f"双边滤波错误: {e}")
            return (图像输入,)