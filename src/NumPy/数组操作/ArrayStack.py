import numpy as np

class ArrayStack:
    '''
    数组堆叠
    沿新轴堆叠多个数组
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
                "堆叠轴": ("INT", {
                    "default": 0,
                    "min": -10,
                    "max": 10,
                    "step": 1,
                    "display": "number",
                    "tooltip": "沿哪个新轴进行堆叠，0表示第一个轴"
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
    RETURN_NAMES = ("堆叠数组",)
    OUTPUT_TOOLTIPS = ("堆叠后的数组",)

    def process(self, 数组A, 数组B, 堆叠轴, 数组C=None, 数组D=None):
        try:
            # 收集所有非空数组
            arrays = [数组A, 数组B]
            if 数组C is not None:
                arrays.append(数组C)
            if 数组D is not None:
                arrays.append(数组D)
            
            # 执行堆叠操作
            result = np.stack(arrays, axis=堆叠轴)
            return (result,)
        except ValueError as e:
            raise ValueError(f"数组堆叠失败: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"堆叠操作时发生未知错误: {str(e)}")