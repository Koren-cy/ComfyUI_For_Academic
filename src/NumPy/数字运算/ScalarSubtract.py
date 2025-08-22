import numpy as np
import sys

class ScalarSubtract:
    '''
    标量减法
    对数组与标量进行减法运算
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "输入数组": ("NPARRAY", {
                    "tooltip": "输入数组"
                }),
                "标量值": ("FLOAT", {
                    "default": 1.0,
                    "min": -float(sys.maxsize),
                    "max": float(sys.maxsize),
                    "step": 0.001,
                    "display": "number",
                    "tooltip": "要与数组相减的标量值"
                }),
                "运算模式": (["数组-标量", "标量-数组"], {
                    "default": "数组-标量",
                    "tooltip": "运算模式：数组-标量 或 标量-数组（结果不同）"
                }),
            },
        }

    RETURN_TYPES = ("NPARRAY",)
    RETURN_NAMES = ("结果数组",)
    OUTPUT_TOOLTIPS = ("标量减法运算的结果数组",)

    def process(self, 输入数组, 标量值, 运算模式):
        try:
            # 执行标量减法运算
            if 运算模式 == "数组-标量":
                result = np.subtract(输入数组, 标量值)
            else:  # 标量-数组
                result = np.subtract(标量值, 输入数组)
            
            return (result,)
        except ValueError as e:
            # 处理数值错误
            raise ValueError(f"标量减法运算失败: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"标量减法运算时发生未知错误: {str(e)}")