import numpy as np

class ArrayEye:
    '''
    单位矩阵
    创建单位矩阵（对角线为1，其他位置为0的方阵）
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "矩阵大小": ("INT", {
                    "default": 3,
                    "min": 1,
                    "max": 1000,
                    "step": 1,
                    "display": "number",
                    "tooltip": "单位矩阵的大小（N x N）"
                }),
                "列数": ("INT", {
                    "default": -1,
                    "min": -1,
                    "max": 1000,
                    "step": 1,
                    "display": "number",
                    "tooltip": "矩阵的列数，-1表示与行数相同"
                }),
                "对角线偏移": ("INT", {
                    "default": 0,
                    "min": -100,
                    "max": 100,
                    "step": 1,
                    "display": "number",
                    "tooltip": "对角线的偏移量，0为主对角线，正数为上偏移，负数为下偏移"
                }),
                "数据类型": (["float64", "float32", "int64", "int32", "int16", "int8", "uint64", "uint32", "uint16", "uint8", "bool", "complex128", "complex64"], {
                    "default": "float64",
                    "tooltip": "矩阵元素的数据类型"
                }),
            },
        }

    RETURN_TYPES = ("NPARRAY",)
    RETURN_NAMES = ("矩阵输出",)
    OUTPUT_TOOLTIPS = ("创建的单位矩阵",)

    def process(self, 矩阵大小, 列数, 对角线偏移, 数据类型):
        try:
            if 矩阵大小 <= 0:
                raise ValueError("矩阵大小必须大于0")
            
            # 设置列数
            M = None if 列数 <= 0 else 列数
            
            eye_matrix = np.eye(
                矩阵大小, 
                M=M, 
                k=对角线偏移, 
                dtype=数据类型
            )
            
            return (eye_matrix,)
        except ValueError as e:
            raise ValueError(f"单位矩阵创建失败: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"创建单位矩阵时发生未知错误: {str(e)}")