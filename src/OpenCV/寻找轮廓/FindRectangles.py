import cv2
import numpy as np

class FindRectangles:
    '''
    寻找矩形轮廓
    通过多种几何判据严格的识别图像中的矩形轮廓
    '''
    
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "图像输入": ("CVIMAGE", {
                    "tooltip": "输入的openCV格式图像，建议使用二值化或边缘检测后的图像"
                }),
                "最小面积": ("INT", {
                    "default": 100,
                    "min": 100,
                    "max": 100000,
                    "step": 100,
                    "display": "number",
                    "tooltip": "矩形的最小面积阈值，过滤掉太小的矩形"
                }),
                "最大面积": ("INT", {
                    "default": 50000,
                    "min": 1000,
                    "max": 500000,
                    "step": 1000,
                    "display": "number",
                    "tooltip": "矩形的最大面积阈值，过滤掉太大的矩形"
                }),
                "近似精度": ("FLOAT", {
                    "default": 0.03,
                    "min": 0.005,
                    "max": 0.1,
                    "step": 0.005,
                    "display": "number",
                    "tooltip": "多边形近似的精度系数，值越小越精确"
                }),
                "最大长宽比": ("FLOAT", {
                    "default": 3.0,
                    "min": 1.0,
                    "max": 10.0,
                    "step": 0.5,
                    "display": "number",
                    "tooltip": "允许的最大长宽比，用于过滤过于狭长的矩形"
                }),
                "角度容差": ("FLOAT", {
                    "default": 15.0,
                    "min": 5.0,
                    "max": 45.0,
                    "step": 5.0,
                    "display": "number",
                    "tooltip": "矩形角度的容差范围（度），用于验证是否为规整矩形"
                }),
                "凸性检测": (["否", "是"], {
                    "default": "是",
                    "tooltip": "是否检测轮廓的凸性，矩形应该是凸多边形"
                }),
                "对角线容差": ("FLOAT", {
                    "default": 0.05,
                    "min": 0.01,
                    "max": 0.2,
                    "step": 0.01,
                    "display": "number",
                    "tooltip": "对角线长度差异的容差比例，矩形的两条对角线应该相等"
                }),
                "边缘平行度": ("FLOAT", {
                    "default": 10.0,
                    "min": 5.0,
                    "max": 30.0,
                    "step": 5.0,
                    "display": "number",
                    "tooltip": "对边平行度的角度容差（度），矩形的对边应该平行"
                }),
                "轮廓完整性": ("FLOAT", {
                    "default": 0.90,
                    "min": 0.7,
                    "max": 1.0,
                    "step": 0.05,
                    "display": "number",
                    "tooltip": "轮廓完整性阈值，检测轮廓是否足够完整"
                }),
                "绘制结果": (["否", "是"], {
                    "default": "是",
                    "tooltip": "是否在输出图像上绘制检测到的矩形"
                }),
            },
        }

    RETURN_TYPES = ("CVIMAGE", "INT", "LIST")
    RETURN_NAMES = ("图像输出", "矩形数量", "矩形坐标")
    OUTPUT_TOOLTIPS = ("绘制了矩形的图像", "检测到的矩形数量", "矩形的四个顶点坐标列表")

    def process(self, 图像输入, 最小面积, 最大面积, 近似精度, 最大长宽比, 角度容差, 凸性检测, 对角线容差, 边缘平行度, 轮廓完整性, 绘制结果):
        """主处理函数"""
        try:
            # 输入验证
            if 图像输入 is None:
                raise Exception("输入图像为空")
            
            # 图像预处理：转换为灰度图
            if len(图像输入.shape) == 3:
                gray_image = cv2.cvtColor(图像输入, cv2.COLOR_BGR2GRAY)
            else:
                gray_image = 图像输入.copy()
            
            # 寻找轮廓并检测矩形
            contours, _ = cv2.findContours(gray_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            rectangle_data = []
            
            for contour in contours:
                # 基础面积过滤
                area = cv2.contourArea(contour)
                if not (最小面积 <= area <= 最大面积):
                    continue
                
                # 多边形近似
                perimeter = cv2.arcLength(contour, True)
                epsilon = 近似精度 * perimeter
                approx = cv2.approxPolyDP(contour, epsilon, True)
                
                # 四边形检查
                if len(approx) != 4:
                    continue
                
                # 矩形验证
                if self._is_rectangle(approx, contour, 最大长宽比, 角度容差, 凸性检测, 对角线容差, 边缘平行度, 轮廓完整性):
                    coords = approx.reshape(-1, 2).tolist()
                    rectangle_data.append((area, approx, coords))
            
            # 按面积从大到小排序
            rectangle_data.sort(key=lambda x: x[0], reverse=True)
            
            # 提取结果数据
            rectangles = [data[1] for data in rectangle_data]
            rectangle_coords = [data[2] for data in rectangle_data]
            
            # 绘制结果
            result_image = 图像输入.copy()
            if len(result_image.shape) == 2:
                result_image = cv2.cvtColor(result_image, cv2.COLOR_GRAY2BGR)
            
            if 绘制结果 == "是" and rectangles:
                for rect in rectangles:
                    cv2.drawContours(result_image, [rect], -1, (0, 255, 0), 2)
                    for point in rect:
                        cv2.circle(result_image, tuple(point[0]), 5, (255, 0, 0), -1)
            
            return (result_image, len(rectangles), rectangle_coords)
            
        except Exception as e:
            print(f"寻找矩形轮廓错误: {e}")
            return (图像输入, 0, [])
    

    
    def _is_rectangle(self, approx, contour, max_aspect_ratio, angle_tolerance, check_convex, diagonal_ratio, parallel_tolerance, contour_integrity):
        """
        验证四边形是否为矩形
        使用多种判定依据确保识别的准确性
        """
        try:
            points = approx.reshape(-1, 2)

            # 凸性检测
            if check_convex == "是" and not cv2.isContourConvex(approx):
                return False
            
            # 计算四条边的长度
            sides = []
            for i in range(4):
                p1 = points[i]
                p2 = points[(i + 1) % 4]
                length = np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
                sides.append(length)
            
            # 检查对边是否相等
            tolerance = 0.1
            if not (abs(sides[0] - sides[2]) / max(sides[0], sides[2]) < tolerance and
                    abs(sides[1] - sides[3]) / max(sides[1], sides[3]) < tolerance):
                return False
            
            # 检查长宽比
            width = max(sides[0], sides[1])
            height = min(sides[0], sides[1])
            if max(width / height, height / width) > max_aspect_ratio:
                return False
            
            # 检查所有角度是否接近90度
            for i in range(4):
                p1 = points[i]
                p2 = points[(i + 1) % 4]
                p3 = points[(i + 2) % 4]
                
                v1 = p1 - p2
                v2 = p3 - p2
                
                cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
                cos_angle = np.clip(cos_angle, -1, 1)
                angle = np.degrees(np.arccos(cos_angle))
                
                if abs(angle - 90) > angle_tolerance:
                    return False
            
            # 对角线长度检测
            diagonal1 = np.sqrt((points[0][0] - points[2][0])**2 + (points[0][1] - points[2][1])**2)
            diagonal2 = np.sqrt((points[1][0] - points[3][0])**2 + (points[1][1] - points[3][1])**2)
            diagonal_diff = abs(diagonal1 - diagonal2) / max(diagonal1, diagonal2)
            if diagonal_diff > diagonal_ratio:
                return False
            
            # 边缘平行度检测
            edges = []
            for i in range(4):
                p1 = points[i]
                p2 = points[(i + 1) % 4]
                edge = p2 - p1
                edges.append(edge)
            
            for i in range(2):
                edge1 = edges[i]
                edge2 = edges[i + 2]
                
                dot_product = np.dot(edge1, edge2)
                norms = np.linalg.norm(edge1) * np.linalg.norm(edge2)
                if norms == 0:
                    continue
                
                cos_angle = abs(dot_product) / norms
                cos_angle = np.clip(cos_angle, 0, 1)
                angle = np.degrees(np.arccos(cos_angle))
                
                if min(angle, 180 - angle) > parallel_tolerance:
                    return False
            
            # 轮廓完整性检测
            original_perimeter = cv2.arcLength(contour, True)
            approx_perimeter = cv2.arcLength(approx, True)
            
            if original_perimeter == 0:
                return False
            
            integrity_ratio = approx_perimeter / original_perimeter
            if integrity_ratio < contour_integrity:
                return False
            
            return True
            
        except Exception:
            return False