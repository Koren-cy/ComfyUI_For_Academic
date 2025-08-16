import cv2

class Gaussian:
    '''
    高斯滤波
    高斯滤波是一种线性平滑滤波，适用于去除高斯噪声
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
                    "step": 2,
                    "display": "number",
                    "tooltip": "高斯核在X方向的大小，必须为奇数，控制水平方向的模糊程度，值越大越模糊"


                }),
                "核大小Y": ("INT", {
                    "default": 5,
                    "min": 1,
                    "max": 99,
                    "step": 2,
                    "display": "number",
                    "tooltip": "高斯核在Y方向的大小，必须为奇数，控制垂直方向的模糊程度，值越大越模糊"

                }),
                "X方向标准差": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 10.0,
                    "step": 0.1,
                    "display": "number",
                    "tooltip": "X方向的高斯核标准差，0表示自动计算，控制水平方向的模糊程度，值越大越模糊"


                }),
                "Y方向标准差": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 10.0,
                    "step": 0.1,
                    "display": "number",
                    "tooltip": "Y方向的高斯核标准差，0表示自动计算，控制垂直方向的模糊程度，值越大越模糊"


                }),
            },
        }

    RETURN_TYPES = ("CVIMAGE",)
    RETURN_NAMES = ("图像输出",)
    OUTPUT_TOOLTIPS = ("高斯滤波处理后的图像",)

    def process(self, 图像输入, 核大小X, 核大小Y, X方向标准差, Y方向标准差):
        try:
            # 检查输入图像
            if 图像输入 is None:
                raise Exception("输入图像为空")
            
            # 确保核大小为奇数
            if 核大小X % 2 == 0:
                核大小X += 1
            if 核大小Y % 2 == 0:
                核大小Y += 1
            
            # 应用高斯滤波
            filtered_image = cv2.GaussianBlur(
                图像输入,
                (核大小X, 核大小Y),
                X方向标准差,
                sigmaY=Y方向标准差
            )
            
            return (filtered_image,)
            
        except Exception as e:
            print(f"高斯滤波错误: {e}")
            return (图像输入,)