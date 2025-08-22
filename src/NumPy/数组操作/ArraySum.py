import numpy as np

class ArraySum:
    '''
    数组求和
    计算数组元素的和
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "输入数组": ("NPARRAY", {
                    "tooltip": "要求和的输入数组"
                }),
            },
            "optional": {
                "求和轴": ("STRING", {
                    "default": "",
                    "tooltip": "沿哪个轴求和，留空表示对所有元素求和，格式如 0 或 (0, 1)"
                }),
                "保持维度": (["是", "否"], {
                    "default": "否",
                    "tooltip": "是否保持原数组的维度"
                }),
            },
        }

    RETURN_TYPES = ("NPARRAY",)
    RETURN_NAMES = ("求和结果",)
    OUTPUT_TOOLTIPS = ("求和后的数组或标量",)

    def process(self, 输入数组, 求和轴="", 保持维度="否"):
        try:
            keepdims = True if 保持维度 == "是" else False
            
            if 求和轴.strip():
                # 解析轴参数
                axis = self._parse_axis(求和轴)
                result = np.sum(输入数组, axis=axis, keepdims=keepdims)
            else:
                # 对所有元素求和
                result = np.sum(输入数组, keepdims=keepdims)
            
            return (result,)
        except Exception as e:
            raise RuntimeError(f"求和操作时发生未知错误: {str(e)}")
    
    def _parse_axis(self, axis_str):
        """解析轴参数字符串"""
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