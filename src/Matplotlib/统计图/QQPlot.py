import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import base64
from io import BytesIO
import matplotlib
from scipy import stats

# 设置matplotlib后端为非交互式
matplotlib.use('Agg')

class QQPlot:
    '''
    QQ图
    使用Matplotlib绘制QQ图，用于正态性检验和分布比较
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
                    "tooltip": "要绘制的列名，留空则使用第一个数值列"
                }),
                "理论分布": (["normal", "uniform", "exponential", "gamma", "beta"], {
                    "default": "normal",
                    "tooltip": "用于比较的理论分布"
                }),
                "标题": ("STRING", {
                    "default": "QQ图",
                    "tooltip": "图表标题"
                }),
                "X轴标签": ("STRING", {
                    "default": "理论分位数",
                    "tooltip": "X轴标签"
                }),
                "Y轴标签": ("STRING", {
                    "default": "样本分位数",
                    "tooltip": "Y轴标签"
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
                "显示参考线": (["True", "False"], {
                    "default": "True",
                    "tooltip": "是否显示45度参考线"
                }),
                "点的颜色": ("STRING", {
                    "default": "blue",
                    "tooltip": "散点颜色"
                }),
                "点的大小": ("INT", {
                    "default": 30,
                    "min": 10,
                    "max": 100,
                    "tooltip": "散点大小"
                }),
                "点的透明度": ("FLOAT", {
                    "default": 0.7,
                    "min": 0.1,
                    "max": 1.0,
                    "step": 0.1,
                    "tooltip": "散点透明度"
                }),
                "参考线颜色": ("STRING", {
                    "default": "red",
                    "tooltip": "参考线颜色"
                }),
                "参考线样式": (["solid", "dashed", "dotted", "dashdot"], {
                    "default": "dashed",
                    "tooltip": "参考线样式"
                }),
            },
        }

    RETURN_TYPES = ()
    RETURN_NAMES = ()
    OUTPUT_NODE = True

    def process(self, 数据, 列名="", 理论分布="normal", 标题="QQ图", X轴标签="理论分位数", Y轴标签="样本分位数", 
                图像宽度=8, 图像高度=8, 显示参考线="True", 点的颜色="blue", 点的大小=30, 
                点的透明度=0.7, 参考线颜色="red", 参考线样式="dashed"):
        try:
            
            # 创建图形
            fig, ax = plt.subplots(figsize=(图像宽度, 图像高度))
            
            # 转换布尔参数
            show_line = 显示参考线 == "True"
            
            # 获取数据
            if 列名 and 列名 in 数据.columns:
                data_values = 数据[列名].dropna()
            else:
                # 使用第一个数值列
                numeric_columns = 数据.select_dtypes(include=[np.number]).columns
                if len(numeric_columns) == 0:
                    raise ValueError("数据中没有找到数值列")
                data_values = 数据[numeric_columns[0]].dropna()
                列名 = numeric_columns[0]
            
            if len(data_values) < 3:
                raise ValueError("数据点数量不足，至少需要3个数据点")
            
            # 根据理论分布生成QQ图
            if 理论分布 == "normal":
                # 正态分布QQ图
                (osm, osr), _ = stats.probplot(data_values, dist="norm", plot=None)
                X轴标签 = X轴标签 if X轴标签 != "理论分位数" else "正态分布理论分位数"
            elif 理论分布 == "uniform":
                # 均匀分布QQ图
                (osm, osr), _ = stats.probplot(data_values, dist="uniform", plot=None)
                X轴标签 = X轴标签 if X轴标签 != "理论分位数" else "均匀分布理论分位数"
            elif 理论分布 == "exponential":
                # 指数分布QQ图
                (osm, osr), _ = stats.probplot(data_values, dist="expon", plot=None)
                X轴标签 = X轴标签 if X轴标签 != "理论分位数" else "指数分布理论分位数"
            elif 理论分布 == "gamma":
                # 伽马分布QQ图
                (osm, osr), _ = stats.probplot(data_values, dist="gamma", sparams=(1,), plot=None)
                X轴标签 = X轴标签 if X轴标签 != "理论分位数" else "伽马分布理论分位数"
            elif 理论分布 == "beta":
                # 贝塔分布QQ图
                (osm, osr), _ = stats.probplot(data_values, dist="beta", sparams=(2, 2), plot=None)
                X轴标签 = X轴标签 if X轴标签 != "理论分位数" else "贝塔分布理论分位数"
            else:
                # 默认使用正态分布
                (osm, osr), _ = stats.probplot(data_values, dist="norm", plot=None)
            
            # 绘制散点图
            ax.scatter(osm, osr, 
                      color=点的颜色, s=点的大小, alpha=点的透明度, edgecolors='black', linewidth=0.5)
            
            # 显示参考线（45度线）
            if show_line:
                # 计算参考线的范围
                min_val = min(np.min(osm), np.min(osr))
                max_val = max(np.max(osm), np.max(osr))
                ax.plot([min_val, max_val], [min_val, max_val], 
                       color=参考线颜色, linestyle=参考线样式, linewidth=2, label='理想拟合线')
                ax.legend()
            
            # 设置标题和标签
            if 列名:
                full_title = f"{标题} - {列名}"
            else:
                full_title = 标题
            ax.set_title(full_title, fontsize=14, fontweight='bold')
            ax.set_xlabel(X轴标签, fontsize=12)
            ax.set_ylabel(Y轴标签, fontsize=12)
            
            # 设置网格
            ax.grid(True, alpha=0.3)
            
            # 设置相等的纵横比
            ax.set_aspect('equal', adjustable='box')
            
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
            ax.set_title('QQPlot 错误', fontsize=14)
            
            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            buffer.close()
            plt.close(fig)
            
            return {"ui": {"data": [image_base64]}}