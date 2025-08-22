import numpy as np
import sys

class ScalarDivide:
    '''
    标量除法
    对数组与标量进行除法运算
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
                    "tooltip": "要与数组相除的标量值"
                }),
                "运算模式": (["数组÷标量", "标量÷数组"], {
                    "default": "数组÷标量",
                    "tooltip": "运算模式：数组÷标量 或 标量÷数组（结果不同）"
                }),
                "处理除零": (["警告", "忽略", "错误"], {
                    "default": "警告",
                    "tooltip": "除零处理方式：警告(返回inf/nan)、忽略(静默返回inf/nan)、错误(抛出异常)"
                }),
            },
        }

    RETURN_TYPES = ("NPARRAY",)
    RETURN_NAMES = ("结果数组",)
    OUTPUT_TOOLTIPS = ("标量除法运算的结果数组",)

    def process(self, 输入数组, 标量值, 运算模式, 处理除零):
        try:
            # 设置除零处理方式
            if 处理除零 == "错误":
                old_settings = np.seterr(divide='raise', invalid='raise')
            elif 处理除零 == "警告":
                old_settings = np.seterr(divide='warn', invalid='warn')
            else:  # 忽略
                old_settings = np.seterr(divide='ignore', invalid='ignore')
            
            try:
                # 执行标量除法运算
                if 运算模式 == "数组÷标量":
                    if 标量值 == 0 and 处理除零 == "错误":
                        raise ValueError("除数不能为零")
                    result = np.divide(输入数组, 标量值)
                else:  # 标量÷数组
                    # 检查数组中是否有零元素
                    if 处理除零 == "错误" and np.any(输入数组 == 0):
                        raise ValueError("数组中包含零元素，无法作为除数")
                    result = np.divide(标量值, 输入数组)
                
                return (result,)
            finally:
                # 恢复原始设置
                np.seterr(**old_settings)
                
        except ValueError as e:
            # 处理数值错误
            raise ValueError(f"标量除法运算失败: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"标量除法运算时发生未知错误: {str(e)}")