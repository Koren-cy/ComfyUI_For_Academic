import numpy as np

class ArrayMax:
    '''
    数组最大值
    计算数组元素的最大值
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "输入数组": ("NPARRAY", {
                    "tooltip": "要计算最大值的输入数组"
                }),
            },
            "optional": {
                "计算轴": ("STRING", {
                    "default": "",
                    "tooltip": "沿哪个轴计算最大值，留空表示对所有元素计算，格式如 0 或 (0, 1)"
                }),
                "保持维度": (["是", "否"], {
                    "default": "否",
                    "tooltip": "是否保持原数组的维度"
                }),
            },
        }

    RETURN_TYPES = ("NPARRAY",)
    RETURN_NAMES = ("最大值结果",)
    OUTPUT_TOOLTIPS = ("最大值计算后的数组或标量",)

    def process(self, 输入数组, 计算轴="", 保持维度="否"):
        try:
            keepdims = True if 保持维度 == "是" else False
            
            if 计算轴.strip():
                # 解析轴参数
                axis = self._parse_axis(计算轴)
                result = np.max(输入数组, axis=axis, keepdims=keepdims)
            else:
                # 对所有元素计算最大值
                result = np.max(输入数组, keepdims=keepdims)
            
            return (result,)
        except Exception as e:
            raise RuntimeError(f"最大值计算时发生未知错误: {str(e)}")
    
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