import numpy as np

class ArrayMultiply:
    '''
    数组乘法
    对两个数组进行逐元素乘法运算
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "数组A": ("NPARRAY", {
                    "tooltip": "第一个输入数组"
                }),
                "数组B": ("NPARRAY", {
                    "tooltip": "第二个输入数组"
                }),
            },
        }

    RETURN_TYPES = ("NPARRAY",)
    RETURN_NAMES = ("结果数组",)
    OUTPUT_TOOLTIPS = ("乘法运算的结果数组",)

    def process(self, 数组A, 数组B):
        try:
            # 执行乘法运算
            result = np.multiply(数组A, 数组B)
            return (result,)
        except ValueError as e:
            # 处理形状不匹配等错误
            raise ValueError(f"数组乘法运算失败: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"乘法运算时发生未知错误: {str(e)}")