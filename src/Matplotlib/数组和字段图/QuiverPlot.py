import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import base64
from io import BytesIO
import matplotlib

# 设置matplotlib后端为非交互式
matplotlib.use('Agg')

class QuiverPlot:
    '''
    向量场图
    使用Matplotlib绘制箭头图
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "数据": ("DATAFRAME", {
                    "tooltip": "输入的DataFrame数据"
                }),
                "X位置列名": ("STRING", {
                    "default": "",
                    "tooltip": "箭头起始X位置的列名"
                }),
                "Y位置列名": ("STRING", {
                    "default": "",
                    "tooltip": "箭头起始Y位置的列名"
                }),
                "X方向列名": ("STRING", {
                    "default": "",
                    "tooltip": "箭头X方向分量的列名"
                }),
                "Y方向列名": ("STRING", {
                    "default": "",
                    "tooltip": "箭头Y方向分量的列名"
                }),
            },
            "optional": {
                "标题": ("STRING", {
                    "default": "箭头图",
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
                    "default": 8,
                    "min": 3,
                    "max": 15,
                    "tooltip": "图像高度（英寸）"
                }),
                "箭头颜色": ("STRING", {
                    "default": "blue",
                    "tooltip": "箭头颜色（如：red, blue, green, #FF0000等）"
                }),
                "箭头缩放": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.1,
                    "max": 10.0,
                    "step": 0.1,
                    "tooltip": "箭头大小缩放因子"
                }),
                "箭头宽度": ("FLOAT", {
                    "default": 0.005,
                    "min": 0.001,
                    "max": 0.02,
                    "step": 0.001,
                    "tooltip": "箭头宽度"
                }),
                "箭头透明度": ("FLOAT", {
                    "default": 0.8,
                    "min": 0.1,
                    "max": 1.0,
                    "step": 0.1,
                    "tooltip": "箭头透明度"
                }),
                "颜色映射列名": ("STRING", {
                    "default": "",
                    "tooltip": "用于颜色映射的列名（可选）"
                }),
                "颜色映射": (["viridis", "plasma", "inferno", "magma", "coolwarm", "RdYlBu", "RdBu", "Blues", "Reds", "Greens"], {
                    "default": "viridis",
                    "tooltip": "颜色映射方案（当指定颜色映射列时使用）"
                }),
                "显示颜色条": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "是否显示颜色条（当使用颜色映射时）"
                }),
            },
        }

    RETURN_TYPES = ()
    RETURN_NAMES = ()
    OUTPUT_NODE = True

    def process(self, 数据, X位置列名, Y位置列名, X方向列名, Y方向列名, 标题="箭头图", X轴标签="X轴", Y轴标签="Y轴", 
                图像宽度=10, 图像高度=8, 箭头颜色="blue", 箭头缩放=1.0, 箭头宽度=0.005, 箭头透明度=0.8, 
                颜色映射列名="", 颜色映射="viridis", 显示颜色条=False):
        try:

            # 创建图形
            fig, ax = plt.subplots(figsize=(图像宽度, 图像高度))
            
            # 检查列名是否存在
            required_columns = [X位置列名, Y位置列名, X方向列名, Y方向列名]
            for col in required_columns:
                if col not in 数据.columns:
                    raise ValueError(f"列 '{col}' 不存在于数据中")
            
            # 获取数据
            x = 数据[X位置列名].values
            y = 数据[Y位置列名].values
            u = 数据[X方向列名].values
            v = 数据[Y方向列名].values
            
            # 移除NaN值
            mask = ~(np.isnan(x) | np.isnan(y) | np.isnan(u) | np.isnan(v))
            x = x[mask]
            y = y[mask]
            u = u[mask]
            v = v[mask]
            
            if len(x) == 0:
                raise ValueError("没有有效的数据点")
            
            # 处理颜色映射
            if 颜色映射列名 and 颜色映射列名 in 数据.columns:
                c_values = 数据[颜色映射列名].values[mask]
                # 移除颜色值中的NaN
                color_mask = ~np.isnan(c_values)
                if np.any(color_mask):
                    x = x[color_mask]
                    y = y[color_mask]
                    u = u[color_mask]
                    v = v[color_mask]
                    c_values = c_values[color_mask]
                    
                    # 绘制带颜色映射的箭头图
                    quiver = ax.quiver(x, y, u, v, c_values, cmap=颜色映射, 
                                     scale_units='xy', scale=1/箭头缩放, width=箭头宽度, alpha=箭头透明度)
                    
                    # 显示颜色条
                    if 显示颜色条:
                        cbar = plt.colorbar(quiver, ax=ax, shrink=0.8)
                        cbar.set_label(颜色映射列名, fontsize=10)
                        cbar.ax.tick_params(labelsize=10)
                else:
                    # 如果颜色列全是NaN，使用单一颜色
                    ax.quiver(x, y, u, v, color=箭头颜色, 
                             scale_units='xy', scale=1/箭头缩放, width=箭头宽度, alpha=箭头透明度)
            else:
                # 绘制单色箭头图
                ax.quiver(x, y, u, v, color=箭头颜色, 
                         scale_units='xy', scale=1/箭头缩放, width=箭头宽度, alpha=箭头透明度)
            
            # 设置标题和标签
            ax.set_title(标题, fontsize=14, fontweight='bold')
            ax.set_xlabel(X轴标签, fontsize=12)
            ax.set_ylabel(Y轴标签, fontsize=12)
            
            # 设置坐标轴比例相等
            ax.set_aspect('equal', adjustable='box')
            
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
            ax.set_title('QuiverPlot 错误', fontsize=14)
            
            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            buffer.close()
            plt.close(fig)
            
            return {"ui": {"data": [image_base64]}}