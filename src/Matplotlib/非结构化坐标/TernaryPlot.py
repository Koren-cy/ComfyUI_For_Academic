import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import base64
from io import BytesIO
import matplotlib
from matplotlib.patches import Polygon

# 设置matplotlib后端为非交互式
matplotlib.use('Agg')

class TernaryPlot:
    '''
    三角图
    使用Matplotlib绘制三角图，用于显示三元组数据
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "数据": ("DATAFRAME", {
                    "tooltip": "输入的DataFrame数据，需要包含三个数值列"
                }),
                "A列名": ("STRING", {
                    "default": "",
                    "tooltip": "第一个分量的列名"
                }),
                "B列名": ("STRING", {
                    "default": "",
                    "tooltip": "第二个分量的列名"
                }),
                "C列名": ("STRING", {
                    "default": "",
                    "tooltip": "第三个分量的列名"
                }),
            },
            "optional": {
                "标题": ("STRING", {
                    "default": "三角图",
                    "tooltip": "图表标题"
                }),
                "A标签": ("STRING", {
                    "default": "A",
                    "tooltip": "A分量的标签"
                }),
                "B标签": ("STRING", {
                    "default": "B",
                    "tooltip": "B分量的标签"
                }),
                "C标签": ("STRING", {
                    "default": "C",
                    "tooltip": "C分量的标签"
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
                "点颜色": ("STRING", {
                    "default": "blue",
                    "tooltip": "点的颜色（如：red, blue, green, #FF0000等）"
                }),
                "点大小": ("FLOAT", {
                    "default": 50.0,
                    "min": 1.0,
                    "max": 500.0,
                    "step": 1.0,
                    "tooltip": "点的大小"
                }),
                "点透明度": ("FLOAT", {
                    "default": 0.7,
                    "min": 0.1,
                    "max": 1.0,
                    "step": 0.1,
                    "tooltip": "点的透明度"
                }),
                "自动标准化": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "是否自动将三个分量标准化为和为1"
                }),
                "显示网格": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "是否显示网格线"
                }),
            },
        }

    RETURN_TYPES = ()
    RETURN_NAMES = ()
    OUTPUT_NODE = True

    def _ternary_to_cartesian(self, a, b, c):
        """将三角坐标转换为笛卡尔坐标"""
        x = 0.5 * (2 * b + c) / (a + b + c)
        y = (np.sqrt(3) / 2) * c / (a + b + c)
        return x, y

    def _draw_ternary_axes(self, ax, A标签, B标签, C标签, 显示网格):
        """绘制三角坐标轴"""
        # 三角形顶点
        triangle = np.array([[0, 0], [1, 0], [0.5, np.sqrt(3)/2], [0, 0]])
        
        # 绘制三角形边界
        ax.plot(triangle[:, 0], triangle[:, 1], 'k-', linewidth=2)
        
        # 添加标签
        ax.text(-0.05, -0.05, A标签, fontsize=14, ha='right', va='top', fontweight='bold')
        ax.text(1.05, -0.05, B标签, fontsize=14, ha='left', va='top', fontweight='bold')
        ax.text(0.5, np.sqrt(3)/2 + 0.05, C标签, fontsize=14, ha='center', va='bottom', fontweight='bold')
        
        # 绘制网格线
        if 显示网格:
            # 平行于底边的线（C = 常数）
            for i in range(1, 10):
                c_val = i / 10.0
                y = (np.sqrt(3) / 2) * c_val
                x_left = 0.5 * c_val
                x_right = 1 - 0.5 * c_val
                ax.plot([x_left, x_right], [y, y], 'k-', alpha=0.3, linewidth=0.5)
            
            # 平行于左边的线（A = 常数）
            for i in range(1, 10):
                a_val = i / 10.0
                x_bottom = 1 - a_val
                y_bottom = 0
                x_top = 0.5 * (1 - a_val)
                y_top = (np.sqrt(3) / 2) * (1 - a_val)
                ax.plot([x_bottom, x_top], [y_bottom, y_top], 'k-', alpha=0.3, linewidth=0.5)
            
            # 平行于右边的线（B = 常数）
            for i in range(1, 10):
                b_val = i / 10.0
                x_bottom = b_val
                y_bottom = 0
                x_top = 0.5 + 0.5 * (1 - b_val)
                y_top = (np.sqrt(3) / 2) * (1 - b_val)
                ax.plot([x_bottom, x_top], [y_bottom, y_top], 'k-', alpha=0.3, linewidth=0.5)

    def process(self, 数据, A列名="", B列名="", C列名="", 标题="三角图", A标签="A", B标签="B", C标签="C",
                图像宽度=10, 图像高度=8, 点颜色="blue", 点大小=50.0, 点透明度=0.7, 
                自动标准化=True, 显示网格=True):
        try:
            # 获取数值列
            numeric_columns = 数据.select_dtypes(include=[np.number]).columns.tolist()
            
            if len(numeric_columns) < 3:
                raise ValueError("数据中至少需要3个数值列")
            
            # 获取A、B、C列数据
            if A列名 and A列名 in 数据.columns:
                a_data = 数据[A列名]
            else:
                a_data = 数据[numeric_columns[0]]
                A标签 = A标签 if A标签 != "A" else numeric_columns[0]
            
            if B列名 and B列名 in 数据.columns:
                b_data = 数据[B列名]
            else:
                b_data = 数据[numeric_columns[1]]
                B标签 = B标签 if B标签 != "B" else numeric_columns[1]
            
            if C列名 and C列名 in 数据.columns:
                c_data = 数据[C列名]
            else:
                c_data = 数据[numeric_columns[2]]
                C标签 = C标签 if C标签 != "C" else numeric_columns[2]
            
            # 确保数据为正值
            a_data = np.abs(a_data)
            b_data = np.abs(b_data)
            c_data = np.abs(c_data)
            
            # 标准化数据
            if 自动标准化:
                total = a_data + b_data + c_data
                # 避免除零
                total = total.replace(0, 1)
                a_data = a_data / total
                b_data = b_data / total
                c_data = c_data / total
            
            # 转换为笛卡尔坐标
            x_coords, y_coords = self._ternary_to_cartesian(a_data, b_data, c_data)
            
            # 创建图形
            fig, ax = plt.subplots(figsize=(图像宽度, 图像高度))
            
            # 绘制三角坐标轴
            self._draw_ternary_axes(ax, A标签, B标签, C标签, 显示网格)
            
            # 绘制数据点
            ax.scatter(x_coords, y_coords, c=点颜色, s=点大小, alpha=点透明度, zorder=5)
            
            # 设置标题
            ax.set_title(标题, fontsize=16, fontweight='bold', pad=20)
            
            # 设置坐标轴
            ax.set_xlim(-0.1, 1.1)
            ax.set_ylim(-0.1, np.sqrt(3)/2 + 0.1)
            ax.set_aspect('equal')
            ax.axis('off')
            
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
            ax.set_title('TernaryPlot 错误', fontsize=14)
            
            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            buffer.close()
            plt.close(fig)
            
            return {"ui": {"data": [image_base64]}}