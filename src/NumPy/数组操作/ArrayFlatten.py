import numpy as np

class ArrayFlatten:
    '''
    数组展平
    将多维数组展平为一维数组
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "输入数组": ("NPARRAY", {
                    "tooltip": "要展平的输入数组"
                }),
                "展平方式": (["C", "F", "A", "K"], {
                    "default": "C",
                    "tooltip": "展平顺序：C(行优先)、F(列优先)、A(自动)、K(保持内存布局)"
                }),
            },
        }

    RETURN_TYPES = ("NPARRAY",)
    RETURN_NAMES = ("展平数组",)
    OUTPUT_TOOLTIPS = ("展平后的一维数组",)

    def process(self, 输入数组, 展平方式):
        try:
            # 执行展平操作
            result = np.flatten(输入数组) if 展平方式 == "C" else 输入数组.flatten(order=展平方式)
            return (result,)
        except Exception as e:
            raise RuntimeError(f"展平操作时发生未知错误: {str(e)}")