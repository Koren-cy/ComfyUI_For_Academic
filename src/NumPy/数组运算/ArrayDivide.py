import numpy as np

class ArrayDivide:
    '''
    数组除法
    对两个数组进行逐元素除法运算
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "数组A": ("NPARRAY", {
                    "tooltip": "被除数数组"
                }),
                "数组B": ("NPARRAY", {
                    "tooltip": "除数数组"
                }),
                "处理零除": (["忽略", "警告", "错误"], {
                    "default": "警告",
                    "tooltip": "遇到零除时的处理方式"
                }),
            },
        }

    RETURN_TYPES = ("NPARRAY",)
    RETURN_NAMES = ("结果数组",)
    OUTPUT_TOOLTIPS = ("除法运算的结果数组",)

    def process(self, 数组A, 数组B, 处理零除):
        try:
            # 设置零除处理方式
            if 处理零除 == "忽略":
                with np.errstate(divide='ignore', invalid='ignore'):
                    result = np.divide(数组A, 数组B)
            elif 处理零除 == "警告":
                with np.errstate(divide='warn', invalid='warn'):
                    result = np.divide(数组A, 数组B)
            else:  # 错误
                with np.errstate(divide='raise', invalid='raise'):
                    result = np.divide(数组A, 数组B)
            
            return (result,)
        except ValueError as e:
            # 处理形状不匹配等错误
            raise ValueError(f"数组除法运算失败: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"除法运算时发生未知错误: {str(e)}")