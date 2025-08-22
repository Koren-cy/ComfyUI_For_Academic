import numpy as np
import sys

class ArrayLogarithm:
    '''
    对数函数数组
    创建指定形状的对数函数数组
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
                    "default": 0.1,
                    "min": -float(sys.maxsize),
                    "max": float(sys.maxsize),
                    "step": 0.001,
                    "display": "number",
                    "tooltip": "x轴的起始值（必须大于0）"
                }),
                "结束值": ("FLOAT", {
                    "default": 10.0,
                    "min": -float(sys.maxsize),
                    "max": float(sys.maxsize),
                    "step": 0.001,
                    "display": "number",
                    "tooltip": "x轴的结束值（必须大于0）"
                }),
                "底数": ("FLOAT", {
                    "default": 2.718,
                    "min": 0.0,
                    "max": float(sys.maxsize),
                    "step": 0.001,
                    "display": "number",
                    "tooltip": "对数函数的底数（默认为e≈2.718，不能等于1）"
                }),
                "系数": ("FLOAT", {
                    "default": 1.0,
                    "min": -float(sys.maxsize),
                    "max": float(sys.maxsize),
                    "step": 0.001,
                    "display": "number",
                    "tooltip": "对数函数的系数"
                }),
                "幅值": ("FLOAT", {
                    "default": 1.0,
                    "min": -float(sys.maxsize),
                    "max": float(sys.maxsize),
                    "step": 0.001,
                    "display": "number",
                    "tooltip": "函数的幅值"
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
    OUTPUT_TOOLTIPS = ("创建的对数函数数组",)

    def process(self, 形状, 起始值, 结束值, 底数, 系数, 幅值, 偏移):
        try:
            # 验证参数
            if 起始值 <= 0 or 结束值 <= 0:
                raise ValueError("起始值和结束值必须大于0")
            if 底数 <= 0 or 底数 == 1:
                raise ValueError("底数必须大于0且不等于1")
            if 起始值 >= 结束值:
                raise ValueError("起始值必须小于结束值")
            
            shape = self._parse_shape(形状)
            
            # 如果是多维数组，计算总元素数量
            if isinstance(shape, tuple):
                total_elements = np.prod(shape)
            else:
                total_elements = shape
            
            # 创建x轴数据
            x = np.linspace(起始值, 结束值, total_elements)
            
            # 计算对数函数: A * log_base(k*x) + offset
            # 使用换底公式: log_base(x) = ln(x) / ln(base)
            if 底数 == np.e or abs(底数 - np.e) < 1e-6:
                # 自然对数
                log_array = 幅值 * np.log(系数 * x) + 偏移
            else:
                # 其他底数的对数
                log_array = 幅值 * (np.log(系数 * x) / np.log(底数)) + 偏移
            
            # 检查是否有无穷大或NaN值
            if np.any(np.isinf(log_array)) or np.any(np.isnan(log_array)):
                raise ValueError("计算结果包含无穷大或NaN值，请检查参数设置")
            
            # 重塑为指定形状
            if isinstance(shape, tuple):
                log_array = log_array.reshape(shape)
            
            return (log_array,)
        except ValueError as e:
            raise ValueError(f"对数函数数组创建失败: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"创建对数函数数组时发生未知错误: {str(e)}")
    
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