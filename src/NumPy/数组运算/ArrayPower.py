import numpy as np

class ArrayPower:
    '''
    数组幂运算
    对数组进行幂运算
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "底数数组": ("NPARRAY", {
                    "tooltip": "底数数组"
                }),
                "指数数组": ("NPARRAY", {
                    "tooltip": "指数数组"
                }),
            },
        }

    RETURN_TYPES = ("NPARRAY",)
    RETURN_NAMES = ("结果数组",)
    OUTPUT_TOOLTIPS = ("幂运算的结果数组",)

    def process(self, 底数数组, 指数数组):
        try:
            # 执行幂运算
            result = np.power(底数数组, 指数数组)
            return (result,)
        except ValueError as e:
            # 处理形状不匹配等错误
            raise ValueError(f"数组幂运算失败: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"幂运算时发生未知错误: {str(e)}")