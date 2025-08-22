import numpy as np

class ArraySplit:
    '''
    数组分割
    沿指定轴将数组分割为多个子数组
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "输入数组": ("NPARRAY", {
                    "tooltip": "要分割的输入数组"
                }),
                "分割数量": ("INT", {
                    "default": 2,
                    "min": 2,
                    "max": 100,
                    "step": 1,
                    "display": "number",
                    "tooltip": "分割成多少个子数组"
                }),
                "分割轴": ("INT", {
                    "default": 0,
                    "min": -10,
                    "max": 10,
                    "step": 1,
                    "display": "number",
                    "tooltip": "沿哪个轴进行分割，0表示第一个轴"
                }),
            },
        }

    RETURN_TYPES = ("NPARRAY", "NPARRAY", "NPARRAY", "NPARRAY")
    RETURN_NAMES = ("子数组1", "子数组2", "子数组3", "子数组4")
    OUTPUT_TOOLTIPS = ("第一个子数组", "第二个子数组", "第三个子数组（可能为空）", "第四个子数组（可能为空）")

    def process(self, 输入数组, 分割数量, 分割轴):
        try:
            # 执行分割操作
            split_arrays = np.array_split(输入数组, 分割数量, axis=分割轴)
            
            # 确保返回4个数组，不足的用None填充
            result = [None, None, None, None]
            for i, arr in enumerate(split_arrays[:4]):
                result[i] = arr
            
            return tuple(result)
        except ValueError as e:
            raise ValueError(f"数组分割失败: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"分割操作时发生未知错误: {str(e)}")