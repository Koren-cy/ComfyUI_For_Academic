import numpy as np
import sys

class ArrayArange:
    '''
    等差数列数组
    创建指定范围和步长的等差数列数组
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "起始值": ("FLOAT", {
                    "default": 0.0,
                    "min": -float(sys.maxsize),
                    "max": float(sys.maxsize),
                    "step": 0.001,
                    "display": "number",
                    "tooltip": "数列的起始值"
                }),
                "结束值": ("FLOAT", {
                    "default": 10.0,
                    "min": -float(sys.maxsize),
                    "max": float(sys.maxsize),
                    "step": 0.001,
                    "display": "number",
                    "tooltip": "数列的结束值（不包含）"
                }),
                "步长": ("FLOAT", {
                    "default": 1.0,
                    "min": -float(sys.maxsize),
                    "max": float(sys.maxsize),
                    "step": 0.001,
                    "display": "number",
                    "tooltip": "数列的步长"
                }),
                "数据类型": (["float64", "float32", "int64", "int32", "int16", "int8", "uint64", "uint32", "uint16", "uint8", "bool", "complex128", "complex64"], {
                    "default": "float64",
                    "tooltip": "数组元素的数据类型"
                }),
            },
        }

    RETURN_TYPES = ("NPARRAY",)
    RETURN_NAMES = ("数组输出",)
    OUTPUT_TOOLTIPS = ("创建的等差数列数组",)

    def process(self, 起始值, 结束值, 步长, 数据类型):
        try:
            if 步长 <= 0:
                raise ValueError("步长必须大于0")
            
            if 起始值 >= 结束值 and 步长 > 0:
                print(f"警告: 起始值({起始值})大于等于结束值({结束值})，将返回空数组")
                return (np.array([], dtype=数据类型),)
            
            arange_array = np.arange(起始值, 结束值, 步长, dtype=数据类型)
            
            return (arange_array,)
        except ValueError as e:
            raise ValueError(f"等差数列数组创建失败: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"创建等差数列数组时发生未知错误: {str(e)}")