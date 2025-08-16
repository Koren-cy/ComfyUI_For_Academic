import os, importlib, pathlib, inspect
from io import StringIO

class IPort_info:
    """输入端口信息类"""
    def __init__(self, port:tuple):
        port_value = port[1]

        self.name:str = port[0]
        self.link:list[str,int] = list()
        self.value:any = None
        self.is_widget:bool = False

        if isinstance(port_value, list):
            self.link = port_value
            self.is_widget = False
        else:
            self.value = port_value
            self.is_widget = True

    def get_var(self) -> str:
        if self.is_widget:
            return str([self.value])[1:-1]
        else:
            return f'_link_{self.link[0]}_{self.link[1]}'

class OPort_info:
    """输出端口信息类"""
    def __init__(self, name:str, link:list[str,int]):
        self.name:str = name
        self.link:list[str,int] = link

    def get_var(self) -> str:
        return f'_link_{self.link[0]}_{self.link[1]}'

class Node_info:
    """节点信息类，包含节点的所有属性和方法"""
    def __init__(self, node:tuple[str,dict]):
        inputs:dict = node[1]['inputs']

        self.id:str = node[0]
        self.type:str = node[1]['class_type']
        self.name:str = node[1]['_meta']['title']

        self.cls:any = None
        self.dependency:set[str] = set()
        self.deepth:int = None

        self.input_port:list[IPort_info] = list()
        for port in inputs.items():
            if '_widget' not in port[0]:
                self.input_port.append(IPort_info(port))

        self.output_port:list[OPort_info] = list()
    
    def parse_cls(self, cls:any, file_path:str) -> None:
        """解析节点类，提取依赖和输出端口信息"""
        self.cls = cls

        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        err_line = 0    
        for line in text.splitlines():
            if 'import' in line:
                self.dependency.add(line.strip())
            else:
                err_line += 1
                if err_line >= 3:
                    # 连续 3 行都没有import关键字
                    break
        
        for index, port_name in enumerate(cls.RETURN_NAMES):
            self.output_port.append(OPort_info(port_name,[self.id,index]))

    def get_links(self) -> list[list[str,str]]:
        """获取节点的连接关系"""
        return [[port.link[0],self.id] for port in self.input_port if not port.is_widget]

    def get_exec_code(self) -> str:
        """生成节点的执行代码"""

        input_code = ', '.join([f'{port.name}={port.get_var()}' for port in self.input_port])
        output_code = ', '.join([port.get_var() for port in self.output_port]) + (', ' if len(self.output_port) == 1 else '')
        func_code = 'process_local' if 'process_local' in self.cls.__dict__ else 'process'

        if output_code:
            return f'{output_code} = _node_{self.name}_{self.id}_.{func_code}({input_code})\n'
        else:
            return f'_node_{self.name}_{self.id}_.{func_code}({input_code})\n'
  
