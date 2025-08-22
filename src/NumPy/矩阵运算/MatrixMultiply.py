import numpy as np

class MatrixMultiply:
    '''
    矩阵乘法
    执行矩阵与矩阵或矩阵与向量的乘法运算
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "矩阵A": ("NPARRAY", {
                    "tooltip": "第一个输入矩阵或向量"
                }),
                "矩阵B": ("NPARRAY", {
                    "tooltip": "第二个输入矩阵或向量"
                }),
            },
        }

    RETURN_TYPES = ("NPARRAY",)
    RETURN_NAMES = ("结果矩阵",)
    OUTPUT_TOOLTIPS = ("矩阵乘法运算的结果",)

    def process(self, 矩阵A, 矩阵B):
        try:
            # 检查输入维度
            if 矩阵A.ndim == 0 or 矩阵B.ndim == 0:
                raise ValueError("输入不能是标量，请使用数组或矩阵")
            
            # 执行矩阵乘法
            result = np.matmul(矩阵A, 矩阵B)
            
            return (result,)
        except ValueError as e:
            # 处理维度不匹配等错误
            if "matmul" in str(e) or "shapes" in str(e):
                raise ValueError(f"矩阵乘法失败：矩阵维度不匹配。矩阵A形状: {矩阵A.shape}, 矩阵B形状: {矩阵B.shape}")
            else:
                raise ValueError(f"矩阵乘法失败: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"矩阵乘法运算时发生未知错误: {str(e)}")