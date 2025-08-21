import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import base64
from io import BytesIO
import matplotlib
from scipy.interpolate import griddata

# 设置matplotlib后端为非交互式
matplotlib.use('Agg')

class ContourPlot:
    '''
    等高线图
    使用Matplotlib绘制等高线图
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
                "Z轴列名": ("STRING", {
                    "default": "",
                    "tooltip": "Z轴（高度）数据的列名"
                }),
            },
            "optional": {
                "标题": ("STRING", {
                    "default": "等高线图",
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
                "等高线数量": ("INT", {
                    "default": 10,
                    "min": 5,
                    "max": 50,
                    "tooltip": "等高线的数量"
                }),
                "颜色映射": (["viridis", "plasma", "inferno", "magma", "coolwarm", "RdYlBu", "RdBu", "Blues", "Reds", "Greens"], {
                    "default": "viridis",
                    "tooltip": "颜色映射方案"
                }),
                "填充等高线": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "是否填充等高线区域"
                }),
                "显示等高线标签": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "是否显示等高线数值标签"
                }),
                "显示颜色条": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "是否显示颜色条"
                }),
                "网格分辨率": ("INT", {
                    "default": 100,
                    "min": 50,
                    "max": 300,
                    "tooltip": "插值网格的分辨率"
                }),
            },
        }

    RETURN_TYPES = ()
    RETURN_NAMES = ()
    OUTPUT_NODE = True

    def process(self, 数据, X轴列名, Y轴列名, Z轴列名, 标题="等高线图", X轴标签="X轴", Y轴标签="Y轴", 
                图像宽度=10, 图像高度=8, 等高线数量=10, 颜色映射="viridis", 填充等高线=True, 
                显示等高线标签=False, 显示颜色条=True, 网格分辨率=100):
        try:

            # 创建图形
            fig, ax = plt.subplots(figsize=(图像宽度, 图像高度))
            
            # 检查列名是否存在
            if X轴列名 not in 数据.columns:
                raise ValueError(f"列 '{X轴列名}' 不存在于数据中")
            if Y轴列名 not in 数据.columns:
                raise ValueError(f"列 '{Y轴列名}' 不存在于数据中")
            if Z轴列名 not in 数据.columns:
                raise ValueError(f"列 '{Z轴列名}' 不存在于数据中")
            
            # 获取数据
            x = 数据[X轴列名].values
            y = 数据[Y轴列名].values
            z = 数据[Z轴列名].values
            
            # 移除NaN值
            mask = ~(np.isnan(x) | np.isnan(y) | np.isnan(z))
            x = x[mask]
            y = y[mask]
            z = z[mask]
            
            if len(x) == 0:
                raise ValueError("没有有效的数据点")
            
            # 创建网格
            xi = np.linspace(x.min(), x.max(), 网格分辨率)
            yi = np.linspace(y.min(), y.max(), 网格分辨率)
            Xi, Yi = np.meshgrid(xi, yi)
            
            # 插值
            try:
                Zi = griddata((x, y), z, (Xi, Yi), method='linear')
                # 如果线性插值失败，尝试最近邻插值
                if np.all(np.isnan(Zi)):
                    Zi = griddata((x, y), z, (Xi, Yi), method='nearest')
            except Exception:
                # 如果插值失败，使用简单的网格化方法
                from scipy.stats import binned_statistic_2d
                ret = binned_statistic_2d(x, y, z, statistic='mean', bins=[网格分辨率//2, 网格分辨率//2])
                Zi = ret.statistic.T
                Xi, Yi = np.meshgrid(ret.x_edge[:-1], ret.y_edge[:-1])
            
            # 绘制等高线
            if 填充等高线:
                cs = ax.contourf(Xi, Yi, Zi, levels=等高线数量, cmap=颜色映射)
                if 显示颜色条:
                    cbar = plt.colorbar(cs, ax=ax, shrink=0.8)
                    cbar.ax.tick_params(labelsize=10)
            
            # 绘制等高线线条
            cs_lines = ax.contour(Xi, Yi, Zi, levels=等高线数量, colors='black', alpha=0.4, linewidths=0.5)
            
            # 显示等高线标签
            if 显示等高线标签:
                ax.clabel(cs_lines, inline=True, fontsize=8, fmt='%.1f')
            
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
            ax.set_title('ContourPlot 错误', fontsize=14)
            
            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            buffer.close()
            plt.close(fig)
            
            return {"ui": {"data": [image_base64]}}