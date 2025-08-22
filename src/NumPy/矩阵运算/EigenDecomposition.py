import numpy as np

class EigenDecomposition:
    '''
    特征值分解
    计算方阵的特征值和特征向量
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "输入矩阵": ("NPARRAY", {
                    "tooltip": "要进行特征值分解的方阵"
                }),
            },
            "optional": {
                "排序方式": (["无排序", "特征值升序", "特征值降序", "特征值绝对值升序", "特征值绝对值降序"], {
                    "default": "特征值降序",
                    "tooltip": "特征值和特征向量的排序方式"
                }),
                "仅计算特征值": (["否", "是"], {
                    "default": "否",
                    "tooltip": "是否仅计算特征值（不计算特征向量，速度更快）"
                }),
            },
        }

    RETURN_TYPES = ("NPARRAY", "NPARRAY", "STRING")
    RETURN_NAMES = ("特征值", "特征向量", "分解信息")
    OUTPUT_TOOLTIPS = ("矩阵的特征值数组", "矩阵的特征向量矩阵（列向量）", "特征值分解的详细信息")

    def process(self, 输入矩阵, 排序方式="特征值降序", 仅计算特征值="否"):
        try:
            # 检查输入是否为方阵
            if 输入矩阵.ndim != 2:
                raise ValueError("输入必须是二维矩阵")
            
            if 输入矩阵.shape[0] != 输入矩阵.shape[1]:
                raise ValueError(f"输入必须是方阵，当前形状为 {输入矩阵.shape}")
            
            # 检查矩阵是否为空
            if 输入矩阵.size == 0:
                raise ValueError("输入矩阵不能为空")
            
            # 计算特征值和特征向量
            if 仅计算特征值 == "是":
                eigenvalues = np.linalg.eigvals(输入矩阵)
                eigenvectors = np.array([])  # 空数组
            else:
                eigenvalues, eigenvectors = np.linalg.eig(输入矩阵)
            
            # 排序特征值和特征向量
            if 排序方式 != "无排序" and eigenvalues.size > 0:
                eigenvalues, eigenvectors = self._sort_eigen(eigenvalues, eigenvectors, 排序方式, 仅计算特征值 == "是")
            
            # 生成分解信息
            decomp_info = self._generate_decomposition_info(eigenvalues, eigenvectors, 输入矩阵, 仅计算特征值 == "是")
            
            return (eigenvalues, eigenvectors, decomp_info)
            
        except np.linalg.LinAlgError as e:
            raise ValueError(f"特征值分解失败: {str(e)}")
        except ValueError as e:
            raise ValueError(f"特征值分解失败: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"特征值分解时发生未知错误: {str(e)}")
    
    def _sort_eigen(self, eigenvalues, eigenvectors, sort_method, values_only):
        """排序特征值和特征向量"""
        if sort_method == "特征值升序":
            idx = np.argsort(eigenvalues.real)
        elif sort_method == "特征值降序":
            idx = np.argsort(eigenvalues.real)[::-1]
        elif sort_method == "特征值绝对值升序":
            idx = np.argsort(np.abs(eigenvalues))
        elif sort_method == "特征值绝对值降序":
            idx = np.argsort(np.abs(eigenvalues))[::-1]
        else:
            return eigenvalues, eigenvectors
        
        sorted_eigenvalues = eigenvalues[idx]
        if not values_only and eigenvectors.size > 0:
            sorted_eigenvectors = eigenvectors[:, idx]
        else:
            sorted_eigenvectors = eigenvectors
        
        return sorted_eigenvalues, sorted_eigenvectors
    
    def _generate_decomposition_info(self, eigenvalues, eigenvectors, original_matrix, values_only):
        """生成特征值分解的详细信息"""
        info = []
        
        # 基本信息
        info.append(f"矩阵维度: {original_matrix.shape[0]}×{original_matrix.shape[1]}")
        info.append(f"特征值数量: {len(eigenvalues)}")
        
        # 特征值分析
        if len(eigenvalues) > 0:
            real_eigenvalues = eigenvalues.real
            imag_eigenvalues = eigenvalues.imag
            
            info.append(f"实特征值范围: [{np.min(real_eigenvalues):.6f}, {np.max(real_eigenvalues):.6f}]")
            
            # 复数特征值检查
            complex_count = np.sum(np.abs(imag_eigenvalues) > 1e-10)
            if complex_count > 0:
                info.append(f"复数特征值数量: {complex_count}")
                info.append("注意: 存在复数特征值，矩阵不是对称矩阵")
            else:
                info.append("所有特征值均为实数")
            
            # 零特征值检查
            zero_count = np.sum(np.abs(eigenvalues) < 1e-10)
            if zero_count > 0:
                info.append(f"零特征值数量: {zero_count}")
                info.append("矩阵是奇异的（不可逆）")
            else:
                info.append("矩阵是非奇异的（可逆）")
            
            # 条件数估计（基于特征值）
            if zero_count == 0:
                max_eigenval = np.max(np.abs(eigenvalues))
                min_eigenval = np.min(np.abs(eigenvalues))
                condition_number = max_eigenval / min_eigenval
                info.append(f"条件数估计: {condition_number:.2e}")
                
                if condition_number > 1e12:
                    info.append("警告: 条件数很大，矩阵接近奇异")
            
            # 特征值统计
            positive_count = np.sum(real_eigenvalues > 1e-10)
            negative_count = np.sum(real_eigenvalues < -1e-10)
            info.append(f"正特征值: {positive_count}, 负特征值: {negative_count}, 零特征值: {zero_count}")
            
            # 矩阵性质推断
            if complex_count == 0:
                if negative_count == 0 and zero_count == 0:
                    info.append("矩阵性质: 正定矩阵")
                elif positive_count == 0 and zero_count == 0:
                    info.append("矩阵性质: 负定矩阵")
                elif negative_count == 0:
                    info.append("矩阵性质: 半正定矩阵")
                elif positive_count == 0:
                    info.append("矩阵性质: 半负定矩阵")
                else:
                    info.append("矩阵性质: 不定矩阵")
        
        # 特征向量信息
        if not values_only and eigenvectors.size > 0:
            info.append(f"特征向量矩阵形状: {eigenvectors.shape}")
            info.append("特征向量以列向量形式存储")
        elif values_only:
            info.append("仅计算特征值，未计算特征向量")
        
        return "\n".join(info)