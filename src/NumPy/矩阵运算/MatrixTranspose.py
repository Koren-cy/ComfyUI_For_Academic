import numpy as np

class MatrixTranspose:
    '''
    矩阵转置
    计算输入矩阵的转置
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "输入矩阵": ("NPARRAY", {
                    "tooltip": "要进行转置的输入矩阵"
                }),
            },
            "optional": {
                "转置轴": ("STRING", {
                    "default": "",
                    "tooltip": "指定转置的轴顺序，留空表示默认转置，格式如 (1, 0) 或 (2, 0, 1)"
                }),
            },
        }

    RETURN_TYPES = ("NPARRAY",)
    RETURN_NAMES = ("转置矩阵",)
    OUTPUT_TOOLTIPS = ("转置后的矩阵",)

    def process(self, 输入矩阵, 转置轴=""):
        try:
            # 检查输入维度
            if 输入矩阵.ndim == 0:
                raise ValueError("输入不能是标量，请使用数组或矩阵")
            
            # 如果指定了转置轴
            if 转置轴.strip():
                axes = self._parse_axes(转置轴, 输入矩阵.ndim)
                result = np.transpose(输入矩阵, axes)
            else:
                # 默认转置（对于2D矩阵是行列互换，对于高维数组是最后两个轴互换）
                if 输入矩阵.ndim == 1:
                    # 1D数组转置后仍是1D数组
                    result = 输入矩阵.copy()
                elif 输入矩阵.ndim == 2:
                    # 2D矩阵标准转置
                    result = np.transpose(输入矩阵)
                else:
                    # 高维数组，交换最后两个轴
                    axes = list(range(输入矩阵.ndim))
                    axes[-2], axes[-1] = axes[-1], axes[-2]
                    result = np.transpose(输入矩阵, axes)
            
            return (result,)
        except ValueError as e:
            raise ValueError(f"矩阵转置失败: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"矩阵转置运算时发生未知错误: {str(e)}")
    
    def _parse_axes(self, axes_str, ndim):
        """解析轴参数字符串"""
        try:
            # 移除空格
            axes_str = axes_str.strip()
            
            # 如果是元组格式
            if axes_str.startswith('(') and axes_str.endswith(')'):
                # 移除括号
                inner = axes_str[1:-1].strip()
                if not inner:
                    return None
                
                # 分割并转换为整数
                parts = [part.strip() for part in inner.split(',') if part.strip()]
                axes = tuple(int(part) for part in parts)
            else:
                # 如果是逗号分隔的数字
                if ',' in axes_str:
                    parts = [part.strip() for part in axes_str.split(',') if part.strip()]
                    axes = tuple(int(part) for part in parts)
                else:
                    # 单个数字
                    axes = (int(axes_str),)
            
            # 验证轴的有效性
            if len(axes) != ndim:
                raise ValueError(f"轴的数量({len(axes)})必须等于数组的维度({ndim})")
            
            # 检查轴的范围和唯一性
            for axis in axes:
                if axis < 0 or axis >= ndim:
                    raise ValueError(f"轴索引{axis}超出范围[0, {ndim-1}]")
            
            if len(set(axes)) != len(axes):
                raise ValueError("轴索引不能重复")
            
            return axes
        except (ValueError, TypeError) as e:
            raise ValueError(f"无效的轴格式: {axes_str}. 请使用如 (1, 0) 的格式")