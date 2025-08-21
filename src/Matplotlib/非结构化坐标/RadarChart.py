import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import base64
from io import BytesIO
import matplotlib
from math import pi

# 设置matplotlib后端为非交互式
matplotlib.use('Agg')

class RadarChart:
    '''
    雷达图
    使用Matplotlib绘制雷达图
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "数据": ("DATAFRAME", {
                    "tooltip": "输入的DataFrame数据，每行代表一个样本，每列代表一个维度"
                }),
            },
            "optional": {
                "标题": ("STRING", {
                    "default": "雷达图",
                    "tooltip": "图表标题"
                }),
                "图像宽度": ("INT", {
                    "default": 10,
                    "min": 4,
                    "max": 20,
                    "tooltip": "图像宽度（英寸）"
                }),
                "图像高度": ("INT", {
                    "default": 10,
                    "min": 3,
                    "max": 15,
                    "tooltip": "图像高度（英寸）"
                }),
                "填充透明度": ("FLOAT", {
                    "default": 0.25,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.05,
                    "tooltip": "填充区域的透明度"
                }),
                "线条宽度": ("FLOAT", {
                    "default": 2.0,
                    "min": 0.5,
                    "max": 5.0,
                    "step": 0.5,
                    "tooltip": "线条宽度"
                }),
                "显示网格": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "是否显示网格线"
                }),
                "标准化数据": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "是否将数据标准化到0-1范围"
                }),
                "颜色方案": (["默认", "彩虹", "蓝色系", "红色系", "绿色系"], {
                    "default": "默认",
                    "tooltip": "颜色方案选择"
                }),
            },
        }

    RETURN_TYPES = ()
    RETURN_NAMES = ()
    OUTPUT_NODE = True

    def process(self, 数据, 标题="雷达图", 图像宽度=10, 图像高度=10, 填充透明度=0.25, 
                线条宽度=2.0, 显示网格=True, 标准化数据=True, 颜色方案="默认"):
        try:
            # 获取数值列
            numeric_data = 数据.select_dtypes(include=[np.number])
            if numeric_data.empty:
                raise ValueError("数据中没有找到数值列")
            
            # 数据标准化
            if 标准化数据:
                numeric_data = (numeric_data - numeric_data.min()) / (numeric_data.max() - numeric_data.min())
                numeric_data = numeric_data.fillna(0)  # 处理除零情况
            
            # 获取维度名称和数量
            categories = list(numeric_data.columns)
            N = len(categories)
            
            if N < 3:
                raise ValueError("雷达图至少需要3个维度")
            
            # 计算角度
            angles = [n / float(N) * 2 * pi for n in range(N)]
            angles += angles[:1]  # 闭合图形
            
            # 创建图形
            fig, ax = plt.subplots(figsize=(图像宽度, 图像高度), subplot_kw=dict(projection='polar'))
            
            # 颜色方案
            if 颜色方案 == "彩虹":
                colors = plt.cm.rainbow(np.linspace(0, 1, len(numeric_data)))
            elif 颜色方案 == "蓝色系":
                colors = plt.cm.Blues(np.linspace(0.3, 1, len(numeric_data)))
            elif 颜色方案 == "红色系":
                colors = plt.cm.Reds(np.linspace(0.3, 1, len(numeric_data)))
            elif 颜色方案 == "绿色系":
                colors = plt.cm.Greens(np.linspace(0.3, 1, len(numeric_data)))
            else:  # 默认
                colors = plt.cm.tab10(np.linspace(0, 1, len(numeric_data)))
            
            # 绘制每个样本
            for idx, (index, row) in enumerate(numeric_data.iterrows()):
                values = row.values.tolist()
                values += values[:1]  # 闭合图形
                
                color = colors[idx] if len(numeric_data) > 1 else colors[0]
                label = str(index) if len(numeric_data) > 1 else None
                
                ax.plot(angles, values, 'o-', linewidth=线条宽度, 
                       label=label, color=color)
                ax.fill(angles, values, alpha=填充透明度, color=color)
            
            # 设置标签
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(categories)
            
            # 设置网格
            if 显示网格:
                ax.grid(True, alpha=0.3)
            else:
                ax.grid(False)
            
            # 设置标题
            ax.set_title(标题, size=16, fontweight='bold', pad=20)
            
            # 添加图例（如果有多个样本）
            if len(numeric_data) > 1:
                plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
            
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
            ax.set_title('RadarChart 错误', fontsize=14)
            
            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            buffer.close()
            plt.close(fig)
            
            return {"ui": {"data": [image_base64]}}