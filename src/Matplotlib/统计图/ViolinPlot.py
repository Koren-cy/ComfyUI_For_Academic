import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import base64
from io import BytesIO
import matplotlib

# 设置matplotlib后端为非交互式
matplotlib.use('Agg')

class ViolinPlot:
    '''
    小提琴图
    使用Matplotlib绘制小提琴图，显示数据密度分布
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "数据": ("DATAFRAME", {
                    "tooltip": "输入的DataFrame数据"
                }),
            },
            "optional": {
                "列名": ("STRING", {
                    "default": "",
                    "tooltip": "要绘制的列名，留空则绘制所有数值列"
                }),
                "分组列": ("STRING", {
                    "default": "",
                    "tooltip": "用于分组的列名，留空则不分组"
                }),
                "标题": ("STRING", {
                    "default": "小提琴图",
                    "tooltip": "图表标题"
                }),
                "X轴标签": ("STRING", {
                    "default": "类别",
                    "tooltip": "X轴标签"
                }),
                "Y轴标签": ("STRING", {
                    "default": "数值",
                    "tooltip": "Y轴标签"
                }),
                "图像宽度": ("INT", {
                    "default": 10,
                    "min": 4,
                    "max": 20,
                    "tooltip": "图像宽度（英寸）"
                }),
                "图像高度": ("INT", {
                    "default": 6,
                    "min": 3,
                    "max": 15,
                    "tooltip": "图像高度（英寸）"
                }),
                "显示中位数": (["True", "False"], {
                    "default": "True",
                    "tooltip": "是否显示中位数线"
                }),
                "显示均值": (["True", "False"], {
                    "default": "False",
                    "tooltip": "是否显示均值点"
                }),
                "显示极值": (["True", "False"], {
                    "default": "True",
                    "tooltip": "是否显示极值线"
                }),
                "填充颜色": ("STRING", {
                    "default": "lightblue",
                    "tooltip": "小提琴图填充颜色"
                }),
                "透明度": ("FLOAT", {
                    "default": 0.7,
                    "min": 0.1,
                    "max": 1.0,
                    "step": 0.1,
                    "tooltip": "填充透明度"
                }),
                "X轴标签旋转角度": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 90,
                    "tooltip": "X轴标签旋转角度"
                }),
            },
        }

    RETURN_TYPES = ()
    RETURN_NAMES = ()
    OUTPUT_NODE = True

    def process(self, 数据, 列名="", 分组列="", 标题="小提琴图", X轴标签="类别", Y轴标签="数值", 
                图像宽度=10, 图像高度=6, 显示中位数="True", 显示均值="False", 显示极值="True", 
                填充颜色="lightblue", 透明度=0.7, X轴标签旋转角度=0):
        try:

            # 创建图形
            fig, ax = plt.subplots(figsize=(图像宽度, 图像高度))
            
            # 转换布尔参数
            show_medians = 显示中位数 == "True"
            show_means = 显示均值 == "True"
            show_extrema = 显示极值 == "True"
            
            # 准备数据
            if 分组列 and 分组列 in 数据.columns:
                # 按分组列分组绘制
                groups = 数据.groupby(分组列)
                
                if 列名 and 列名 in 数据.columns:
                    # 指定列名的分组小提琴图
                    data_to_plot = [group[列名].dropna() for name, group in groups]
                    labels = [str(name) for name, group in groups]
                else:
                    # 所有数值列的分组小提琴图
                    numeric_columns = 数据.select_dtypes(include=[np.number]).columns
                    if len(numeric_columns) == 0:
                        raise ValueError("数据中没有找到数值列")
                    
                    # 使用第一个数值列
                    first_numeric_col = numeric_columns[0]
                    data_to_plot = [group[first_numeric_col].dropna() for name, group in groups]
                    labels = [str(name) for name, group in groups]
            else:
                # 不分组的小提琴图
                if 列名 and 列名 in 数据.columns:
                    # 指定列名
                    data_to_plot = [数据[列名].dropna()]
                    labels = [列名]
                else:
                    # 所有数值列
                    numeric_columns = 数据.select_dtypes(include=[np.number]).columns
                    if len(numeric_columns) == 0:
                        raise ValueError("数据中没有找到数值列")
                    
                    data_to_plot = [数据[col].dropna() for col in numeric_columns]
                    labels = list(numeric_columns)
            
            # 绘制小提琴图
            violin_parts = ax.violinplot(data_to_plot, 
                                        positions=range(1, len(data_to_plot) + 1),
                                        showmedians=show_medians,
                                        showmeans=show_means,
                                        showextrema=show_extrema)
            
            # 设置小提琴图颜色和透明度
            for pc in violin_parts['bodies']:
                pc.set_facecolor(填充颜色)
                pc.set_alpha(透明度)
            
            # 设置X轴标签
            ax.set_xticks(range(1, len(labels) + 1))
            ax.set_xticklabels(labels)
            
            # 设置标题和标签
            ax.set_title(标题, fontsize=14, fontweight='bold')
            ax.set_xlabel(X轴标签, fontsize=12)
            ax.set_ylabel(Y轴标签, fontsize=12)
            
            # 设置X轴标签旋转
            if X轴标签旋转角度 > 0:
                plt.xticks(rotation=X轴标签旋转角度)
            
            # 设置网格
            ax.grid(True, alpha=0.3, axis='y')
            
            # 调整布局
            plt.tight_layout()
            
            # 转换为base64
            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            buffer.close()
            
            # 清理图形
            plt.close(fig)
            
            return {"ui": {"data": [image_base64]}}
            
        except Exception as e:
            # 错误处理
            fig, ax = plt.subplots(figsize=(图像宽度, 图像高度))
            ax.text(0.5, 0.5, f'错误: {str(e)}', ha='center', va='center', 
                   transform=ax.transAxes, fontsize=12, color='red')
            ax.set_title('ViolinPlot 错误', fontsize=14)
            
            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            buffer.close()
            plt.close(fig)
            
            return {"ui": {"data": [image_base64]}}