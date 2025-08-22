import numpy as np

class MatrixInverse:
    '''
    矩阵求逆
    计算方阵的逆矩阵
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "输入矩阵": ("NPARRAY", {
                    "tooltip": "要求逆的方阵（必须是可逆的方阵）"
                }),
            },
            "optional": {
                "检查条件数": (["是", "否"], {
                    "default": "是",
                    "tooltip": "是否检查矩阵的条件数以评估数值稳定性"
                }),
                "条件数阈值": ("FLOAT", {
                    "default": 1e12,
                    "min": 1.0,
                    "max": 1e16,
                    "step": 1e6,
                    "display": "number",
                    "tooltip": "条件数阈值，超过此值将发出警告"
                }),
            },
        }

    RETURN_TYPES = ("NPARRAY", "FLOAT")
    RETURN_NAMES = ("逆矩阵", "条件数")
    OUTPUT_TOOLTIPS = ("计算得到的逆矩阵", "矩阵的条件数（数值稳定性指标）")

    def process(self, 输入矩阵, 检查条件数="是", 条件数阈值=1e12):
        try:
            # 检查输入是否为方阵
            if 输入矩阵.ndim != 2:
                raise ValueError("输入必须是二维矩阵")
            
            if 输入矩阵.shape[0] != 输入矩阵.shape[1]:
                raise ValueError(f"输入必须是方阵，当前形状为 {输入矩阵.shape}")
            
            # 检查矩阵是否为空
            if 输入矩阵.size == 0:
                raise ValueError("输入矩阵不能为空")
            
            # 计算条件数（如果需要）
            condition_number = None
            if 检查条件数 == "是":
                try:
                    condition_number = np.linalg.cond(输入矩阵)
                    if condition_number > 条件数阈值:
                        print(f"警告：矩阵条件数 {condition_number:.2e} 较大，可能导致数值不稳定")
                except Exception:
                    condition_number = float('inf')
                    print("警告：无法计算条件数，矩阵可能接近奇异")
            else:
                condition_number = 0.0
            
            # 计算逆矩阵
            try:
                inverse_matrix = np.linalg.inv(输入矩阵)
            except np.linalg.LinAlgError as e:
                if "Singular matrix" in str(e):
                    raise ValueError("矩阵是奇异的（不可逆），无法计算逆矩阵")
                else:
                    raise ValueError(f"矩阵求逆失败: {str(e)}")
            
            # 验证逆矩阵的正确性（可选的数值验证）
            if 输入矩阵.shape[0] <= 100:  # 只对小矩阵进行验证以避免性能问题
                try:
                    identity_check = np.matmul(输入矩阵, inverse_matrix)
                    identity_expected = np.eye(输入矩阵.shape[0])
                    max_error = np.max(np.abs(identity_check - identity_expected))
                    if max_error > 1e-10:
                        print(f"警告：逆矩阵验证误差较大 ({max_error:.2e})，结果可能不准确")
                except Exception:
                    pass  # 验证失败不影响主要功能
            
            return (inverse_matrix, condition_number)
            
        except ValueError as e:
            raise ValueError(f"矩阵求逆失败: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"矩阵求逆运算时发生未知错误: {str(e)}")