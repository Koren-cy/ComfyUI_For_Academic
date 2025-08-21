"""Top-level package for ComfyUI_For_Academic."""

__all__ = [
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS",
    "WEB_DIRECTORY",
]

__author__ = """BitWalker"""
__email__ = "koren.cai.cy@gmail.com"
__version__ = "0.1.0"

from .src.import_nodes import NODE_CLASS_MAPPINGS
from .src.import_nodes import NODE_DISPLAY_NAME_MAPPINGS

WEB_DIRECTORY = "./web"



import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'SimSun', 'Arial Unicode MS']  # 优先使用的中文字体列表
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
plt.rcParams['font.family'] = 'sans-serif'  # 使用无衬线字体


import os
import matplotlib as mpl

if os.name == 'nt':  # Windows系统
    mpl.rc('font', family='Microsoft YaHei')
else:  # 类Unix系统
    mpl.rc('font', family='Arial Unicode MS')
mpl.rcParams['axes.unicode_minus'] = False 



import json
import server
import traceback
from io import StringIO
from aiohttp import web
from .src.compiler import Compiler

if not hasattr(server.PromptServer.instance, '_comfyui_for_academic_routes_registered'):
    @server.PromptServer.instance.routes.post("/comfyui_for_academic_compile")
    async def comfyui_for_academic_compile(request):
        try:
            data = await request.json()
            workflow = json.loads(data["workflow"])

            sio = StringIO()
            Compiler(workflow=workflow, output_file=sio)

            sio.seek(0)
            data = sio.read()

            return web.Response(text=data, status=200)
        except Exception as e:
            traceback.print_exc()
            return web.Response(text=str(e), status=500)
    
    # 设置标志表示路由已注册
    server.PromptServer.instance._comfyui_for_academic_routes_registered = True
