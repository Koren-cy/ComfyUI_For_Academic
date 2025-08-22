import numpy as np
import sys

class ScalarPower:
    '''
    标量幂运算
    对数组与标量进行幂运算
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
                    "tooltip": "幂运算的指数或底数"
                }),
                "运算模式": (["数组^标量", "标量^数组"], {
                    "default": "数组^标量",
                    "tooltip": "运算模式：数组^标量(数组的标量次幂) 或 标量^数组(标量的数组次幂)"
                }),
                "处理负数开方": (["警告", "忽略", "错误"], {
                    "default": "警告",
                    "tooltip": "负数开方处理方式：警告(返回复数)、忽略(静默返回复数)、错误(抛出异常)"
                }),
            },
        }

    RETURN_TYPES = ("NPARRAY",)
    RETURN_NAMES = ("结果数组",)
    OUTPUT_TOOLTIPS = ("标量幂运算的结果数组",)

    def process(self, 输入数组, 标量值, 运算模式, 处理负数开方):
        try:
            # 设置无效值处理方式
            if 处理负数开方 == "错误":
                old_settings = np.seterr(invalid='raise')
            elif 处理负数开方 == "警告":
                old_settings = np.seterr(invalid='warn')
            else:  # 忽略
                old_settings = np.seterr(invalid='ignore')
            
            try:
                # 执行标量幂运算
                if 运算模式 == "数组^标量":
                    # 检查负数开方情况
                    if (标量值 < 1 and 标量值 > 0 and 
                        处理负数开方 == "错误" and np.any(输入数组 < 0)):
                        raise ValueError("负数不能进行分数次幂运算")
                    result = np.power(输入数组, 标量值)
                else:  # 标量^数组
                    # 检查负底数情况
                    if (标量值 < 0 and 处理负数开方 == "错误" and 
                        np.any((输入数组 % 1) != 0)):
                        raise ValueError("负数底数不能进行非整数次幂运算")
                    result = np.power(标量值, 输入数组)
                
                return (result,)
            finally:
                # 恢复原始设置
                np.seterr(**old_settings)
                
        except ValueError as e:
            # 处理数值错误
            raise ValueError(f"标量幂运算失败: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"标量幂运算时发生未知错误: {str(e)}")