import numpy as np

class ArrayTranspose:
    '''
    数组转置
    交换数组的轴
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "输入数组": ("NPARRAY", {
                    "tooltip": "要转置的输入数组"
                }),
            },
            "optional": {
                "轴顺序": ("STRING", {
                    "default": "",
                    "tooltip": "指定轴的顺序，如 (1, 0) 或 (2, 0, 1)，留空则反转所有轴"
                }),
            },
        }

    RETURN_TYPES = ("NPARRAY",)
    RETURN_NAMES = ("转置数组",)
    OUTPUT_TOOLTIPS = ("转置后的数组",)

    def process(self, 输入数组, 轴顺序=""):
        try:
            if 轴顺序.strip():
                # 解析轴顺序
                axes = self._parse_axes(轴顺序)
                result = np.transpose(输入数组, axes)
            else:
                # 默认转置（反转所有轴）
                result = np.transpose(输入数组)
            
            return (result,)
        except ValueError as e:
            raise ValueError(f"数组转置失败: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"转置操作时发生未知错误: {str(e)}")
    
    def _parse_axes(self, axes_str):
        """解析轴顺序字符串"""
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
            return tuple(int(part) for part in parts if part)
        
        # 如果是逗号分隔的数字
        if ',' in axes_str:
            parts = [part.strip() for part in axes_str.split(',') if part.strip()]
            return tuple(int(part) for part in parts)
        
        # 单个数字
        if axes_str.isdigit():
            return (int(axes_str),)
        
        return None