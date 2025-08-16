import cv2
import numpy as np
import base64
from io import BytesIO
from PIL import Image

class ShowImage:
    '''
    显示图片
    用于在ComfyUI界面中显示OpenCV格式的图片
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "图片输入": ("CVIMAGE", {
                    "tooltip": "要显示的OpenCV格式图片(ndarray)"
                }),
            },
        }

    RETURN_TYPES = ()
    RETURN_NAMES = ()
    OUTPUT_NODE = True

    def process(self, 图片输入):
        # 颜色空间转换
        if len(图片输入.shape) == 2:
            rgb_image = cv2.cvtColor(图片输入, cv2.COLOR_GRAY2RGB)
        elif 图片输入.shape[2] == 3:
            rgb_image = cv2.cvtColor(图片输入, cv2.COLOR_BGR2RGB)
        elif 图片输入.shape[2] == 4:
            rgb_image = cv2.cvtColor(图片输入, cv2.COLOR_BGRA2RGB)
        else:
            rgb_image = 图片输入  # 假设已经是RGB格式
        
        # 数据类型转换
        if rgb_image.dtype != np.uint8:
            if rgb_image.max() <= 1.0:
                rgb_image = (rgb_image * 255).astype(np.uint8)
            else:
                rgb_image = np.clip(rgb_image, 0, 255).astype(np.uint8)
        
        # 防止内存泄漏
        with BytesIO() as buffer:
            pil_image = Image.fromarray(rgb_image, 'RGB')
            pil_image.save(buffer, format='PNG')
            result = base64.b64encode(buffer.getvalue()).decode()
            pil_image.close()
            del pil_image
        
        return {"ui": {"data": [result]}}

    def process_local(self, 图片输入):
        cv2.imshow(f'Image_{id(self)}', 图片输入)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            import sys
            cv2.destroyAllWindows()
            sys.exit(0)