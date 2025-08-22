import numpy as np
import sys, math

class ArrayCosine:
    '''
    余弦函数数组
    创建指定形状的余弦函数数组
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "形状": ("STRING", {
                    "default": "(100,)",
                    "tooltip": "数组的形状，格式如 (100,) 或 (10, 10) 或 100"
                }),
                "起始值": ("FLOAT", {
                    "default": 0.0,
                    "min": -float(sys.maxsize),
                    "max": float(sys.maxsize),
                    "step": 0.001,
                    "display": "number",
                    "tooltip": "x轴的起始值"
                }),
                "结束值": ("FLOAT", {
                    "default": math.pi * 2,
                    "min": -float(sys.maxsize),
                    "max": float(sys.maxsize),
                    "step": 0.001,
                    "display": "number",
                    "tooltip": "x轴的结束值（默认2π）"
                }),
                "振幅": ("FLOAT", {
                    "default": 1.0,
                    "min": -float(sys.maxsize),
                    "max": float(sys.maxsize),
                    "step": 0.001,
                    "display": "number",
                    "tooltip": "余弦波的振幅"
                }),
                "频率": ("FLOAT", {
                    "default": 1.0,
                    "min": -float(sys.maxsize),
                    "max": float(sys.maxsize),
                    "step": 0.001,
                    "display": "number",
                    "tooltip": "余弦波的频率"
                }),
                "相位": ("FLOAT", {
                    "default": 0.0,
                    "min": -math.pi * 2,
                    "max": math.pi * 2,
                    "step": 0.001,
                    "display": "number",
                    "tooltip": "余弦波的相位偏移（弧度）"
                }),
                "偏移": ("FLOAT", {
                    "default": 0.0,
                    "min": -float(sys.maxsize),
                    "max": float(sys.maxsize),
                    "step": 0.001,
                    "display": "number",
                    "tooltip": "y轴的偏移量"
                }),
            },
        }

    RETURN_TYPES = ("NPARRAY",)
    RETURN_NAMES = ("数组输出",)
    OUTPUT_TOOLTIPS = ("创建的余弦函数数组",)

    def process(self, 形状, 起始值, 结束值, 振幅, 频率, 相位, 偏移):
        try:
            shape = self._parse_shape(形状)
            
            # 如果是多维数组，计算总元素数量
            if isinstance(shape, tuple):
                total_elements = np.prod(shape)
            else:
                total_elements = shape
            
            # 创建x轴数据
            x = np.linspace(起始值, 结束值, total_elements)
            
            # 计算余弦函数: A * cos(2π * f * x + φ) + offset
            cosine_array = 振幅 * np.cos(2 * np.pi * 频率 * x + 相位) + 偏移
            
            # 重塑为指定形状
            if isinstance(shape, tuple):
                cosine_array = cosine_array.reshape(shape)
            
            return (cosine_array,)
        except ValueError as e:
            raise ValueError(f"余弦函数数组创建失败: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"创建余弦函数数组时发生未知错误: {str(e)}")
    
    def _parse_shape(self, shape_str):
        """解析形状字符串"""
        try:
            # 移除空格
            shape_str = shape_str.strip()
            
            # 如果是单个数字
            if shape_str.isdigit():
                return int(shape_str)
            
            # 如果是元组格式
            if shape_str.startswith('(') and shape_str.endswith(')'):
                # 移除括号
                inner = shape_str[1:-1].strip()
                if not inner:
                    return ()
                
                # 分割并转换为整数
                parts = [part.strip() for part in inner.split(',') if part.strip()]
                if len(parts) == 1 and parts[0]:
                    return (int(parts[0]),)
                return tuple(int(part) for part in parts if part)
            
            # 如果是逗号分隔的数字
            if ',' in shape_str:
                parts = [part.strip() for part in shape_str.split(',') if part.strip()]
                return tuple(int(part) for part in parts)
            
            # 默认情况，尝试转换为整数
            return int(shape_str)
        except (ValueError, TypeError) as e:
            raise ValueError(f"无效的形状格式: {shape_str}. 请使用如 (100,) 或 100 的格式")