import numpy as np

class ArrayOnes:
    '''
    全一数组
    创建指定形状和数据类型的全一数组
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "形状": ("STRING", {
                    "default": "(3, 3)",
                    "tooltip": "数组的形状，格式如 (3, 3) 或 (5,) 或 10"
                }),
                "数据类型": (["float64", "float32", "int64", "int32", "int16", "int8", "uint64", "uint32", "uint16", "uint8", "bool", "complex128", "complex64"], {
                    "default": "float64",
                    "tooltip": "数组元素的数据类型"
                }),
            },
        }

    RETURN_TYPES = ("NPARRAY",)
    RETURN_NAMES = ("数组输出",)
    OUTPUT_TOOLTIPS = ("创建的全一数组",)

    def process(self, 形状, 数据类型):
        try:
            shape = self._parse_shape(形状)
            
            ones_array = np.ones(shape, dtype=数据类型)
            
            return (ones_array,)
        except ValueError as e:
            raise ValueError(f"全一数组创建失败: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"创建全一数组时发生未知错误: {str(e)}")
    
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