import numpy as np

class ArrayReshape:
    '''
    数组重塑
    改变数组的形状而不改变数据
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "输入数组": ("NPARRAY", {
                    "tooltip": "要重塑的输入数组"
                }),
                "新形状": ("STRING", {
                    "default": "(3, 3)",
                    "tooltip": "新的数组形状，格式如 (3, 3) 或 (5,) 或 10，使用 -1 表示自动计算该维度"
                }),
            },
        }

    RETURN_TYPES = ("NPARRAY",)
    RETURN_NAMES = ("重塑数组",)
    OUTPUT_TOOLTIPS = ("重塑后的数组",)

    def process(self, 输入数组, 新形状):
        try:
            shape = self._parse_shape(新形状)
            
            # 执行重塑操作
            result = np.reshape(输入数组, shape)
            return (result,)
        except ValueError as e:
            raise ValueError(f"数组重塑失败: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"重塑操作时发生未知错误: {str(e)}")
    
    def _parse_shape(self, shape_str):
        """解析形状字符串"""
        # 移除空格
        shape_str = shape_str.strip()
        
        # 如果是单个数字或-1
        if shape_str.isdigit() or shape_str == "-1":
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
                return (int(parts[0]) if parts[0] != "-1" else -1,)
            return tuple(int(part) if part != "-1" else -1 for part in parts if part)
        
        # 如果是逗号分隔的数字
        if ',' in shape_str:
            parts = [part.strip() for part in shape_str.split(',') if part.strip()]
            return tuple(int(part) if part != "-1" else -1 for part in parts)
        
        # 默认情况，尝试转换为整数
        return int(shape_str) if shape_str != "-1" else -1