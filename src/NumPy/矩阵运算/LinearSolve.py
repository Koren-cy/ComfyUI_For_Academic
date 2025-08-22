import numpy as np

class LinearSolve:
    '''
    线性方程组求解
    求解 Ax = b 形式的线性方程组
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "系数矩阵A": ("NPARRAY", {
                    "tooltip": "线性方程组的系数矩阵A"
                }),
                "常数向量b": ("NPARRAY", {
                    "tooltip": "线性方程组的常数向量b"
                }),
            },
            "optional": {
                "求解方法": (["自动选择", "直接求解", "最小二乘", "SVD求解"], {
                    "default": "自动选择",
                    "tooltip": "求解方法选择"
                }),
                "正则化参数": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 1e-6,
                    "display": "number",
                    "tooltip": "岭回归正则化参数（仅在最小二乘方法中使用）"
                }),
            },
        }

    RETURN_TYPES = ("NPARRAY", "NPARRAY", "STRING")
    RETURN_NAMES = ("解向量x", "残差", "求解信息")
    OUTPUT_TOOLTIPS = ("线性方程组的解", "求解残差（b - Ax）", "求解过程的详细信息")

    def process(self, 系数矩阵A, 常数向量b, 求解方法="自动选择", 正则化参数=0.0):
        try:
            # 输入验证
            if 系数矩阵A.ndim != 2:
                raise ValueError("系数矩阵A必须是二维矩阵")
            
            if 常数向量b.ndim > 2:
                raise ValueError("常数向量b必须是一维或二维数组")
            
            # 确保b是正确的形状
            if 常数向量b.ndim == 1:
                if len(常数向量b) != 系数矩阵A.shape[0]:
                    raise ValueError(f"维度不匹配：A的行数({系数矩阵A.shape[0]}) != b的长度({len(常数向量b)})")
            else:
                if 常数向量b.shape[0] != 系数矩阵A.shape[0]:
                    raise ValueError(f"维度不匹配：A的行数({系数矩阵A.shape[0]}) != b的行数({常数向量b.shape[0]})")
            
            # 检查矩阵是否为空
            if 系数矩阵A.size == 0 or 常数向量b.size == 0:
                raise ValueError("输入矩阵或向量不能为空")
            
            # 根据方法求解
            if 求解方法 == "自动选择":
                solution, residual, solve_info = self._auto_solve(系数矩阵A, 常数向量b)
            elif 求解方法 == "直接求解":
                solution, residual, solve_info = self._direct_solve(系数矩阵A, 常数向量b)
            elif 求解方法 == "最小二乘":
                solution, residual, solve_info = self._least_squares_solve(系数矩阵A, 常数向量b, 正则化参数)
            elif 求解方法 == "SVD求解":
                solution, residual, solve_info = self._svd_solve(系数矩阵A, 常数向量b)
            else:
                raise ValueError(f"未知的求解方法: {求解方法}")
            
            return (solution, residual, solve_info)
            
        except np.linalg.LinAlgError as e:
            raise ValueError(f"线性方程组求解失败: {str(e)}")
        except ValueError as e:
            raise ValueError(f"线性方程组求解失败: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"线性方程组求解时发生未知错误: {str(e)}")
    
    def _auto_solve(self, A, b):
        """自动选择最适合的求解方法"""
        m, n = A.shape
        
        if m == n:
            # 方阵，尝试直接求解
            try:
                return self._direct_solve(A, b)
            except:
                # 如果直接求解失败，使用SVD
                return self._svd_solve(A, b)
        else:
            # 非方阵，使用最小二乘
            return self._least_squares_solve(A, b, 0.0)
    
    def _direct_solve(self, A, b):
        """直接求解（适用于方阵）"""
        if A.shape[0] != A.shape[1]:
            raise ValueError("直接求解方法仅适用于方阵")
        
        solution = np.linalg.solve(A, b)
        residual = b - np.dot(A, solution)
        
        info = f"求解方法: 直接求解\n"
        info += f"矩阵形状: {A.shape}\n"
        info += f"解的形状: {solution.shape}\n"
        info += f"残差范数: {np.linalg.norm(residual):.6e}"
        
        return solution, residual, info
    
    def _least_squares_solve(self, A, b, regularization):
        """最小二乘求解"""
        if regularization > 0:
            # 岭回归
            m, n = A.shape
            A_reg = np.vstack([A, np.sqrt(regularization) * np.eye(n)])
            if b.ndim == 1:
                b_reg = np.hstack([b, np.zeros(n)])
            else:
                b_reg = np.vstack([b, np.zeros((n, b.shape[1]))])
            solution, residuals, rank, s = np.linalg.lstsq(A_reg, b_reg, rcond=None)
        else:
            # 标准最小二乘
            solution, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)
        
        residual = b - np.dot(A, solution)
        
        info = f"求解方法: 最小二乘法\n"
        if regularization > 0:
            info += f"正则化参数: {regularization}\n"
        info += f"矩阵形状: {A.shape}\n"
        info += f"矩阵秩: {rank}\n"
        info += f"解的形状: {solution.shape}\n"
        info += f"残差范数: {np.linalg.norm(residual):.6e}\n"
        if len(residuals) > 0:
            info += f"最小二乘残差: {residuals[0]:.6e}"
        
        return solution, residual, info
    
    def _svd_solve(self, A, b):
        """SVD求解（适用于奇异或接近奇异的矩阵）"""
        U, s, Vt = np.linalg.svd(A, full_matrices=False)
        
        # 计算有效秩
        tolerance = max(A.shape) * np.finfo(s.dtype).eps * np.max(s)
        rank = np.sum(s > tolerance)
        
        # 使用伪逆求解
        s_inv = np.zeros_like(s)
        s_inv[:rank] = 1.0 / s[:rank]
        
        if b.ndim == 1:
            solution = np.dot(Vt.T, s_inv * np.dot(U.T, b))
        else:
            solution = np.dot(Vt.T, s_inv[:, np.newaxis] * np.dot(U.T, b))
        
        residual = b - np.dot(A, solution)
        
        info = f"求解方法: SVD求解\n"
        info += f"矩阵形状: {A.shape}\n"
        info += f"有效秩: {rank} / {min(A.shape)}\n"
        info += f"条件数: {s[0]/s[rank-1]:.2e}\n" if rank > 0 else "条件数: 无穷大\n"
        info += f"解的形状: {solution.shape}\n"
        info += f"残差范数: {np.linalg.norm(residual):.6e}"
        
        if rank < min(A.shape):
            info += "\n警告: 矩阵是秩亏缺的，解可能不唯一"
        
        return solution, residual, info