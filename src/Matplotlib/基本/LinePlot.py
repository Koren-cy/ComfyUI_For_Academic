import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import base64
from io import BytesIO
import matplotlib

# 设置matplotlib后端为非交互式
matplotlib.use('Agg')

class LinePlot:
    '''
    线图
    使用Matplotlib绘制线图，支持DataFrame数据输入
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "数据": ("DATAFRAME", {
                    "tooltip": "输入的DataFrame数据"
                }),
                "X轴列名": ("STRING", {
                    "default": "",
                    "tooltip": "X轴数据的列名，留空则使用索引"
                }),
                "Y轴列名": ("STRING", {
                    "default": "",
                    "tooltip": "Y轴数据的列名，留空则使用第一列"
                }),
            },
            "optional": {
                "标题": ("STRING", {
                    "default": "线图",
                    "tooltip": "图表标题"
                }),
                "X轴标签": ("STRING", {
                    "default": "X轴",
                    "tooltip": "X轴标签"
                }),
                "Y轴标签": ("STRING", {
                    "default": "Y轴",
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
                "线条颜色": ("STRING", {
                    "default": "blue",
                    "tooltip": "线条颜色（如：red, blue, green, #FF0000等）"
                }),
                "线条样式": (["solid", "dashed", "dotted", "dashdot"], {
                    "default": "solid",
                    "tooltip": "线条样式"
                }),
                "线条宽度": ("FLOAT", {
                    "default": 2.0,
                    "min": 0.5,
                    "max": 10.0,
                    "step": 0.5,
                    "tooltip": "线条宽度"
                }),
            },
        }

    RETURN_TYPES = ()
    RETURN_NAMES = ()
    OUTPUT_NODE = True

    def process(self, 数据, X轴列名="", Y轴列名="", 标题="线图", X轴标签="X轴", Y轴标签="Y轴", 
                图像宽度=10, 图像高度=6, 线条颜色="blue", 线条样式="solid", 线条宽度=2.0):
        try:

            # 创建图形
            fig, ax = plt.subplots(figsize=(图像宽度, 图像高度))
            
            # 获取X轴数据
            if X轴列名 and X轴列名 in 数据.columns:
                x_data = 数据[X轴列名]
            else:
                x_data = 数据.index
            
            # 获取Y轴数据
            if Y轴列名 and Y轴列名 in 数据.columns:
                y_data = 数据[Y轴列名]
            else:
                # 使用第一个数值列
                numeric_columns = 数据.select_dtypes(include=[np.number]).columns
                if len(numeric_columns) > 0:
                    y_data = 数据[numeric_columns[0]]
                else:
                    raise ValueError("数据中没有找到数值列")
            
            # 绘制线图
            ax.plot(x_data, y_data, color=线条颜色, linestyle=线条样式, linewidth=线条宽度)
            
            # 设置标题和标签
            ax.set_title(标题, fontsize=14, fontweight='bold')
            ax.set_xlabel(X轴标签, fontsize=12)
            ax.set_ylabel(Y轴标签, fontsize=12)
            
            # 设置网格
            ax.grid(True, alpha=0.3)
            
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
            ax.set_title('LinePlot 错误', fontsize=14)
            
            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            buffer.close()
            plt.close(fig)
            
            return {"ui": {"data": [image_base64]}}