class Compiler():
    """编译器主类，负责将工作流转换为Python代码"""
    def __init__(self, workflow:dict, output_file:StringIO):
        # code section
        self.dependency_code:str = ''
        self.node_class_code:str = ''
        self.statement_code:str = ''
        self.main_code:str = ''

        self.nodes:list[Node_info] = list()
        for node in workflow.items():
            self.nodes.append(Node_info(node))

        self.prefix:str = 'ComfyUI_For_Academic'
        self.nodes_path:str = './'
        self.file_path:str = f'./custom_nodes/{self.prefix}/src'

        self.output_file:StringIO = output_file

        self.compile()

    def compile(self):
        """编译主流程"""
        self.import_nodes(prefix=self.prefix, nodes_path=self.nodes_path, file_path=self.file_path, nodes=self.nodes)
        self.mark_node_depth()
        self.handle_dependency()
        self.generate_node_class_code()
        self.generate_statement_code()
        self.generate_main_code()

        self.output_file.write(self.dependency_code)
        self.output_file.write('\n')
        self.output_file.write(self.node_class_code)
        self.output_file.write('\n')
        self.output_file.write(self.statement_code)
        self.output_file.write('\n')
        self.output_file.write(self.main_code)

    def import_nodes(self, prefix:str, nodes_path:str, file_path:str, nodes:list[Node_info]):
        """导入节点类并解析"""
        def is_python_file(path):
            """检查是否为有效的Python文件"""
            return (os.path.isfile(path) 
                    and os.path.splitext(path)[1] == '.py' 
                    and not '__' in pathlib.Path(path).stem)

        def is_valid_dir(path):
            """检查是否为有效的目录"""
            return (os.path.isdir(path) 
                    and not '__' in pathlib.Path(path).stem)

        def import_nodes_from_dir(dir):
            """从目录中递归导入节点"""
            script_dir = os.path.dirname(os.path.realpath(__file__))
            for file in os.listdir(os.path.join(script_dir,dir[2:])):
                rel_path = os.path.join(dir,file)
                full_path = os.path.join(script_dir,rel_path[2:])

                if is_python_file(full_path):
                    try:
                        module = importlib.import_module(
                            os.path.join(file_path,rel_path)
                            .replace('./','')
                            .replace('\\','.')
                            .replace('/','.')
                            .replace('.py',''))

                        for cls_name,cls in inspect.getmembers(module, inspect.isclass):
                            if cls_name != pathlib.Path(full_path).stem:
                                continue
                            
                            unique_name = f'{prefix}_{cls_name}'
                            
                            for node in nodes:
                                if node.type == unique_name:
                                    node.parse_cls(cls, full_path)

                    except Exception as e:
                        print(e)

                elif is_valid_dir(full_path):
                    import_nodes_from_dir(rel_path)

        import_nodes_from_dir(nodes_path)
    
    def mark_node_depth(self):
        """标记节点的执行深度，用于确定执行顺序"""
        for node in self.nodes:
            have_input_link = False
            for port in node.input_port:
                if not port.is_widget:
                    have_input_link = True
                    break
            if not have_input_link:
                node.deepth = 0
        
        links:list[list[str,str]] = list()
        for node in self.nodes:
            links.extend(node.get_links())
        
        while links:
            for link in links:
                start_node:Node_info = next(filter(lambda node: node.id == link[0], self.nodes))
                end_node:Node_info = next(filter(lambda node: node.id == link[1], self.nodes))
                if start_node.deepth is not None:
                    end_node.deepth = max(start_node.deepth + 1, end_node.deepth if end_node.deepth is not None else 0)
                    links.remove(link)

    def handle_dependency(self):
        """处理依赖包，生成自动安装代码"""
        dependency:set[str] = set()
        for node in self.nodes:
            dependency.update(node.dependency)
        self.dependency_code = '# 导入第三方依赖\n\n'
        self.dependency_code += f'''
import subprocess
import sys

while True:
    try:
        {'\n        '.join(dependency)}
        break
    except ImportError as e:
        missing_package = str(e).split("'")[1] if "'" in str(e) else str(e).split()[-1]
        package_map = {{
            "PIL": "Pillow", 
            "cv2": "opencv-python",
            "serial": "pyserial",
            "sklearn": "scikit-learn",
            "skimage": "scikit-image",
        }}
        install_name = package_map.get(missing_package, missing_package)
        subprocess.check_call([sys.executable, "-m", "pip", "install", install_name])

        '''

    def generate_node_class_code(self):
        """生成节点类定义代码"""
        history:set[str] = set()
        self.node_class_code = '# 导入本地节点\n\n'
        for node in self.nodes:
            if node.type not in history:
                self.node_class_code += inspect.getsource(node.cls)
                self.node_class_code += '\n'
            history.add(node.type)

    def generate_statement_code(self):
        """生成节点实例化代码"""
        self.statement_code = '# 实例化节点类\n\n'
        for node in self.nodes:
            self.statement_code += f'_node_{node.name}_{node.id}_ = {node.type[len(self.prefix) + 1:]}()\n'


    def generate_main_code(self):
        """生成主执行循环代码"""
        deepthes:list = sorted(list(set([node.deepth for node in self.nodes])))
        self.main_code = '# 主循环\n\n'
        self.main_code += 'while True:\n'
        for deepth in deepthes:
            self.main_code += '    ' + f'# 层深度 {deepth}\n'
            for node in self.nodes:
                if node.deepth == deepth:
                    self.main_code += '    ' + node.get_exec_code()
        self.main_code += '    ' + '\n'
        self.main_code += '    ' + '#break\n'