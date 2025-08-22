import numpy as np

class ArraySubtract:
    '''
    数组减法
    对两个数组进行逐元素减法运算
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "数组A": ("NPARRAY", {
                    "tooltip": "被减数数组"
                }),
                "数组B": ("NPARRAY", {
                    "tooltip": "减数数组"
                }),
            },
        }

    RETURN_TYPES = ("NPARRAY",)
    RETURN_NAMES = ("结果数组",)
    OUTPUT_TOOLTIPS = ("减法运算的结果数组",)

    def process(self, 数组A, 数组B):
        try:
            # 执行减法运算
            result = np.subtract(数组A, 数组B)
            return (result,)
        except ValueError as e:
            # 处理形状不匹配等错误
            raise ValueError(f"数组减法运算失败: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"减法运算时发生未知错误: {str(e)}")