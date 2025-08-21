import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import base64
from io import BytesIO
import matplotlib

# 设置matplotlib后端为非交互式
matplotlib.use('Agg')

class PolarPlot:
    '''
    极坐标图
    使用Matplotlib绘制极坐标图，支持DataFrame数据输入
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "数据": ("DATAFRAME", {
                    "tooltip": "输入的DataFrame数据"
                }),
                "角度列名": ("STRING", {
                    "default": "",
                    "tooltip": "角度数据的列名（弧度制）"
                }),
                "半径列名": ("STRING", {
                    "default": "",
                    "tooltip": "半径数据的列名"
                }),
            },
            "optional": {
                "标题": ("STRING", {
                    "default": "极坐标图",
                    "tooltip": "图表标题"
                }),
                "图像宽度": ("INT", {
                    "default": 8,
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
                "角度单位": (["弧度", "角度"], {
                    "default": "弧度",
                    "tooltip": "角度数据的单位"
                }),
                "绘图类型": (["散点", "线图", "散点+线图"], {
                    "default": "散点",
                    "tooltip": "极坐标图的绘制类型"
                }),
            },
        }

    RETURN_TYPES = ()
    RETURN_NAMES = ()
    OUTPUT_NODE = True

    def process(self, 数据, 角度列名="", 半径列名="", 标题="极坐标图", 图像宽度=8, 图像高度=8, 
                点颜色="blue", 点大小=50.0, 点透明度=0.7, 角度单位="弧度", 绘图类型="散点"):
        try:
            # 创建极坐标图形
            fig, ax = plt.subplots(figsize=(图像宽度, 图像高度), subplot_kw=dict(projection='polar'))
            
            # 获取角度数据
            if 角度列名 and 角度列名 in 数据.columns:
                theta_data = 数据[角度列名]
            else:
                # 使用第一个数值列作为角度
                numeric_columns = 数据.select_dtypes(include=[np.number]).columns
                if len(numeric_columns) > 0:
                    theta_data = 数据[numeric_columns[0]]
                else:
                    raise ValueError("数据中没有找到数值列作为角度数据")
            
            # 获取半径数据
            if 半径列名 and 半径列名 in 数据.columns:
                r_data = 数据[半径列名]
            else:
                # 使用第二个数值列作为半径，如果只有一列则使用索引
                numeric_columns = 数据.select_dtypes(include=[np.number]).columns
                if len(numeric_columns) > 1:
                    r_data = 数据[numeric_columns[1]]
                elif len(numeric_columns) == 1:
                    r_data = pd.Series(range(len(数据)), index=数据.index)
                else:
                    raise ValueError("数据中没有找到足够的数值列")
            
            # 角度单位转换
            if 角度单位 == "角度":
                theta_data = np.radians(theta_data)
            
            # 绘制极坐标图
            if 绘图类型 == "散点":
                ax.scatter(theta_data, r_data, c=点颜色, s=点大小, alpha=点透明度)
            elif 绘图类型 == "线图":
                ax.plot(theta_data, r_data, color=点颜色, alpha=点透明度)
            elif 绘图类型 == "散点+线图":
                ax.plot(theta_data, r_data, color=点颜色, alpha=点透明度)
                ax.scatter(theta_data, r_data, c=点颜色, s=点大小, alpha=点透明度)
            
            # 设置标题
            ax.set_title(标题, fontsize=14, fontweight='bold', pad=20)
            
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
            ax.set_title('PolarPlot 错误', fontsize=14)
            
            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            buffer.close()
            plt.close(fig)
            
            return {"ui": {"data": [image_base64]}}