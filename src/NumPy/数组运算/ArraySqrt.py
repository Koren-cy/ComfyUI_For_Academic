import numpy as np

class ArraySqrt:
    '''
    数组平方根
    计算数组中每个元素的平方根
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "输入数组": ("NPARRAY", {
                    "tooltip": "输入数组"
                }),
                "处理负数": (["忽略", "警告", "错误"], {
                    "default": "警告",
                    "tooltip": "遇到负数时的处理方式"
                }),
            },
        }

    RETURN_TYPES = ("NPARRAY",)
    RETURN_NAMES = ("结果数组",)
    OUTPUT_TOOLTIPS = ("平方根运算的结果数组",)

    def process(self, 输入数组, 处理负数):
        try:
            # 设置负数处理方式
            if 处理负数 == "忽略":
                with np.errstate(invalid='ignore'):
                    result = np.sqrt(输入数组)
            elif 处理负数 == "警告":
                with np.errstate(invalid='warn'):
                    result = np.sqrt(输入数组)
            else:  # 错误
                with np.errstate(invalid='raise'):
                    result = np.sqrt(输入数组)
            
            return (result,)
        except ValueError as e:
            raise ValueError(f"数组平方根运算失败: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"平方根运算时发生未知错误: {str(e)}")