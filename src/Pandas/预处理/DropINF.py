import pandas as pd
import numpy as np


class DropINF:
    """
    删除含无穷值的行
    """
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "数据帧": ("DATAFRAME", {}),
            },
            "optional": {
                "关注的列": ("STRING", {
                    "multiline": False,
                    "default": "",
                    "tooltip": "指定列名，多个列名用逗号分隔。留空则检查所有列"
                }),
                "策略": (["any", "all"], {
                    "default": "any",
                    "tooltip": "any: 任一列有无穷值就删除该行\nall: 所有列都有无穷值才删除该行"
                }),
            },
        }

    RETURN_TYPES = ("DATAFRAME",)
    RETURN_NAMES = ("数据帧",)
    OUTPUT_TOOLTIPS = ("删除含无穷值的行后的DataFrame",)


    def process(self, 数据帧, 关注的列="", 策略="any"):
        subset_cols = None
        if 关注的列.strip():
            subset_cols = [col.strip() for col in 关注的列.split(',') if col.strip()]
            invalid_cols = [col for col in subset_cols if col not in 数据帧.columns]
            if invalid_cols:
                raise ValueError(f"列名不存在: {invalid_cols}")
        
        # 创建数据帧副本
        df = 数据帧.copy()
        
        # 确定要检查的列
        check_cols = subset_cols if subset_cols else df.columns.tolist()
        
        # 只检查数值列中的无穷值
        numeric_cols = [col for col in check_cols if pd.api.types.is_numeric_dtype(df[col])]
        
        if not numeric_cols:
            # 如果没有数值列，直接返回原数据帧
            return (df,)
        
        # 检查无穷值并删除相应行
        if 策略 == "any":
            # 任一列有无穷值就删除该行
            mask = ~np.isinf(df[numeric_cols]).any(axis=1)
        else: 
            # 所有列都有无穷值才删除该行
            mask = ~np.isinf(df[numeric_cols]).all(axis=1)
        
        return (df[mask],)