import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import base64
from io import BytesIO
import matplotlib
from matplotlib.patches import Rectangle, FancyBboxPatch
from matplotlib.collections import LineCollection

# 设置matplotlib后端为非交互式
matplotlib.use('Agg')

class SankeyDiagram:
    '''
    桑基图
    使用Matplotlib绘制桑基图，用于流量数据可视化
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "数据": ("DATAFRAME", {
                    "tooltip": "输入的DataFrame数据，需要包含源节点、目标节点和流量值"
                }),
                "源节点列名": ("STRING", {
                    "default": "",
                    "tooltip": "源节点的列名"
                }),
                "目标节点列名": ("STRING", {
                    "default": "",
                    "tooltip": "目标节点的列名"
                }),
                "流量列名": ("STRING", {
                    "default": "",
                    "tooltip": "流量值的列名"
                }),
            },
            "optional": {
                "标题": ("STRING", {
                    "default": "桑基图",
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
                "节点宽度": ("FLOAT", {
                    "default": 0.1,
                    "min": 0.05,
                    "max": 0.3,
                    "step": 0.01,
                    "tooltip": "节点的宽度比例"
                }),
                "流量透明度": ("FLOAT", {
                    "default": 0.6,
                    "min": 0.1,
                    "max": 1.0,
                    "step": 0.1,
                    "tooltip": "流量线的透明度"
                }),
                "节点颜色": ("STRING", {
                    "default": "lightblue",
                    "tooltip": "节点的颜色"
                }),
                "流量颜色方案": (["viridis", "plasma", "inferno", "magma", "rainbow", "coolwarm"], {
                    "default": "viridis",
                    "tooltip": "流量线的颜色方案"
                }),
                "显示数值": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "是否在节点上显示数值"
                }),
                "字体大小": ("INT", {
                    "default": 10,
                    "min": 6,
                    "max": 16,
                    "tooltip": "文字的字体大小"
                }),
            },
        }

    RETURN_TYPES = ()
    RETURN_NAMES = ()
    OUTPUT_NODE = True

    def _calculate_node_positions(self, nodes, flows):
        """计算节点位置"""
        # 简化的布局算法：左右两列
        source_nodes = set(flows['source'])
        target_nodes = set(flows['target'])
        
        # 只在源节点中出现的节点放在左侧
        left_nodes = source_nodes - target_nodes
        # 只在目标节点中出现的节点放在右侧
        right_nodes = target_nodes - source_nodes
        # 既是源又是目标的节点放在中间
        middle_nodes = source_nodes & target_nodes
        
        positions = {}
        
        # 左侧节点
        if left_nodes:
            for i, node in enumerate(sorted(left_nodes)):
                positions[node] = (0.1, (i + 1) / (len(left_nodes) + 1))
        
        # 中间节点
        if middle_nodes:
            for i, node in enumerate(sorted(middle_nodes)):
                positions[node] = (0.5, (i + 1) / (len(middle_nodes) + 1))
        
        # 右侧节点
        if right_nodes:
            for i, node in enumerate(sorted(right_nodes)):
                positions[node] = (0.9, (i + 1) / (len(right_nodes) + 1))
        
        return positions

    def _draw_flow(self, ax, source_pos, target_pos, value, max_value, color, alpha):
        """绘制流量线"""
        # 计算流量线宽度
        width = (value / max_value) * 0.1
        
        # 创建贝塞尔曲线路径
        x1, y1 = source_pos
        x2, y2 = target_pos
        
        # 控制点
        cx1 = x1 + 0.2
        cx2 = x2 - 0.2
        
        # 生成曲线点
        t = np.linspace(0, 1, 100)
        x = (1-t)**3 * x1 + 3*(1-t)**2*t * cx1 + 3*(1-t)*t**2 * cx2 + t**3 * x2
        y = (1-t)**3 * y1 + 3*(1-t)**2*t * y1 + 3*(1-t)*t**2 * y2 + t**3 * y2
        
        # 绘制流量带
        for i in range(len(x)-1):
            ax.plot([x[i], x[i+1]], [y[i], y[i+1]], color=color, 
                   linewidth=width*100, alpha=alpha, solid_capstyle='round')

    def process(self, 数据, 源节点列名="", 目标节点列名="", 流量列名="", 标题="桑基图", 
                图像宽度=12, 图像高度=8, 节点宽度=0.1, 流量透明度=0.6, 节点颜色="lightblue", 
                流量颜色方案="viridis", 显示数值=True, 字体大小=10):
        try:
            # 获取列名
            columns = 数据.columns.tolist()
            
            if len(columns) < 3:
                raise ValueError("数据至少需要3列：源节点、目标节点、流量值")
            
            # 确定源节点、目标节点和流量列
            if 源节点列名 and 源节点列名 in columns:
                source_col = 源节点列名
            else:
                source_col = columns[0]
            
            if 目标节点列名 and 目标节点列名 in columns:
                target_col = 目标节点列名
            else:
                target_col = columns[1]
            
            if 流量列名 and 流量列名 in columns:
                value_col = 流量列名
            else:
                # 找到第一个数值列
                numeric_cols = 数据.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 0:
                    value_col = numeric_cols[0]
                else:
                    value_col = columns[2]
            
            # 准备数据
            flows = pd.DataFrame({
                'source': 数据[source_col],
                'target': 数据[target_col],
                'value': pd.to_numeric(数据[value_col], errors='coerce')
            }).dropna()
            
            if flows.empty:
                raise ValueError("没有有效的流量数据")
            
            # 获取所有节点
            all_nodes = set(flows['source']) | set(flows['target'])
            
            # 计算节点位置
            node_positions = self._calculate_node_positions(all_nodes, flows)
            
            # 计算节点大小（基于流入流出总量）
            node_values = {}
            for node in all_nodes:
                inflow = flows[flows['target'] == node]['value'].sum()
                outflow = flows[flows['source'] == node]['value'].sum()
                node_values[node] = max(inflow, outflow)
            
            # 创建图形
            fig, ax = plt.subplots(figsize=(图像宽度, 图像高度))
            
            # 设置颜色映射
            max_flow = flows['value'].max()
            cmap = plt.get_cmap(流量颜色方案)
            norm = plt.Normalize(vmin=flows['value'].min(), vmax=max_flow)
            
            # 绘制流量线
            for _, row in flows.iterrows():
                source_pos = node_positions[row['source']]
                target_pos = node_positions[row['target']]
                color = cmap(norm(row['value']))
                
                self._draw_flow(ax, source_pos, target_pos, row['value'], 
                              max_flow, color, 流量透明度)
            
            # 绘制节点
            max_node_value = max(node_values.values()) if node_values else 1
            for node, pos in node_positions.items():
                # 节点大小基于流量值
                size = (node_values.get(node, 0) / max_node_value) * 0.15 + 0.05
                
                # 绘制节点矩形
                rect = FancyBboxPatch(
                    (pos[0] - 节点宽度/2, pos[1] - size/2),
                    节点宽度, size,
                    boxstyle="round,pad=0.01",
                    facecolor=节点颜色,
                    edgecolor='black',
                    linewidth=1
                )
                ax.add_patch(rect)
                
                # 添加节点标签
                ax.text(pos[0], pos[1], str(node), ha='center', va='center', 
                       fontsize=字体大小, fontweight='bold')
                
                # 显示数值
                if 显示数值 and node in node_values:
                    ax.text(pos[0], pos[1] - size/2 - 0.05, 
                           f'{node_values[node]:.1f}', 
                           ha='center', va='top', fontsize=字体大小-2)
            
            # 设置坐标轴
            ax.set_xlim(-0.1, 1.1)
            ax.set_ylim(-0.1, 1.1)
            ax.set_aspect('equal')
            ax.axis('off')
            
            # 设置标题
            ax.set_title(标题, fontsize=16, fontweight='bold', pad=20)
            
            # 添加颜色条
            sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
            sm.set_array([])
            cbar = plt.colorbar(sm, ax=ax, shrink=0.6)
            cbar.set_label('流量值', rotation=270, labelpad=15)
            
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
            ax.set_title('SankeyDiagram 错误', fontsize=14)
            
            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            buffer.close()
            plt.close(fig)
            
            return {"ui": {"data": [image_base64]}}