import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import base64
from io import BytesIO
import matplotlib
from scipy import stats

# 设置matplotlib后端为非交互式
matplotlib.use('Agg')

class DensityPlot:
    '''
    密度图
    使用Matplotlib绘制密度图，支持DataFrame数据输入，显示概率密度函数
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
                    "default": "密度图",
                    "tooltip": "图表标题"
                }),
                "X轴标签": ("STRING", {
                    "default": "数值",
                    "tooltip": "X轴标签"
                }),
                "Y轴标签": ("STRING", {
                    "default": "密度",
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
                "填充曲线下方": (["True", "False"], {
                    "default": "True",
                    "tooltip": "是否填充密度曲线下方区域"
                }),
                "显示直方图": (["True", "False"], {
                    "default": "False",
                    "tooltip": "是否同时显示直方图"
                }),
                "线条宽度": ("FLOAT", {
                    "default": 2.0,
                    "min": 0.5,
                    "max": 5.0,
                    "step": 0.5,
                    "tooltip": "密度曲线线条宽度"
                }),
                "透明度": ("FLOAT", {
                    "default": 0.7,
                    "min": 0.1,
                    "max": 1.0,
                    "step": 0.1,
                    "tooltip": "填充透明度"
                }),
                "带宽调整": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.1,
                    "max": 3.0,
                    "step": 0.1,
                    "tooltip": "核密度估计带宽调整因子"
                }),
            },
        }

    RETURN_TYPES = ()
    RETURN_NAMES = ()
    OUTPUT_NODE = True

    def process(self, 数据, 列名="", 分组列="", 标题="密度图", X轴标签="数值", Y轴标签="密度", 
                图像宽度=10, 图像高度=6, 填充曲线下方="True", 显示直方图="False", 
                线条宽度=2.0, 透明度=0.7, 带宽调整=1.0):
        try:

            # 创建图形
            fig, ax = plt.subplots(figsize=(图像宽度, 图像高度))
            
            # 转换布尔参数
            fill_under = 填充曲线下方 == "True"
            show_hist = 显示直方图 == "True"
            
            # 颜色列表
            colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']
            
            # 准备数据
            if 分组列 and 分组列 in 数据.columns:
                # 按分组列分组绘制
                groups = 数据.groupby(分组列)
                
                if 列名 and 列名 in 数据.columns:
                    # 指定列名的分组密度图
                    for i, (name, group) in enumerate(groups):
                        data_values = group[列名].dropna()
                        if len(data_values) > 1:
                            # 计算核密度估计
                            kde = stats.gaussian_kde(data_values, bw_method=带宽调整)
                            x_range = np.linspace(data_values.min(), data_values.max(), 200)
                            density = kde(x_range)
                            
                            color = colors[i % len(colors)]
                            
                            # 绘制密度曲线
                            ax.plot(x_range, density, linewidth=线条宽度, color=color, label=str(name))
                            
                            # 填充曲线下方
                            if fill_under:
                                ax.fill_between(x_range, density, alpha=透明度, color=color)
                            
                            # 显示直方图
                            if show_hist:
                                ax.hist(data_values, bins=30, density=True, alpha=0.3, color=color)
                    
                    ax.legend()
                else:
                    # 所有数值列的分组密度图
                    numeric_columns = 数据.select_dtypes(include=[np.number]).columns
                    if len(numeric_columns) == 0:
                        raise ValueError("数据中没有找到数值列")
                    
                    # 使用第一个数值列
                    first_numeric_col = numeric_columns[0]
                    for i, (name, group) in enumerate(groups):
                        data_values = group[first_numeric_col].dropna()
                        if len(data_values) > 1:
                            kde = stats.gaussian_kde(data_values, bw_method=带宽调整)
                            x_range = np.linspace(data_values.min(), data_values.max(), 200)
                            density = kde(x_range)
                            
                            color = colors[i % len(colors)]
                            ax.plot(x_range, density, linewidth=线条宽度, color=color, label=str(name))
                            
                            if fill_under:
                                ax.fill_between(x_range, density, alpha=透明度, color=color)
                            
                            if show_hist:
                                ax.hist(data_values, bins=30, density=True, alpha=0.3, color=color)
                    
                    ax.legend()
            else:
                # 不分组的密度图
                if 列名 and 列名 in 数据.columns:
                    # 指定列名
                    data_values = 数据[列名].dropna()
                    if len(data_values) <= 1:
                        raise ValueError(f"列 '{列名}' 中的有效数据点不足")
                    
                    kde = stats.gaussian_kde(data_values, bw_method=带宽调整)
                    x_range = np.linspace(data_values.min(), data_values.max(), 200)
                    density = kde(x_range)
                    
                    ax.plot(x_range, density, linewidth=线条宽度, color='blue', label=列名)
                    
                    if fill_under:
                        ax.fill_between(x_range, density, alpha=透明度, color='blue')
                    
                    if show_hist:
                        ax.hist(data_values, bins=30, density=True, alpha=0.3, color='blue')
                else:
                    # 所有数值列
                    numeric_columns = 数据.select_dtypes(include=[np.number]).columns
                    if len(numeric_columns) == 0:
                        raise ValueError("数据中没有找到数值列")
                    
                    for i, col in enumerate(numeric_columns[:5]):  # 最多显示5列
                        data_values = 数据[col].dropna()
                        if len(data_values) > 1:
                            kde = stats.gaussian_kde(data_values, bw_method=带宽调整)
                            x_range = np.linspace(data_values.min(), data_values.max(), 200)
                            density = kde(x_range)
                            
                            color = colors[i % len(colors)]
                            ax.plot(x_range, density, linewidth=线条宽度, color=color, label=col)
                            
                            if fill_under:
                                ax.fill_between(x_range, density, alpha=透明度, color=color)
                            
                            if show_hist:
                                ax.hist(data_values, bins=30, density=True, alpha=0.3, color=color)
                    
                    if len(numeric_columns) > 1:
                        ax.legend()
            
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
            ax.set_title('DensityPlot 错误', fontsize=14)
            
            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            buffer.close()
            plt.close(fig)
            
            return {"ui": {"data": [image_base64]}}