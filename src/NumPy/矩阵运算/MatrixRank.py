import numpy as np

class MatrixRank:
    '''
    矩阵秩
    计算矩阵的秩（线性无关的行或列的最大数目）
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "输入矩阵": ("NPARRAY", {
                    "tooltip": "要计算秩的输入矩阵"
                }),
            },
            "optional": {
                "计算方法": (["SVD", "QR分解", "LU分解"], {
                    "default": "SVD",
                    "tooltip": "计算矩阵秩的方法"
                }),
                "容差": ("FLOAT", {
                    "default": -1.0,
                    "min": -1.0,
                    "max": 1.0,
                    "step": 1e-10,
                    "display": "number",
                    "tooltip": "判断奇异值为零的容差，-1表示自动选择"
                }),
                "Hermitian矩阵": (["否", "是"], {
                    "default": "否",
                    "tooltip": "输入矩阵是否为Hermitian矩阵（可提高计算效率）"
                }),
            },
        }

    RETURN_TYPES = ("INT", "NPARRAY", "STRING")
    RETURN_NAMES = ("矩阵秩", "奇异值", "秩信息")
    OUTPUT_TOOLTIPS = ("矩阵的秩", "用于计算秩的奇异值", "矩阵秩计算的详细信息")

    def process(self, 输入矩阵, 计算方法="SVD", 容差=-1.0, Hermitian矩阵="否"):
        try:
            # 检查输入
            if 输入矩阵.size == 0:
                raise ValueError("输入矩阵不能为空")
            
            hermitian = True if Hermitian矩阵 == "是" else False
            
            # 自动选择容差
            if 容差 < 0:
                # 使用机器精度的倍数作为默认容差
                tol = max(输入矩阵.shape) * np.finfo(输入矩阵.dtype).eps
            else:
                tol = 容差
            
            # 根据计算方法计算秩
            if 计算方法 == "SVD":
                rank, singular_values = self._rank_by_svd(输入矩阵, tol, hermitian)
            elif 计算方法 == "QR分解":
                rank, singular_values = self._rank_by_qr(输入矩阵, tol)
            elif 计算方法 == "LU分解":
                rank, singular_values = self._rank_by_lu(输入矩阵, tol)
            else:
                raise ValueError(f"未知的计算方法: {计算方法}")
            
            # 生成详细信息
            rank_info = self._generate_rank_info(输入矩阵, rank, singular_values, 计算方法, tol, hermitian)
            
            return (int(rank), singular_values, rank_info)
            
        except ValueError as e:
            raise ValueError(f"矩阵秩计算失败: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"矩阵秩计算时发生未知错误: {str(e)}")
    
    def _rank_by_svd(self, matrix, tol, hermitian=False):
        """使用SVD方法计算矩阵秩"""
        try:
            if hermitian and matrix.shape[0] == matrix.shape[1]:
                # 对于Hermitian矩阵，可以使用特征值分解
                eigenvalues = np.linalg.eigvals(matrix)
                singular_values = np.abs(eigenvalues)
            else:
                # 一般情况使用SVD
                singular_values = np.linalg.svd(matrix, compute_uv=False)
            
            # 计算秩
            rank = np.sum(singular_values > tol)
            
            return rank, singular_values
        except np.linalg.LinAlgError as e:
            raise ValueError(f"SVD计算失败: {str(e)}")
    
    def _rank_by_qr(self, matrix, tol):
        """使用QR分解计算矩阵秩"""
        try:
            # QR分解
            Q, R = np.linalg.qr(matrix)
            
            # R矩阵对角线元素的绝对值
            diag_R = np.abs(np.diag(R))
            
            # 计算秩
            rank = np.sum(diag_R > tol)
            
            # 为了保持一致性，也计算奇异值
            singular_values = np.linalg.svd(matrix, compute_uv=False)
            
            return rank, singular_values
        except np.linalg.LinAlgError as e:
            raise ValueError(f"QR分解计算失败: {str(e)}")
    
    def _rank_by_lu(self, matrix, tol):
        """使用LU分解计算矩阵秩"""
        try:
            from scipy.linalg import lu
            
            # LU分解
            P, L, U = lu(matrix)
            
            # U矩阵对角线元素的绝对值
            diag_U = np.abs(np.diag(U))
            
            # 计算秩
            rank = np.sum(diag_U > tol)
            
            # 为了保持一致性，也计算奇异值
            singular_values = np.linalg.svd(matrix, compute_uv=False)
            
            return rank, singular_values
        except ImportError:
            # 如果没有scipy，回退到SVD方法
            return self._rank_by_svd(matrix, tol)
        except Exception as e:
            raise ValueError(f"LU分解计算失败: {str(e)}")
    
    def _generate_rank_info(self, matrix, rank, singular_values, method, tol, hermitian):
        """生成矩阵秩计算的详细信息"""
        info = []
        
        # 基本信息
        info.append(f"矩阵形状: {matrix.shape}")
        info.append(f"计算方法: {method}")
        info.append(f"使用容差: {tol:.2e}")
        if hermitian:
            info.append("矩阵类型: Hermitian矩阵")
        
        # 秩信息
        info.append(f"矩阵秩: {rank}")
        max_possible_rank = min(matrix.shape)
        info.append(f"最大可能秩: {max_possible_rank}")
        
        # 矩阵性质分析
        if rank == 0:
            info.append("矩阵性质: 零矩阵")
        elif rank == max_possible_rank:
            if matrix.shape[0] == matrix.shape[1]:
                info.append("矩阵性质: 满秩方阵（可逆）")
            else:
                info.append("矩阵性质: 满秩矩阵")
        else:
            rank_deficiency = max_possible_rank - rank
            info.append(f"矩阵性质: 秩亏缺矩阵（亏缺度: {rank_deficiency}）")
            if matrix.shape[0] == matrix.shape[1]:
                info.append("矩阵性质: 奇异方阵（不可逆）")
        
        # 奇异值信息
        if len(singular_values) > 0:
            info.append(f"奇异值数量: {len(singular_values)}")
            info.append(f"最大奇异值: {np.max(singular_values):.6e}")
            info.append(f"最小奇异值: {np.min(singular_values):.6e}")
            
            # 有效奇异值（大于容差的）
            effective_sv = singular_values[singular_values > tol]
            if len(effective_sv) > 0:
                info.append(f"有效奇异值数量: {len(effective_sv)}")
                if len(effective_sv) < len(singular_values):
                    info.append(f"近零奇异值数量: {len(singular_values) - len(effective_sv)}")
            
            # 条件数
            if rank > 0 and np.min(singular_values) > 0:
                condition_number = np.max(singular_values) / np.min(singular_values)
                info.append(f"条件数: {condition_number:.2e}")
                
                if condition_number > 1e12:
                    info.append("数值稳定性: 病态矩阵，数值计算可能不稳定")
                elif condition_number > 1e6:
                    info.append("数值稳定性: 条件数较大，注意数值精度")
                else:
                    info.append("数值稳定性: 良好")
        
        # 线性代数意义
        if matrix.shape[0] == matrix.shape[1]:  # 方阵
            if rank == matrix.shape[0]:
                info.append("线性代数意义: 列向量线性无关，行向量线性无关")
            else:
                info.append(f"线性代数意义: 存在 {matrix.shape[0] - rank} 个线性相关的行/列向量")
        else:
            info.append(f"线性代数意义: {rank} 个线性无关的列向量")
        
        # 应用建议
        if rank < max_possible_rank:
            info.append("应用建议: 考虑使用正则化方法或伪逆求解线性系统")
        
        return "\n".join(info)