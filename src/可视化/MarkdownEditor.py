class MarkdownEditor:
    '''
    Markdown编辑器
    提供Markdown编辑和预览功能，可以输出编辑的Markdown代码
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "内容": ("STRING", {
                    "default": "# Markdown编辑器\n\n在这里编写你的**Markdown**内容。\n\n- 支持实时预览\n- 支持代码输出\n- 易于使用",
                    "tooltip": "编辑器的初始Markdown内容"
                }),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("markdown代码",)
    OUTPUT_NODE = True

    def process(self, 内容):
        # 处理输入的初始内容
        content = str(内容)
        
        # 返回初始内容和UI数据
        return {
            "ui": {"data": [content]},
            "result": (content,)
        }