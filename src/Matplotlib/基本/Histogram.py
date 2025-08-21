import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import base64
from io import BytesIO
import matplotlib

# 设置matplotlib后端为非交互式
matplotlib.use('Agg')

class Histogram:
    '''
    直方图
    使用Matplotlib绘制直方图，支持DataFrame数据输入
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "数据": ("DATAFRAME", {
                    "tooltip": "输入的DataFrame数据"
                }),
                "列名": ("STRING", {
                    "default": "",
                    "tooltip": "要绘制直方图的列名，留空则使用第一个数值列"
                }),
            },
            "optional": {
                "标题": ("STRING", {
                    "default": "直方图",
                    "tooltip": "图表标题"
                }),
                "X轴标签": ("STRING", {
                    "default": "数值",
                    "tooltip": "X轴标签"
                }),
                "Y轴标签": ("STRING", {
                    "default": "频次",
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
                "柱子数量": ("INT", {
                    "default": 30,
                    "min": 5,
                    "max": 100,
                    "tooltip": "直方图柱子数量（bins）"
                }),
                "柱子颜色": ("STRING", {
                    "default": "skyblue",
                    "tooltip": "柱子颜色（如：red, blue, green, #FF0000等）"
                }),
                "柱子透明度": ("FLOAT", {
                    "default": 0.7,
                    "min": 0.1,
                    "max": 1.0,
                    "step": 0.1,
                    "tooltip": "柱子透明度"
                }),
                "边框颜色": ("STRING", {
                    "default": "black",
                    "tooltip": "柱子边框颜色"
                }),
                "边框宽度": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 5.0,
                    "step": 0.5,
                    "tooltip": "柱子边框宽度"
                }),
                "显示统计信息": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "是否显示均值和标准差线"
                }),
            },
        }

    RETURN_TYPES = ()
    RETURN_NAMES = ()
    OUTPUT_NODE = True

    def process(self, 数据, 列名="", 标题="直方图", X轴标签="数值", Y轴标签="频次", 
                图像宽度=10, 图像高度=6, 柱子数量=30, 柱子颜色="skyblue", 柱子透明度=0.7, 
                边框颜色="black", 边框宽度=1.0, 显示统计信息=True):
        try:

            # 创建图形
            fig, ax = plt.subplots(figsize=(图像宽度, 图像高度))
            
            # 获取数值列
            numeric_columns = 数据.select_dtypes(include=[np.number]).columns.tolist()
            
            if len(numeric_columns) == 0:
                raise ValueError("数据中没有找到数值列")
            
            # 获取要绘制的数据
            if 列名 and 列名 in 数据.columns:
                data_column = 数据[列名]
                col_name = 列名
            else:
                data_column = 数据[numeric_columns[0]]
                col_name = numeric_columns[0]
            
            # 确保数据是数值类型
            if not pd.api.types.is_numeric_dtype(data_column):
                try:
                    data_column = pd.to_numeric(data_column, errors='coerce')
                except:
                    raise ValueError(f"无法将列 '{col_name}' 转换为数值类型")
            
            # 移除缺失值
            data_clean = data_column.dropna()
            
            if len(data_clean) == 0:
                raise ValueError("清理后的数据为空")
            
            # 绘制直方图
            n, bins, patches = ax.hist(data_clean, bins=柱子数量, color=柱子颜色, 
                                     alpha=柱子透明度, edgecolor=边框颜色, linewidth=边框宽度)
            
            # 显示统计信息
            if 显示统计信息:
                mean_val = data_clean.mean()
                std_val = data_clean.std()
                
                # 添加均值线
                ax.axvline(mean_val, color='red', linestyle='--', linewidth=2, 
                          label=f'均值: {mean_val:.2f}')
                
                # 添加标准差线
                ax.axvline(mean_val + std_val, color='orange', linestyle=':', linewidth=2, 
                          label=f'+1σ: {mean_val + std_val:.2f}')
                ax.axvline(mean_val - std_val, color='orange', linestyle=':', linewidth=2, 
                          label=f'-1σ: {mean_val - std_val:.2f}')
                
                # 添加图例
                ax.legend()
            
            # 设置标题和标签
            ax.set_title(标题, fontsize=14, fontweight='bold')
            ax.set_xlabel(X轴标签 if X轴标签 != "数值" else col_name, fontsize=12)
            ax.set_ylabel(Y轴标签, fontsize=12)
            
            # 设置网格
            ax.grid(True, alpha=0.3)
            
            # 添加统计信息文本
            if 显示统计信息:
                stats_text = f'样本数: {len(data_clean)}\n均值: {data_clean.mean():.2f}\n标准差: {data_clean.std():.2f}\n最小值: {data_clean.min():.2f}\n最大值: {data_clean.max():.2f}'
                ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, fontsize=10,
                       verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
            
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
            ax.set_title('Histogram 错误', fontsize=14)
            
            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            buffer.close()
            plt.close(fig)
            
            return {"ui": {"data": [image_base64]}}