import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import base64
from io import BytesIO
import matplotlib

# 设置matplotlib后端为非交互式
matplotlib.use('Agg')

class PieChart:
    '''
    饼图
    使用Matplotlib绘制饼图
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "数据": ("DATAFRAME", {
                    "tooltip": "输入的DataFrame数据"
                }),
                "标签列名": ("STRING", {
                    "default": "",
                    "tooltip": "用作标签的列名"
                }),
                "数值列名": ("STRING", {
                    "default": "",
                    "tooltip": "用作数值的列名"
                }),
            },
            "optional": {
                "标题": ("STRING", {
                    "default": "饼图",
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
                "显示百分比": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "是否显示百分比"
                }),
                "显示数值": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "是否显示具体数值"
                }),
                "突出显示": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 0.5,
                    "step": 0.05,
                    "tooltip": "突出显示最大扇形的距离"
                }),
                "起始角度": ("INT", {
                    "default": 90,
                    "min": 0,
                    "max": 360,
                    "tooltip": "饼图起始角度"
                }),
                "颜色方案": (["default", "pastel", "bright", "dark", "colorful"], {
                    "default": "default",
                    "tooltip": "颜色方案"
                }),
                "显示图例": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "是否显示图例"
                }),
            },
        }

    RETURN_TYPES = ()
    RETURN_NAMES = ()
    OUTPUT_NODE = True

    def process(self, 数据, 标签列名="", 数值列名="", 标题="饼图", 图像宽度=10, 图像高度=8, 
                显示百分比=True, 显示数值=False, 突出显示=0.0, 起始角度=90, 颜色方案="default", 显示图例=True):
        try:

            # 创建图形
            fig, ax = plt.subplots(figsize=(图像宽度, 图像高度))
            
            # 获取数值列和非数值列
            numeric_columns = 数据.select_dtypes(include=[np.number]).columns.tolist()
            categorical_columns = 数据.select_dtypes(exclude=[np.number]).columns.tolist()
            
            # 获取标签数据
            if 标签列名 and 标签列名 in 数据.columns:
                labels = 数据[标签列名]
                label_col = 标签列名
            else:
                # 优先选择非数值列作为标签
                if categorical_columns:
                    labels = 数据[categorical_columns[0]]
                    label_col = categorical_columns[0]
                else:
                    # 使用索引作为标签
                    labels = 数据.index
                    label_col = "索引"
            
            # 获取数值数据
            if 数值列名 and 数值列名 in 数据.columns:
                values = 数据[数值列名]
                value_col = 数值列名
            else:
                # 选择第一个数值列
                if numeric_columns:
                    values = 数据[numeric_columns[0]]
                    value_col = numeric_columns[0]
                else:
                    raise ValueError("数据中没有找到数值列")
            
            # 确保数值是数值类型
            if not pd.api.types.is_numeric_dtype(values):
                try:
                    values = pd.to_numeric(values, errors='coerce')
                except:
                    raise ValueError(f"无法将列 '{value_col}' 转换为数值类型")
            
            # 处理缺失值和负值
            mask = ~(pd.isna(labels) | pd.isna(values)) & (values > 0)
            labels_clean = labels[mask]
            values_clean = values[mask]
            
            if len(values_clean) == 0:
                raise ValueError("没有有效的正数值数据")
            
            # 如果有重复标签，进行聚合
            if len(labels_clean) != len(labels_clean.unique()):
                df_temp = pd.DataFrame({'labels': labels_clean, 'values': values_clean})
                df_grouped = df_temp.groupby('labels')['values'].sum().reset_index()
                labels_clean = df_grouped['labels']
                values_clean = df_grouped['values']
            
            # 设置颜色方案
            color_schemes = {
                "default": None,
                "pastel": plt.cm.Pastel1.colors,
                "bright": plt.cm.Set1.colors,
                "dark": plt.cm.Dark2.colors,
                "colorful": plt.cm.tab10.colors
            }
            colors = color_schemes.get(颜色方案, None)
            
            # 设置突出显示
            explode = None
            if 突出显示 > 0:
                max_idx = values_clean.idxmax() if hasattr(values_clean, 'idxmax') else np.argmax(values_clean)
                explode = [突出显示 if i == max_idx else 0 for i in range(len(values_clean))]
            
            # 设置标签格式
            def make_autopct(values):
                def my_autopct(pct):
                    total = sum(values)
                    val = int(round(pct*total/100.0))
                    if 显示百分比 and 显示数值:
                        return f'{pct:.1f}%\n({val})'
                    elif 显示百分比:
                        return f'{pct:.1f}%'
                    elif 显示数值:
                        return f'{val}'
                    else:
                        return ''
                return my_autopct
            
            # 绘制饼图
            wedges, texts, autotexts = ax.pie(values_clean, 
                                            labels=labels_clean if not 显示图例 else None,
                                            autopct=make_autopct(values_clean) if (显示百分比 or 显示数值) else None,
                                            startangle=起始角度,
                                            explode=explode,
                                            colors=colors,
                                            textprops={'fontsize': 10})
            
            # 设置标题
            ax.set_title(标题, fontsize=14, fontweight='bold', pad=20)
            
            # 显示图例
            if 显示图例:
                ax.legend(wedges, labels_clean, title="类别", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
            
            # 确保饼图是圆形
            ax.axis('equal')
            
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
            ax.set_title('PieChart 错误', fontsize=14)
            
            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            buffer.close()
            plt.close(fig)
            
            return {"ui": {"data": [image_base64]}}