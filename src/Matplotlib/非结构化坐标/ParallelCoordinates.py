import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import base64
from io import BytesIO
import matplotlib
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# 设置matplotlib后端为非交互式
matplotlib.use('Agg')

class ParallelCoordinates:
    '''
    平行坐标图
    使用Matplotlib绘制平行坐标图，支持DataFrame数据输入，用于高维数据可视化
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "数据": ("DATAFRAME", {
                    "tooltip": "输入的DataFrame数据，每列代表一个维度"
                }),
            },
            "optional": {
                "标题": ("STRING", {
                    "default": "平行坐标图",
                    "tooltip": "图表标题"
                }),
                "图像宽度": ("INT", {
                    "default": 12,
                    "min": 6,
                    "max": 20,
                    "tooltip": "图像宽度（英寸）"
                }),
                "图像高度": ("INT", {
                    "default": 8,
                    "min": 4,
                    "max": 15,
                    "tooltip": "图像高度（英寸）"
                }),
                "线条透明度": ("FLOAT", {
                    "default": 0.6,
                    "min": 0.1,
                    "max": 1.0,
                    "step": 0.1,
                    "tooltip": "线条的透明度"
                }),
                "线条宽度": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.1,
                    "max": 3.0,
                    "step": 0.1,
                    "tooltip": "线条宽度"
                }),
                "标准化方法": (["MinMax", "StandardScaler", "无"], {
                    "default": "MinMax",
                    "tooltip": "数据标准化方法"
                }),
                "颜色列名": ("STRING", {
                    "default": "",
                    "tooltip": "用于着色的列名，留空则使用默认颜色"
                }),
                "颜色方案": (["viridis", "plasma", "inferno", "magma", "rainbow", "coolwarm"], {
                    "default": "viridis",
                    "tooltip": "颜色方案选择"
                }),
                "显示轴标签": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "是否显示坐标轴标签"
                }),
                "轴标签角度": ("INT", {
                    "default": 45,
                    "min": 0,
                    "max": 90,
                    "tooltip": "轴标签的旋转角度"
                }),
            },
        }

    RETURN_TYPES = ()
    RETURN_NAMES = ()
    OUTPUT_NODE = True

    def process(self, 数据, 标题="平行坐标图", 图像宽度=12, 图像高度=8, 线条透明度=0.6, 
                线条宽度=1.0, 标准化方法="MinMax", 颜色列名="", 颜色方案="viridis", 
                显示轴标签=True, 轴标签角度=45):
        try:
            # 获取数值列
            numeric_data = 数据.select_dtypes(include=[np.number])
            if numeric_data.empty:
                raise ValueError("数据中没有找到数值列")
            
            if len(numeric_data.columns) < 2:
                raise ValueError("平行坐标图至少需要2个维度")
            
            # 数据标准化
            if 标准化方法 == "MinMax":
                scaler = MinMaxScaler()
                scaled_data = pd.DataFrame(
                    scaler.fit_transform(numeric_data),
                    columns=numeric_data.columns,
                    index=numeric_data.index
                )
            elif 标准化方法 == "StandardScaler":
                scaler = StandardScaler()
                scaled_data = pd.DataFrame(
                    scaler.fit_transform(numeric_data),
                    columns=numeric_data.columns,
                    index=numeric_data.index
                )
            else:  # 无标准化
                scaled_data = numeric_data.copy()
            
            # 创建图形
            fig, ax = plt.subplots(figsize=(图像宽度, 图像高度))
            
            # 设置x轴位置
            x_positions = range(len(scaled_data.columns))
            
            # 处理颜色
            if 颜色列名 and 颜色列名 in 数据.columns:
                color_data = 数据[颜色列名]
                if pd.api.types.is_numeric_dtype(color_data):
                    # 数值型数据，使用colormap
                    norm = plt.Normalize(vmin=color_data.min(), vmax=color_data.max())
                    cmap = plt.get_cmap(颜色方案)
                    colors = [cmap(norm(val)) for val in color_data]
                else:
                    # 分类数据，使用离散颜色
                    unique_vals = color_data.unique()
                    cmap = plt.get_cmap(颜色方案)
                    color_map = {val: cmap(i/len(unique_vals)) for i, val in enumerate(unique_vals)}
                    colors = [color_map[val] for val in color_data]
            else:
                # 默认颜色
                colors = ['blue'] * len(scaled_data)
            
            # 绘制每条线
            for idx, (index, row) in enumerate(scaled_data.iterrows()):
                values = row.values
                ax.plot(x_positions, values, color=colors[idx], 
                       alpha=线条透明度, linewidth=线条宽度)
            
            # 设置坐标轴
            ax.set_xlim(-0.5, len(scaled_data.columns) - 0.5)
            ax.set_xticks(x_positions)
            
            if 显示轴标签:
                ax.set_xticklabels(scaled_data.columns, rotation=轴标签角度, ha='right')
            else:
                ax.set_xticklabels([])
            
            # 为每个维度添加垂直轴线
            for i, col in enumerate(scaled_data.columns):
                y_min, y_max = scaled_data[col].min(), scaled_data[col].max()
                ax.axvline(x=i, color='black', alpha=0.3, linewidth=0.5)
                
                # 添加刻度标签
                if 标准化方法 != "无":
                    # 显示原始数据的范围
                    orig_min, orig_max = numeric_data[col].min(), numeric_data[col].max()
                    ax.text(i, y_min - 0.1, f'{orig_min:.2f}', ha='center', va='top', fontsize=8)
                    ax.text(i, y_max + 0.1, f'{orig_max:.2f}', ha='center', va='bottom', fontsize=8)
            
            # 设置标题
            ax.set_title(标题, fontsize=16, fontweight='bold', pad=20)
            
            # 设置网格
            ax.grid(True, alpha=0.3, axis='y')
            
            # 如果使用了颜色列，添加颜色条
            if 颜色列名 and 颜色列名 in 数据.columns and pd.api.types.is_numeric_dtype(数据[颜色列名]):
                sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
                sm.set_array([])
                cbar = plt.colorbar(sm, ax=ax)
                cbar.set_label(颜色列名, rotation=270, labelpad=15)
            
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
            ax.set_title('ParallelCoordinates 错误', fontsize=14)
            
            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            buffer.close()
            plt.close(fig)
            
            return {"ui": {"data": [image_base64]}}