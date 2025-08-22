import numpy as np

class ArrayAbs:
    '''
    数组绝对值
    计算数组中每个元素的绝对值
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "输入数组": ("NPARRAY", {
                    "tooltip": "输入数组"
                }),
            },
        }

    RETURN_TYPES = ("NPARRAY",)
    RETURN_NAMES = ("结果数组",)
    OUTPUT_TOOLTIPS = ("绝对值运算的结果数组",)

    def process(self, 输入数组):
        try:
            # 执行绝对值运算
            result = np.abs(输入数组)
            return (result,)
        except Exception as e:
            raise RuntimeError(f"绝对值运算时发生未知错误: {str(e)}")