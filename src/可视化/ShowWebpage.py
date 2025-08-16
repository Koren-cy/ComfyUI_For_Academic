class ShowWebpage:
    '''
    渲染网页
    用于在ComfyUI界面中展示指定URL的网页内容
    '''
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "网址": ("STRING", {
                    "default": "https://www.example.com",
                    "tooltip": "要渲染的网页URL地址"
                }),
            },
        }

    RETURN_TYPES = ()
    RETURN_NAMES = ()
    OUTPUT_NODE = True

    def process(self, 网址):
        # 处理输入的URL和尺寸参数
        url = str(网址).strip()
        
        # 确保URL有协议前缀
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        
        return {"ui": {"data": [url]}}