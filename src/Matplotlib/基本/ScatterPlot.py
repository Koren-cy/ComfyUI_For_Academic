import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import base64
from io import BytesIO
import matplotlib

# 设置matplotlib后端为非交互式
matplotlib.use('Agg')

class ScatterPlot:
    '''
    散点图
    使用Matplotlib绘制散点图，支持DataFrame数据输入
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
                    "tooltip": "X轴数据的列名"
                }),
                "Y轴列名": ("STRING", {
                    "default": "",
                    "tooltip": "Y轴数据的列名"
                }),
            },
            "optional": {
                "标题": ("STRING", {
                    "default": "散点图",
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
                "点颜色": ("STRING", {
                    "default": "blue",
                    "tooltip": "散点颜色（如：red, blue, green, #FF0000等）"
                }),
                "点大小": ("FLOAT", {
                    "default": 50.0,
                    "min": 1.0,
                    "max": 500.0,
                    "step": 5.0,
                    "tooltip": "散点大小"
                }),
                "点透明度": ("FLOAT", {
                    "default": 0.7,
                    "min": 0.1,
                    "max": 1.0,
                    "step": 0.1,
                    "tooltip": "散点透明度"
                }),
                "点形状": (["o", "s", "^", "v", "<", ">", "D", "*", "+", "x"], {
                    "default": "o",
                    "tooltip": "散点形状"
                }),
            },
        }

    RETURN_TYPES = ()
    RETURN_NAMES = ()
    OUTPUT_NODE = True

    def process(self, 数据, X轴列名="", Y轴列名="", 标题="散点图", X轴标签="X轴", Y轴标签="Y轴", 
                图像宽度=10, 图像高度=6, 点颜色="blue", 点大小=50.0, 点透明度=0.7, 点形状="o"):
        try:

            # 创建图形
            fig, ax = plt.subplots(figsize=(图像宽度, 图像高度))
            
            # 获取数值列
            numeric_columns = 数据.select_dtypes(include=[np.number]).columns.tolist()
            
            if len(numeric_columns) < 2:
                raise ValueError("数据中至少需要两个数值列")
            
            # 获取X轴数据
            if X轴列名 and X轴列名 in 数据.columns:
                x_data = 数据[X轴列名]
            else:
                x_data = 数据[numeric_columns[0]]
                X轴列名 = numeric_columns[0]
            
            # 获取Y轴数据
            if Y轴列名 and Y轴列名 in 数据.columns:
                y_data = 数据[Y轴列名]
            else:
                # 选择与X轴不同的列
                available_cols = [col for col in numeric_columns if col != X轴列名]
                if available_cols:
                    y_data = 数据[available_cols[0]]
                    Y轴列名 = available_cols[0]
                else:
                    y_data = 数据[numeric_columns[1]] if len(numeric_columns) > 1 else 数据[numeric_columns[0]]
                    Y轴列名 = numeric_columns[1] if len(numeric_columns) > 1 else numeric_columns[0]
            
            # 绘制散点图
            ax.scatter(x_data, y_data, c=点颜色, s=点大小, alpha=点透明度, marker=点形状)
            
            # 设置标题和标签
            ax.set_title(标题, fontsize=14, fontweight='bold')
            ax.set_xlabel(X轴标签 if X轴标签 != "X轴" else X轴列名, fontsize=12)
            ax.set_ylabel(Y轴标签 if Y轴标签 != "Y轴" else Y轴列名, fontsize=12)
            
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
            ax.set_title('ScatterPlot 错误', fontsize=14)
            
            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            buffer.close()
            plt.close(fig)
            
            return {"ui": {"data": [image_base64]}}