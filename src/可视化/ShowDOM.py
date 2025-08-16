class ShowDOM:
    '''
    渲染HTML
    用于在ComfyUI界面中展示HTML内容
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "内容": ("STRING", {
                    "default": "<h1>Hello World</h1><p>This is <strong>HTML</strong> content.</p>",
                    "tooltip": "要显示的HTML内容"
                }),
            },
        }

    RETURN_TYPES = ()
    RETURN_NAMES = ()
    OUTPUT_NODE = True

    def process(self, 内容):
        # 处理输入的HTML内容
        processed_content = str(内容)
        
        # 返回处理后的内容，这将被发送到前端的DOM容器
        return {"ui": {"data": [processed_content]}}