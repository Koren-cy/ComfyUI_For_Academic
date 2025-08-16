import cv2

class Morphology:
    '''
    形态学操作
    提供完整的形态学操作功能，包括腐蚀、膨胀、开运算、闭运算、形态学梯度、顶帽、黑帽
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "图像输入": ("CVIMAGE", {
                    "tooltip": "输入的openCV格式图像"
                }),
                "操作类型": (["腐蚀", "膨胀", "开运算", "闭运算", "形态学梯度", "顶帽", "黑帽"], {
                    "default": "开运算",
                    "tooltip": "选择要执行的形态学操作类型\n"
                               "腐蚀：移除图像中的小物体,平滑边界,断开连接的物体\n"
                               "膨胀：填充图像中的小孔,连接断开的物体,增强物体区域\n"
                               "开运算：先腐蚀再膨胀,移除小物体,保留大物体,平滑边界\n"
                               "闭运算：先膨胀再腐蚀,填充小孔,保留大物体,平滑边界\n"
                               "形态学梯度：膨胀减去腐蚀,提取物体轮廓,保留物体结构\n"
                               "顶帽：原始图像减去开运算,突出小物体,增强细节\n"
                               "黑帽：闭运算减去原始图像,突出暗细节,增强暗区域"
                }),
                "核形状": (["矩形", "椭圆", "十字"], {
                    "default": "矩形",
                    "tooltip": "形态学操作的结构元素形状\n"
                               "椭圆核：平滑边缘,圆形对象,平滑效果\n"
                               "矩形核：保留物体边界,线性结构,强烈效果\n"
                               "十字核：突出物体内部细节,水平/垂直处理"
                }),
                "核大小": ("INT", {
                    "default": 5,
                    "min": 3,
                    "max": 27,
                    "step": 2,
                    "display": "number",
                    "tooltip": "结构元素的大小，必须为奇数"
                }),
                "迭代次数": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 30,
                    "step": 1,
                    "display": "number",
                    "tooltip": "形态学操作的迭代次数"
                }),
            },
        }

    RETURN_TYPES = ("CVIMAGE",)
    RETURN_NAMES = ("图像输出",)
    OUTPUT_TOOLTIPS = ("形态学操作处理后的图像",)

    def process(self, 图像输入, 操作类型, 核形状, 核大小, 迭代次数):
        try:
            # 检查输入图像
            if 图像输入 is None:
                raise Exception("输入图像为空")
            
            # 确保核大小为奇数
            if 核大小 % 2 == 0:
                核大小 += 1
            
            # 根据形状创建结构元素
            if 核形状 == "矩形":
                kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (核大小, 核大小))
            elif 核形状 == "椭圆":
                kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (核大小, 核大小))
            else:  # 十字
                kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (核大小, 核大小))
            
            # 根据操作类型执行相应的形态学操作
            if 操作类型 == "腐蚀":
                result_image = cv2.erode(图像输入, kernel, iterations=迭代次数)
            elif 操作类型 == "膨胀":
                result_image = cv2.dilate(图像输入, kernel, iterations=迭代次数)
            elif 操作类型 == "开运算":
                result_image = cv2.morphologyEx(图像输入, cv2.MORPH_OPEN, kernel, iterations=迭代次数)
            elif 操作类型 == "闭运算":
                result_image = cv2.morphologyEx(图像输入, cv2.MORPH_CLOSE, kernel, iterations=迭代次数)
            elif 操作类型 == "形态学梯度":
                result_image = cv2.morphologyEx(图像输入, cv2.MORPH_GRADIENT, kernel, iterations=迭代次数)
            elif 操作类型 == "顶帽":
                result_image = cv2.morphologyEx(图像输入, cv2.MORPH_TOPHAT, kernel, iterations=迭代次数)
            elif 操作类型 == "黑帽":
                result_image = cv2.morphologyEx(图像输入, cv2.MORPH_BLACKHAT, kernel, iterations=迭代次数)
            else:
                # 默认使用开运算
                result_image = cv2.morphologyEx(图像输入, cv2.MORPH_OPEN, kernel, iterations=迭代次数)
            
            return (result_image,)
            
        except Exception as e:
            print(f"形态学操作错误: {e}")
            return (图像输入,)