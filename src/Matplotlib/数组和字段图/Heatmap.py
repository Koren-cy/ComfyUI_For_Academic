import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import base64
from io import BytesIO
import matplotlib
import seaborn as sns

# 设置matplotlib后端为非交互式
matplotlib.use('Agg')

class Heatmap:
    '''
    热力图
    使用Matplotlib绘制热力图，支持DataFrame数据输入
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
                "标题": ("STRING", {
                    "default": "热力图",
                    "tooltip": "图表标题"
                }),
                "图像宽度": ("INT", {
                    "default": 10,
                    "min": 4,
                    "max": 20,
                    "tooltip": "图像宽度（英寸）"
                }),
                "图像高度": ("INT", {
                    "default": 8,
                    "min": 3,
                    "max": 15,
                    "tooltip": "图像高度（英寸）"
                }),
                "颜色映射": (["viridis", "plasma", "inferno", "magma", "coolwarm", "RdYlBu", "RdBu", "Blues", "Reds", "Greens"], {
                    "default": "RdYlBu",
                    "tooltip": "颜色映射方案"
                }),
                "显示数值": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "是否在热力图上显示数值"
                }),
                "数值格式": ("STRING", {
                    "default": ".2f",
                    "tooltip": "数值显示格式（如：.2f, .1f, .0f）"
                }),
                "显示颜色条": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "是否显示颜色条"
                }),
                "X轴标签旋转": ("INT", {
                    "default": 45,
                    "min": 0,
                    "max": 90,
                    "tooltip": "X轴标签旋转角度"
                }),
                "Y轴标签旋转": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 90,
                    "tooltip": "Y轴标签旋转角度"
                }),
            },
        }

    RETURN_TYPES = ()
    RETURN_NAMES = ()
    OUTPUT_NODE = True

    def process(self, 数据, 标题="热力图", 图像宽度=10, 图像高度=8, 颜色映射="viridis", 
                显示数值=True, 数值格式=".2f", 显示颜色条=True, X轴标签旋转=45, Y轴标签旋转=0):
        try:

            # 创建图形
            fig, ax = plt.subplots(figsize=(图像宽度, 图像高度))
            
            # 只选择数值列
            numeric_data = 数据.select_dtypes(include=[np.number])
            
            if numeric_data.empty:
                raise ValueError("数据中没有找到数值列")
            
            # 计算相关性矩阵（如果列数大于1）或直接使用数据
            if len(numeric_data.columns) > 1:
                plot_data = numeric_data.corr()
                if 标题 == "热力图":
                    标题 = "相关性热力图"
            else:
                # 如果只有一列，创建一个简单的热力图
                plot_data = numeric_data.values.reshape(-1, 1)
            
            # 绘制热力图
            im = ax.imshow(plot_data, cmap=颜色映射, aspect='auto')
            
            # 设置标题
            ax.set_title(标题, fontsize=14, fontweight='bold', pad=20)
            
            # 设置坐标轴标签
            if hasattr(plot_data, 'columns'):  # DataFrame
                ax.set_xticks(range(len(plot_data.columns)))
                ax.set_yticks(range(len(plot_data.index)))
                ax.set_xticklabels(plot_data.columns, rotation=X轴标签旋转, ha='right')
                ax.set_yticklabels(plot_data.index, rotation=Y轴标签旋转)
                
                # 显示数值
                if 显示数值:
                    for i in range(len(plot_data.index)):
                        for j in range(len(plot_data.columns)):
                            value = plot_data.iloc[i, j]
                            if not np.isnan(value):
                                text_color = 'white' if abs(value) > 0.5 else 'black'
                                ax.text(j, i, format(value, 数值格式), 
                                       ha='center', va='center', color=text_color, fontsize=10)
            else:  # numpy array
                if 显示数值:
                    for i in range(plot_data.shape[0]):
                        for j in range(plot_data.shape[1]):
                            value = plot_data[i, j]
                            if not np.isnan(value):
                                text_color = 'white' if abs(value - plot_data.mean()) > plot_data.std() else 'black'
                                ax.text(j, i, format(value, 数值格式), 
                                       ha='center', va='center', color=text_color, fontsize=10)
            
            # 添加颜色条
            if 显示颜色条:
                cbar = plt.colorbar(im, ax=ax, shrink=0.8)
                cbar.ax.tick_params(labelsize=10)
            
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
            ax.set_title('Heatmap 错误', fontsize=14)
            
            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            buffer.close()
            plt.close(fig)
            
            return {"ui": {"data": [image_base64]}}