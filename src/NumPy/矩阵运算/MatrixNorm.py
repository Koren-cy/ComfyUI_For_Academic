import numpy as np
import sys

class MatrixNorm:
    '''
    矩阵范数
    计算矩阵的各种范数
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "输入矩阵": ("NPARRAY", {
                    "tooltip": "要计算范数的输入矩阵"
                }),
            },
            "optional": {
                "范数类型": (["Frobenius", "核范数", "1范数", "2范数", "无穷范数", "-1范数", "-2范数", "-无穷范数", "自定义"], {
                    "default": "Frobenius",
                    "tooltip": "要计算的范数类型"
                }),
                "自定义阶数": ("FLOAT", {
                    "default": 2.0,
                    "min": -float(sys.maxsize),
                    "max": float(sys.maxsize),
                    "step": 0.1,
                    "display": "number",
                    "tooltip": "自定义范数的阶数（仅在选择自定义时使用）"
                }),
                "计算轴": ("STRING", {
                    "default": "",
                    "tooltip": "沿哪个轴计算范数，留空表示整个矩阵，格式如 0, 1, (0,1)"
                }),
                "保持维度": (["否", "是"], {
                    "default": "否",
                    "tooltip": "是否保持原数组的维度"
                }),
            },
        }

    RETURN_TYPES = ("NPARRAY", "STRING")
    RETURN_NAMES = ("范数值", "范数信息")
    OUTPUT_TOOLTIPS = ("计算得到的范数值", "范数计算的详细信息")

    def process(self, 输入矩阵, 范数类型="Frobenius", 自定义阶数=2.0, 计算轴="", 保持维度="否"):
        try:
            # 检查输入
            if 输入矩阵.size == 0:
                raise ValueError("输入矩阵不能为空")
            
            keepdims = True if 保持维度 == "是" else False
            
            # 解析轴参数
            axis = self._parse_axis(计算轴) if 计算轴.strip() else None
            
            # 根据范数类型计算
            if 范数类型 == "Frobenius":
                norm_value = np.linalg.norm(输入矩阵, ord='fro', axis=axis, keepdims=keepdims)
                norm_description = "Frobenius范数（所有元素平方和的平方根）"
            elif 范数类型 == "核范数":
                if axis is not None:
                    raise ValueError("核范数不支持指定轴，请留空计算轴参数")
                if 输入矩阵.ndim != 2:
                    raise ValueError("核范数仅适用于二维矩阵")
                # 核范数是奇异值的和
                singular_values = np.linalg.svd(输入矩阵, compute_uv=False)
                norm_value = np.sum(singular_values)
                if keepdims:
                    norm_value = np.array([[norm_value]])
                else:
                    norm_value = np.array(norm_value)
                norm_description = "核范数（奇异值之和）"
            elif 范数类型 == "1范数":
                norm_value = np.linalg.norm(输入矩阵, ord=1, axis=axis, keepdims=keepdims)
                norm_description = "1范数（列和的最大值）"
            elif 范数类型 == "2范数":
                norm_value = np.linalg.norm(输入矩阵, ord=2, axis=axis, keepdims=keepdims)
                norm_description = "2范数（最大奇异值）"
            elif 范数类型 == "无穷范数":
                norm_value = np.linalg.norm(输入矩阵, ord=np.inf, axis=axis, keepdims=keepdims)
                norm_description = "无穷范数（行和的最大值）"
            elif 范数类型 == "-1范数":
                norm_value = np.linalg.norm(输入矩阵, ord=-1, axis=axis, keepdims=keepdims)
                norm_description = "-1范数（列和的最小值）"
            elif 范数类型 == "-2范数":
                norm_value = np.linalg.norm(输入矩阵, ord=-2, axis=axis, keepdims=keepdims)
                norm_description = "-2范数（最小奇异值）"
            elif 范数类型 == "-无穷范数":
                norm_value = np.linalg.norm(输入矩阵, ord=-np.inf, axis=axis, keepdims=keepdims)
                norm_description = "-无穷范数（行和的最小值）"
            elif 范数类型 == "自定义":
                if 自定义阶数 == float('inf'):
                    ord_param = np.inf
                elif 自定义阶数 == float('-inf'):
                    ord_param = -np.inf
                else:
                    ord_param = 自定义阶数
                norm_value = np.linalg.norm(输入矩阵, ord=ord_param, axis=axis, keepdims=keepdims)
                norm_description = f"自定义{自定义阶数}范数"
            else:
                raise ValueError(f"未知的范数类型: {范数类型}")
            
            # 生成详细信息
            norm_info = self._generate_norm_info(输入矩阵, norm_value, 范数类型, norm_description, axis)
            
            return (norm_value, norm_info)
            
        except ValueError as e:
            raise ValueError(f"矩阵范数计算失败: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"矩阵范数计算时发生未知错误: {str(e)}")
    
    def _parse_axis(self, axis_str):
        """解析轴参数字符串"""
        try:
            # 移除空格
            axis_str = axis_str.strip()
            
            # 如果是单个数字
            if axis_str.isdigit() or (axis_str.startswith('-') and axis_str[1:].isdigit()):
                return int(axis_str)
            
            # 如果是元组格式
            if axis_str.startswith('(') and axis_str.endswith(')'):
                # 移除括号
                inner = axis_str[1:-1].strip()
                if not inner:
                    return None
                
                # 分割并转换为整数
                parts = [part.strip() for part in inner.split(',') if part.strip()]
                if len(parts) == 1:
                    return int(parts[0])
                return tuple(int(part) for part in parts)
            
            # 如果是逗号分隔的数字
            if ',' in axis_str:
                parts = [part.strip() for part in axis_str.split(',') if part.strip()]
                if len(parts) == 1:
                    return int(parts[0])
                return tuple(int(part) for part in parts)
            
            return None
        except (ValueError, TypeError):
            raise ValueError(f"无效的轴格式: {axis_str}. 请使用如 0, 1 或 (0,1) 的格式")
    
    def _generate_norm_info(self, matrix, norm_value, norm_type, description, axis):
        """生成范数计算的详细信息"""
        info = []
        
        # 基本信息
        info.append(f"矩阵形状: {matrix.shape}")
        info.append(f"范数类型: {norm_type}")
        info.append(f"范数描述: {description}")
        
        if axis is not None:
            info.append(f"计算轴: {axis}")
        else:
            info.append("计算轴: 整个矩阵")
        
        # 范数值信息
        if np.isscalar(norm_value) or norm_value.size == 1:
            info.append(f"范数值: {float(norm_value):.6e}")
        else:
            info.append(f"范数值形状: {norm_value.shape}")
            info.append(f"范数值范围: [{np.min(norm_value):.6e}, {np.max(norm_value):.6e}]")
        
        # 特殊范数的额外信息
        if norm_type == "Frobenius" and axis is None:
            total_elements = matrix.size
            rms_value = float(norm_value) / np.sqrt(total_elements)
            info.append(f"均方根值: {rms_value:.6e}")
        
        if norm_type in ["1范数", "无穷范数", "-1范数", "-无穷范数"] and matrix.ndim == 2 and axis is None:
            if norm_type == "1范数":
                col_sums = np.sum(np.abs(matrix), axis=0)
                max_col_idx = np.argmax(col_sums)
                info.append(f"最大列和位置: 第{max_col_idx}列")
            elif norm_type == "无穷范数":
                row_sums = np.sum(np.abs(matrix), axis=1)
                max_row_idx = np.argmax(row_sums)
                info.append(f"最大行和位置: 第{max_row_idx}行")
        
        if norm_type == "核范数":
            # 提供奇异值的额外信息
            try:
                singular_values = np.linalg.svd(matrix, compute_uv=False)
                info.append(f"奇异值数量: {len(singular_values)}")
                info.append(f"最大奇异值: {np.max(singular_values):.6e}")
                info.append(f"最小奇异值: {np.min(singular_values):.6e}")
            except:
                pass
        
        # 数值特性
        if np.isscalar(norm_value) or norm_value.size == 1:
            norm_val = float(norm_value)
            if norm_val == 0:
                info.append("特性: 零矩阵")
            elif norm_val < 1e-10:
                info.append("特性: 接近零矩阵")
            elif norm_val > 1e10:
                info.append("特性: 大范数值，注意数值精度")
        
        return "\n".join(info)