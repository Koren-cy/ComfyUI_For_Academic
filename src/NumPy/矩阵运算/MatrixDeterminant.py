import numpy as np

class MatrixDeterminant:
    '''
    矩阵行列式
    计算方阵的行列式值
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "输入矩阵": ("NPARRAY", {
                    "tooltip": "要计算行列式的方阵"
                }),
            },
            "optional": {
                "输出格式": (["标量", "数组"], {
                    "default": "标量",
                    "tooltip": "输出格式：标量(单个数值) 或 数组(包装为数组)"
                }),
            },
        }

    RETURN_TYPES = ("NPARRAY", "STRING")
    RETURN_NAMES = ("行列式值", "矩阵性质")
    OUTPUT_TOOLTIPS = ("计算得到的行列式值", "基于行列式值的矩阵性质描述")

    def process(self, 输入矩阵, 输出格式="标量"):
        try:
            # 检查输入是否为方阵
            if 输入矩阵.ndim != 2:
                raise ValueError("输入必须是二维矩阵")
            
            if 输入矩阵.shape[0] != 输入矩阵.shape[1]:
                raise ValueError(f"输入必须是方阵，当前形状为 {输入矩阵.shape}")
            
            # 检查矩阵是否为空
            if 输入矩阵.size == 0:
                raise ValueError("输入矩阵不能为空")
            
            # 计算行列式
            det_value = np.linalg.det(输入矩阵)
            
            # 根据输出格式处理结果
            if 输出格式 == "标量":
                result = np.array(det_value)
            else:  # 数组格式
                result = np.array([det_value])
            
            # 分析矩阵性质
            matrix_properties = self._analyze_matrix_properties(det_value, 输入矩阵.shape[0])
            
            return (result, matrix_properties)
            
        except ValueError as e:
            raise ValueError(f"行列式计算失败: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"行列式计算时发生未知错误: {str(e)}")
    
    def _analyze_matrix_properties(self, det_value, matrix_size):
        """基于行列式值分析矩阵性质"""
        properties = []
        
        # 行列式值的基本信息
        properties.append(f"行列式值: {det_value:.6e}")
        
        # 判断矩阵的可逆性
        if abs(det_value) < 1e-12:
            properties.append("矩阵性质: 奇异矩阵（不可逆）")
            properties.append("线性相关: 行/列向量线性相关")
        else:
            properties.append("矩阵性质: 非奇异矩阵（可逆）")
            properties.append("线性相关: 行/列向量线性无关")
        
        # 行列式的符号意义
        if det_value > 0:
            properties.append("符号: 正值（保持定向）")
        elif det_value < 0:
            properties.append("符号: 负值（改变定向）")
        else:
            properties.append("符号: 零值（降维变换）")
        
        # 体积缩放因子
        if matrix_size <= 3:
            if matrix_size == 1:
                properties.append(f"长度缩放因子: {abs(det_value):.6f}")
            elif matrix_size == 2:
                properties.append(f"面积缩放因子: {abs(det_value):.6f}")
            elif matrix_size == 3:
                properties.append(f"体积缩放因子: {abs(det_value):.6f}")
        else:
            properties.append(f"超体积缩放因子: {abs(det_value):.6f}")
        
        # 数值稳定性提示
        if 0 < abs(det_value) < 1e-10:
            properties.append("警告: 行列式值接近零，矩阵接近奇异")
        elif abs(det_value) > 1e10:
            properties.append("提示: 行列式值很大，注意数值精度")
        
        return "\n".join(properties)