import numpy as np

class ArrayCos:
    '''
    数组余弦函数
    计算数组中每个元素的余弦值
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "输入数组": ("NPARRAY", {
                    "tooltip": "输入数组（弧度制）"
                }),
                "角度单位": (["弧度", "度"], {
                    "default": "弧度",
                    "tooltip": "输入角度的单位"
                }),
            },
        }

    RETURN_TYPES = ("NPARRAY",)
    RETURN_NAMES = ("结果数组",)
    OUTPUT_TOOLTIPS = ("余弦函数的结果数组",)

    def process(self, 输入数组, 角度单位):
        try:
            # 如果输入是度数，转换为弧度
            if 角度单位 == "度":
                input_radians = np.deg2rad(输入数组)
            else:
                input_radians = 输入数组
            
            # 执行余弦运算
            result = np.cos(input_radians)
            return (result,)
        except Exception as e:
            raise RuntimeError(f"余弦运算时发生未知错误: {str(e)}")