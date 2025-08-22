import numpy as np
import pandas as pd

class NumpyToDataFrame:
    '''
    NumPy转DataFrame
    将NumPy数组转换为DataFrame格式
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "数组": ("NPARRAY", {
                    "tooltip": "要转换的NumPy数组"
                }),
            },
            "optional": {
                "列名": ("STRING", {
                    "default": "",
                    "tooltip": "DataFrame的列名，用逗号分隔，如 'A,B,C'。留空则使用默认列名"
                }),
                "索引名": ("STRING", {
                    "default": "",
                    "tooltip": "DataFrame的索引名，用逗号分隔。留空则使用默认索引"
                }),
            },
        }

    RETURN_TYPES = ("DATAFRAME",)
    RETURN_NAMES = ("DataFrame输出",)
    OUTPUT_TOOLTIPS = ("Pandas DataFrame",)

    def process(self, 数组, 列名="", 索引名=""):
        try:
            # 确保输入是NumPy数组
            if not isinstance(数组, np.ndarray):
                raise ValueError("输入必须是NumPy数组")
            
            # 处理列名
            columns = None
            if 列名.strip():
                columns = [col.strip() for col in 列名.split(',')]
                # 检查列名数量是否匹配
                if 数组.ndim == 1:
                    if len(columns) != 1:
                        raise ValueError(f"一维数组需要1个列名，但提供了{len(columns)}个")
                elif 数组.ndim == 2:
                    if len(columns) != 数组.shape[1]:
                        raise ValueError(f"二维数组需要{数组.shape[1]}个列名，但提供了{len(columns)}个")
                else:
                    raise ValueError("只支持一维或二维数组转换为DataFrame")
            
            # 处理索引名
            index = None
            if 索引名.strip():
                index = [idx.strip() for idx in 索引名.split(',')]
                # 检查索引数量是否匹配
                expected_rows = 数组.shape[0] if 数组.ndim >= 1 else 1
                if len(index) != expected_rows:
                    raise ValueError(f"数组有{expected_rows}行，但提供了{len(index)}个索引名")
            
            # 根据数组维度进行转换
            if 数组.ndim == 1:
                # 一维数组转换为单列DataFrame
                df = pd.DataFrame(数组, columns=columns if columns else ['value'], index=index)
            elif 数组.ndim == 2:
                # 二维数组直接转换
                df = pd.DataFrame(数组, columns=columns, index=index)
            else:
                raise ValueError("只支持一维或二维数组转换为DataFrame")
            
            return (df,)
            
        except ValueError as e:
            raise ValueError(f"NumPy转DataFrame失败: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"转换过程中发生未知错误: {str(e)}")