import numpy as np

class ArrayConcatenate:
    '''
    数组连接
    沿指定轴连接多个数组
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "数组A": ("NPARRAY", {
                    "tooltip": "第一个输入数组"
                }),
                "数组B": ("NPARRAY", {
                    "tooltip": "第二个输入数组"
                }),
                "连接轴": ("INT", {
                    "default": 0,
                    "min": -10,
                    "max": 10,
                    "step": 1,
                    "display": "number",
                    "tooltip": "沿哪个轴进行连接，0表示第一个轴"
                }),
            },
            "optional": {
                "数组C": ("NPARRAY", {
                    "tooltip": "第三个输入数组（可选）"
                }),
                "数组D": ("NPARRAY", {
                    "tooltip": "第四个输入数组（可选）"
                }),
            },
        }

    RETURN_TYPES = ("NPARRAY",)
    RETURN_NAMES = ("连接数组",)
    OUTPUT_TOOLTIPS = ("连接后的数组",)

    def process(self, 数组A, 数组B, 连接轴, 数组C=None, 数组D=None):
        try:
            # 收集所有非空数组
            arrays = [数组A, 数组B]
            if 数组C is not None:
                arrays.append(数组C)
            if 数组D is not None:
                arrays.append(数组D)
            
            # 执行连接操作
            result = np.concatenate(arrays, axis=连接轴)
            return (result,)
        except ValueError as e:
            raise ValueError(f"数组连接失败: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"连接操作时发生未知错误: {str(e)}")