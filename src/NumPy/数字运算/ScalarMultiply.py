import numpy as np
import sys

class ScalarMultiply:
    '''
    标量乘法
    对数组与标量进行乘法运算
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "输入数组": ("NPARRAY", {
                    "tooltip": "输入数组"
                }),
                "标量值": ("FLOAT", {
                    "default": 2.0,
                    "min": -float(sys.maxsize),
                    "max": float(sys.maxsize),
                    "step": 0.001,
                    "display": "number",
                    "tooltip": "要与数组相乘的标量值"
                }),
                "运算模式": (["数组×标量", "标量×数组"], {
                    "default": "数组×标量",
                    "tooltip": "运算模式：数组×标量 或 标量×数组（结果相同，仅为语义区分）"
                }),
            },
        }

    RETURN_TYPES = ("NPARRAY",)
    RETURN_NAMES = ("结果数组",)
    OUTPUT_TOOLTIPS = ("标量乘法运算的结果数组",)

    def process(self, 输入数组, 标量值, 运算模式):
        try:
            # 执行标量乘法运算
            if 运算模式 == "数组×标量":
                result = np.multiply(输入数组, 标量值)
            else:  # 标量×数组
                result = np.multiply(标量值, 输入数组)
            
            return (result,)
        except ValueError as e:
            # 处理数值错误
            raise ValueError(f"标量乘法运算失败: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"标量乘法运算时发生未知错误: {str(e)}")