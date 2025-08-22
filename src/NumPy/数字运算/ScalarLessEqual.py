import numpy as np
import sys

class ScalarLessEqual:
    '''
    标量小于等于比较
    对数组与标量进行小于等于比较运算
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "输入数组": ("NPARRAY", {
                    "tooltip": "输入数组"
                }),
                "标量值": ("FLOAT", {
                    "default": 0.0,
                    "min": -float(sys.maxsize),
                    "max": float(sys.maxsize),
                    "step": 0.001,
                    "display": "number",
                    "tooltip": "要比较的标量值"
                }),
                "运算模式": (["数组<=标量", "标量<=数组"], {
                    "default": "数组<=标量",
                    "tooltip": "运算模式：数组<=标量(数组元素小于等于标量) 或 标量<=数组(标量小于等于数组元素)"
                }),
            },
        }

    RETURN_TYPES = ("NPARRAY",)
    RETURN_NAMES = ("结果数组",)
    OUTPUT_TOOLTIPS = ("布尔类型的比较结果数组",)

    def process(self, 输入数组, 标量值, 运算模式):
        try:
            # 执行标量小于等于比较运算
            if 运算模式 == "数组<=标量":
                result = np.less_equal(输入数组, 标量值)
            else:  # 标量<=数组
                result = np.less_equal(标量值, 输入数组)
            
            return (result,)
        except ValueError as e:
            # 处理数值错误
            raise ValueError(f"标量小于等于比较运算失败: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"标量小于等于比较运算时发生未知错误: {str(e)}")