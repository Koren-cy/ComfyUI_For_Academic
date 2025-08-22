import numpy as np

class MatrixSVD:
    '''
    奇异值分解
    对矩阵进行奇异值分解 A = U * Σ * V^T
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "输入矩阵": ("NPARRAY", {
                    "tooltip": "要进行奇异值分解的矩阵（可以是任意形状的2D矩阵）"
                }),
            },
            "optional": {
                "完整矩阵": (["是", "否"], {
                    "default": "否",
                    "tooltip": "是否计算完整的U和V矩阵（否则计算经济型SVD）"
                }),
                "仅计算奇异值": (["否", "是"], {
                    "default": "否",
                    "tooltip": "是否仅计算奇异值（不计算U和V矩阵，速度更快）"
                }),
                "排序方式": (["降序", "升序"], {
                    "default": "降序",
                    "tooltip": "奇异值的排序方式"
                }),
            },
        }

    RETURN_TYPES = ("NPARRAY", "NPARRAY", "NPARRAY", "STRING")
    RETURN_NAMES = ("U矩阵", "奇异值", "V转置矩阵", "分解信息")
    OUTPUT_TOOLTIPS = ("左奇异向量矩阵U", "奇异值数组", "右奇异向量转置矩阵V^T", "SVD分解的详细信息")

    def process(self, 输入矩阵, 完整矩阵="否", 仅计算奇异值="否", 排序方式="降序"):
        try:
            # 检查输入是否为2D矩阵
            if 输入矩阵.ndim != 2:
                raise ValueError("输入必须是二维矩阵")
            
            # 检查矩阵是否为空
            if 输入矩阵.size == 0:
                raise ValueError("输入矩阵不能为空")
            
            # 执行奇异值分解
            if 仅计算奇异值 == "是":
                # 仅计算奇异值
                singular_values = np.linalg.svd(输入矩阵, compute_uv=False)
                U = np.array([])  # 空数组
                Vt = np.array([])  # 空数组
            else:
                # 计算完整的SVD
                full_matrices = True if 完整矩阵 == "是" else False
                U, singular_values, Vt = np.linalg.svd(输入矩阵, full_matrices=full_matrices)
            
            # 排序奇异值和对应的向量
            if 排序方式 == "升序" and singular_values.size > 0:
                U, singular_values, Vt = self._sort_svd(U, singular_values, Vt, 仅计算奇异值 == "是")
            
            # 生成分解信息
            svd_info = self._generate_svd_info(输入矩阵, U, singular_values, Vt, 完整矩阵, 仅计算奇异值 == "是")
            
            return (U, singular_values, Vt, svd_info)
            
        except np.linalg.LinAlgError as e:
            raise ValueError(f"奇异值分解失败: {str(e)}")
        except ValueError as e:
            raise ValueError(f"奇异值分解失败: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"奇异值分解时发生未知错误: {str(e)}")
    
    def _sort_svd(self, U, singular_values, Vt, values_only):
        """按升序排列奇异值和对应的向量"""
        # 获取排序索引（升序）
        idx = np.argsort(singular_values)
        
        # 排序奇异值
        sorted_singular_values = singular_values[idx]
        
        if not values_only:
            # 排序对应的向量
            sorted_U = U[:, idx] if U.size > 0 else U
            sorted_Vt = Vt[idx, :] if Vt.size > 0 else Vt
        else:
            sorted_U = U
            sorted_Vt = Vt
        
        return sorted_U, sorted_singular_values, sorted_Vt
    
    def _generate_svd_info(self, original_matrix, U, singular_values, Vt, full_matrices, values_only):
        """生成SVD分解的详细信息"""
        info = []
        
        # 基本信息
        m, n = original_matrix.shape
        info.append(f"原矩阵形状: {m}×{n}")
        info.append(f"奇异值数量: {len(singular_values)}")
        
        # 奇异值分析
        if len(singular_values) > 0:
            info.append(f"最大奇异值: {np.max(singular_values):.6e}")
            info.append(f"最小奇异值: {np.min(singular_values):.6e}")
            
            # 条件数
            if np.min(singular_values) > 1e-15:
                condition_number = np.max(singular_values) / np.min(singular_values)
                info.append(f"条件数: {condition_number:.2e}")
                
                if condition_number > 1e12:
                    info.append("警告: 条件数很大，矩阵接近奇异")
            else:
                info.append("条件数: 无穷大（矩阵是奇异的）")
            
            # 矩阵秩估计
            tolerance = max(m, n) * np.finfo(singular_values.dtype).eps * np.max(singular_values)
            rank = np.sum(singular_values > tolerance)
            info.append(f"矩阵秩: {rank}")
            
            if rank < min(m, n):
                info.append(f"矩阵是秩亏缺的（满秩应为 {min(m, n)}）")
            else:
                info.append("矩阵是满秩的")
            
            # 能量分析（奇异值平方和）
            total_energy = np.sum(singular_values**2)
            info.append(f"总能量（Frobenius范数平方）: {total_energy:.6e}")
            
            # 主要奇异值分析
            if len(singular_values) > 1:
                energy_ratios = np.cumsum(singular_values**2) / total_energy
                # 找到包含90%能量的奇异值数量
                num_90_percent = np.argmax(energy_ratios >= 0.9) + 1
                info.append(f"包含90%能量的奇异值数量: {num_90_percent}")
                
                # 找到包含99%能量的奇异值数量
                num_99_percent = np.argmax(energy_ratios >= 0.99) + 1
                info.append(f"包含99%能量的奇异值数量: {num_99_percent}")
        
        # U和V矩阵信息
        if not values_only:
            if U.size > 0:
                info.append(f"U矩阵形状: {U.shape}")
                if full_matrices == "是":
                    info.append("U矩阵: 完整的正交矩阵")
                else:
                    info.append("U矩阵: 经济型（仅前r列）")
            
            if Vt.size > 0:
                info.append(f"V^T矩阵形状: {Vt.shape}")
                if full_matrices == "是":
                    info.append("V^T矩阵: 完整的正交矩阵")
                else:
                    info.append("V^T矩阵: 经济型（仅前r行）")
        else:
            info.append("仅计算奇异值，未计算U和V矩阵")
        
        # 应用建议
        info.append("\n应用建议:")
        if len(singular_values) > 0:
            if rank < min(m, n):
                info.append("- 适用于降维、数据压缩")
                info.append("- 可用于求解最小二乘问题")
            else:
                info.append("- 适用于矩阵求逆、线性方程组求解")
                info.append("- 可用于主成分分析")
        
        return "\n".join(info)