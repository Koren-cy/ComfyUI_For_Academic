import numpy as np

class ArrayAdd:
    '''
    数组加法
    对两个数组进行逐元素加法运算
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
    OUTPUT_TOOLTIPS = ("加法运算的结果数组",)

    def process(self, 数组A, 数组B):
        try:
            # 执行加法运算
            result = np.add(数组A, 数组B)
            return (result,)
        except ValueError as e:
            # 处理形状不匹配等错误
            raise ValueError(f"数组加法运算失败: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"加法运算时发生未知错误: {str(e)}")