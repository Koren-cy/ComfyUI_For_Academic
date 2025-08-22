import numpy as np
import sys

class ArrayRandom:
    '''
    随机数组
    创建各种类型的随机数组
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "形状": ("STRING", {
                    "default": "(3, 3)",
                    "tooltip": "数组的形状，格式如 (3, 3) 或 (5,) 或 10"
                }),
                "随机类型": (["uniform", "normal", "randint"], {
                    "default": "uniform",
                    "tooltip": "随机数类型：uniform(均匀分布)、normal(正态分布)、randint(随机整数)"
                }),
                "最小值": ("FLOAT", {
                    "default": 0.0,
                    "min": -float(sys.maxsize),
                    "max": float(sys.maxsize),
                    "step": 0.001,
                    "display": "number",
                    "tooltip": "随机数的最小值（uniform和randint使用）"
                }),
                "最大值": ("FLOAT", {
                    "default": 1.0,
                    "min": -float(sys.maxsize),
                    "max": float(sys.maxsize),
                    "step": 0.001,
                    "display": "number",
                    "tooltip": "随机数的最大值（uniform和randint使用）"
                }),
                "均值": ("FLOAT", {
                    "default": 0.0,
                    "min": -float(sys.maxsize),
                    "max": float(sys.maxsize),
                    "step": 0.001,
                    "display": "number",
                    "tooltip": "正态分布的均值（仅normal类型使用）"
                }),
                "标准差": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.001,
                    "max": 1000.0,
                    "step": 0.001,
                    "display": "number",
                    "tooltip": "正态分布的标准差（仅normal类型使用）"
                }),
                "随机种子": ("INT", {
                    "default": -1,
                    "min": -1,
                    "max": int(sys.maxsize),
                    "step": 1,
                    "display": "number",
                    "tooltip": "随机种子，-1表示不设置种子"
                }),
            },
        }

    RETURN_TYPES = ("NPARRAY",)
    RETURN_NAMES = ("数组输出",)
    OUTPUT_TOOLTIPS = ("创建的随机数组",)

    def process(self, 形状, 随机类型, 最小值, 最大值, 均值, 标准差, 随机种子):
        try:
            if 随机种子 >= 0:
                np.random.seed(随机种子)
            
            shape = self._parse_shape(形状)
            
            # 根据随机类型创建数组
            if 随机类型 == "uniform":
                # 均匀分布
                random_array = np.random.uniform(最小值, 最大值, shape)
            elif 随机类型 == "normal":
                # 正态分布
                random_array = np.random.normal(均值, 标准差, shape)
            elif 随机类型 == "randint":
                # 随机整数
                low = int(最小值)
                high = int(最大值) + 1  # randint的high是不包含的
                if low >= high:
                    high = low + 1
                random_array = np.random.randint(low, high, shape)
            else:
                # 默认使用uniform
                random_array = np.random.uniform(最小值, 最大值, shape)
            
            return (random_array,)
        except ValueError as e:
            raise ValueError(f"随机数组创建失败: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"创建随机数组时发生未知错误: {str(e)}")

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
            raise ValueError(f"无效的形状格式: {shape_str}. 请使用如 (3, 3) 或 10 的格式")