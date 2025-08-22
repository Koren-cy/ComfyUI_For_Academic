import numpy as np
import sys

class ArrayLinspace:
    '''
    等差数组
    在指定区间内创建等间距的数组
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
                    "tooltip": "数列的结束值（包含）"
                }),
                "元素个数": ("INT", {
                    "default": 50,
                    "min": 1,
                    "max": int(sys.maxsize),
                    "step": 1,
                    "display": "number",
                    "tooltip": "生成数组的元素个数"
                }),
                "包含结束值": (["是", "否"], {
                    "default": "是",
                    "tooltip": "是否包含结束值"
                }),
                "数据类型": (["float64", "float32", "int64", "int32", "int16", "int8", "uint64", "uint32", "uint16", "uint8", "bool", "complex128", "complex64"], {
                    "default": "float64",
                    "tooltip": "数组元素的数据类型"
                }),
            },
        }

    RETURN_TYPES = ("NPARRAY",)
    RETURN_NAMES = ("数组输出",)
    OUTPUT_TOOLTIPS = ("创建的线性等分数组",)

    def process(self, 起始值, 结束值, 元素个数, 包含结束值, 数据类型):
        try:
            if 元素个数 <= 0:
                raise ValueError("元素个数必须大于0")
            
            # 设置是否包含结束值
            endpoint = True if 包含结束值 == "是" else False
            
            linspace_array = np.linspace(
                起始值, 
                结束值, 
                元素个数, 
                endpoint=endpoint, 
                dtype=数据类型
            )
            
            return (linspace_array,)
        except ValueError as e:
            raise ValueError(f"线性等分数组创建失败: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"创建线性等分数组时发生未知错误: {str(e)}")