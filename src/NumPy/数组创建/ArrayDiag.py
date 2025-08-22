import numpy as np

class ArrayDiag:
    '''
    对角矩阵
    从一维数组创建对角矩阵，或从矩阵中提取对角线元素
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "输入数组": ("NPARRAY", {
                    "tooltip": "输入的NumPy数组"
                }),
                "操作模式": (["创建对角矩阵", "提取对角线"], {
                    "default": "创建对角矩阵",
                    "tooltip": "选择操作模式：从1D数组创建对角矩阵，或从2D矩阵提取对角线"
                }),
                "对角线偏移": ("INT", {
                    "default": 0,
                    "min": -100,
                    "max": 100,
                    "step": 1,
                    "display": "number",
                    "tooltip": "对角线的偏移量，0为主对角线，正数为上偏移，负数为下偏移"
                }),
            },
        }

    RETURN_TYPES = ("NPARRAY",)
    RETURN_NAMES = ("数组输出",)
    OUTPUT_TOOLTIPS = ("创建的对角矩阵或提取的对角线数组",)

    def process(self, 输入数组, 操作模式, 对角线偏移):
        try:
            if not isinstance(输入数组, np.ndarray):
                raise ValueError("输入必须是NumPy数组")
            
            if 操作模式 == "创建对角矩阵":
                # 从1D数组创建对角矩阵
                if 输入数组.ndim != 1:
                    raise ValueError("创建对角矩阵时，输入数组必须是一维数组")
                
                result = np.diag(输入数组, k=对角线偏移)
                
            elif 操作模式 == "提取对角线":
                # 从2D矩阵提取对角线
                if 输入数组.ndim < 2:
                    raise ValueError("提取对角线时，输入数组必须是二维或更高维数组")
                
                result = np.diag(输入数组, k=对角线偏移)
                
            else:
                raise ValueError(f"未知的操作模式: {操作模式}")
            
            return (result,)
            
        except ValueError as e:
            raise ValueError(f"对角矩阵操作失败: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"执行对角矩阵操作时发生未知错误: {str(e)}")