import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import base64
from io import BytesIO
import matplotlib
from scipy.interpolate import griddata

# 设置matplotlib后端为非交互式
matplotlib.use('Agg')

class StreamPlot:
    '''
    流线图
    使用Matplotlib绘制流线图，支持DataFrame数据输入
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
                    "tooltip": "X位置的列名"
                }),
                "Y位置列名": ("STRING", {
                    "default": "",
                    "tooltip": "Y位置的列名"
                }),
                "X方向列名": ("STRING", {
                    "default": "",
                    "tooltip": "X方向速度分量的列名"
                }),
                "Y方向列名": ("STRING", {
                    "default": "",
                    "tooltip": "Y方向速度分量的列名"
                }),
            },
            "optional": {
                "标题": ("STRING", {
                    "default": "流线图",
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
                "流线颜色": ("STRING", {
                    "default": "blue",
                    "tooltip": "流线颜色（如：red, blue, green, #FF0000等）"
                }),
                "流线密度": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.1,
                    "max": 5.0,
                    "step": 0.1,
                    "tooltip": "流线密度"
                }),
                "流线宽度": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.5,
                    "max": 5.0,
                    "step": 0.1,
                    "tooltip": "流线宽度"
                }),
                "箭头大小": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.1,
                    "max": 3.0,
                    "step": 0.1,
                    "tooltip": "箭头大小"
                }),
                "网格分辨率": ("INT", {
                    "default": 50,
                    "min": 20,
                    "max": 200,
                    "tooltip": "插值网格的分辨率"
                }),
                "颜色映射列名": ("STRING", {
                    "default": "",
                    "tooltip": "用于颜色映射的列名（可选，通常使用速度大小）"
                }),
                "颜色映射": (["viridis", "plasma", "inferno", "magma", "coolwarm", "RdYlBu", "RdBu", "Blues", "Reds", "Greens"], {
                    "default": "viridis",
                    "tooltip": "颜色映射方案"
                }),
                "显示颜色条": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "是否显示颜色条"
                }),
            },
        }

    RETURN_TYPES = ()
    RETURN_NAMES = ()
    OUTPUT_NODE = True

    def process(self, 数据, X位置列名, Y位置列名, X方向列名, Y方向列名, 标题="流线图", X轴标签="X轴", Y轴标签="Y轴", 
                图像宽度=10, 图像高度=8, 流线颜色="blue", 流线密度=1.0, 流线宽度=1.0, 箭头大小=1.0, 
                网格分辨率=50, 颜色映射列名="", 颜色映射="viridis", 显示颜色条=False):
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
            
            # 创建规则网格
            x_min, x_max = x.min(), x.max()
            y_min, y_max = y.min(), y.max()
            
            # 添加边距
            x_margin = (x_max - x_min) * 0.1
            y_margin = (y_max - y_min) * 0.1
            
            xi = np.linspace(x_min - x_margin, x_max + x_margin, 网格分辨率)
            yi = np.linspace(y_min - y_margin, y_max + y_margin, 网格分辨率)
            Xi, Yi = np.meshgrid(xi, yi)
            
            # 插值到规则网格
            try:
                Ui = griddata((x, y), u, (Xi, Yi), method='linear', fill_value=0)
                Vi = griddata((x, y), v, (Xi, Yi), method='linear', fill_value=0)
                
                # 如果插值结果全是NaN，尝试最近邻插值
                if np.all(np.isnan(Ui)) or np.all(np.isnan(Vi)):
                    Ui = griddata((x, y), u, (Xi, Yi), method='nearest')
                    Vi = griddata((x, y), v, (Xi, Yi), method='nearest')
            except Exception:
                raise ValueError("数据插值失败，请检查数据分布")
            
            # 处理颜色映射
            if 颜色映射列名 and 颜色映射列名 in 数据.columns:
                # 使用指定列作为颜色
                color_values = 数据[颜色映射列名].values[mask]
                color_grid = griddata((x, y), color_values, (Xi, Yi), method='linear')
                
                # 绘制带颜色映射的流线图
                strm = ax.streamplot(Xi, Yi, Ui, Vi, color=color_grid, cmap=颜色映射,
                                   density=流线密度, linewidth=流线宽度, arrowsize=箭头大小)
                
                if 显示颜色条:
                    cbar = plt.colorbar(strm.lines, ax=ax, shrink=0.8)
                    cbar.set_label(颜色映射列名, fontsize=10)
                    cbar.ax.tick_params(labelsize=10)
            else:
                # 计算速度大小作为颜色（如果没有指定颜色列）
                speed = np.sqrt(Ui**2 + Vi**2)
                
                if 颜色映射列名 == "" and 显示颜色条:
                    # 使用速度大小作为颜色
                    strm = ax.streamplot(Xi, Yi, Ui, Vi, color=speed, cmap=颜色映射,
                                       density=流线密度, linewidth=流线宽度, arrowsize=箭头大小)
                    cbar = plt.colorbar(strm.lines, ax=ax, shrink=0.8)
                    cbar.set_label('速度大小', fontsize=10)
                    cbar.ax.tick_params(labelsize=10)
                else:
                    # 使用单一颜色
                    ax.streamplot(Xi, Yi, Ui, Vi, color=流线颜色,
                                density=流线密度, linewidth=流线宽度, arrowsize=箭头大小)
            
            # 设置标题和标签
            ax.set_title(标题, fontsize=14, fontweight='bold')
            ax.set_xlabel(X轴标签, fontsize=12)
            ax.set_ylabel(Y轴标签, fontsize=12)
            
            # 设置坐标轴范围
            ax.set_xlim(x_min - x_margin, x_max + x_margin)
            ax.set_ylim(y_min - y_margin, y_max + y_margin)
            
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
            ax.set_title('StreamPlot 错误', fontsize=14)
            
            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            buffer.close()
            plt.close(fig)
            
            return {"ui": {"data": [image_base64]}}