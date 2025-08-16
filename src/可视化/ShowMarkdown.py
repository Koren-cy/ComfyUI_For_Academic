class ShowMarkdown:
    '''
    渲染Markdown
    用于在ComfyUI中展示Markdown内容
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "内容": ("STRING", {
                    "default": "# Hello World\n\nThis is **markdown** content.",
                    "tooltip": "要显示的Markdown内容"
                }),
            },
        }

    RETURN_TYPES = ()
    RETURN_NAMES = ()
    OUTPUT_NODE = True

    def process(self, 内容):
        # 处理输入的Markdown内容
        processed_content = str(内容)
        
        # 返回处理后的内容，这将被发送到前端的DOM容器
        return {"ui": {"data": [processed_content]}}