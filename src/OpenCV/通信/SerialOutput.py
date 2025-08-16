import serial
import json
import numpy as np

class SerialOutput:
    '''
    串口输出
    通过串口发送任意类型数据
    '''
    
    def __init__(self):
        self.serial_port = None
        self.last_port = None
        self.last_baudrate = None
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "数据输入": ("*", {
                    "tooltip": "要发送的数据，支持任意类型"
                }),
                "串口端口": ("STRING", {
                    "default": "COM3",
                    "tooltip": "串口端口名称"
                }),
                "波特率": (["9600", "19200", "38400", "57600", "115200", "230400", "460800", "921600"], {
                    "default": "115200",
                    "tooltip": "串口通信波特率"
                }),
                "数据格式": (["原始文本", "JSON格式", "十六进制"], {
                    "default": "原始文本",
                    "tooltip": "数据发送格式"
                }),
                "换行符": (["\\r\\n", "\\n", "\\r", "无"], {
                    "default": "\\r\\n",
                    "tooltip": "数据末尾添加的换行符"
                }),
                "时间戳": ("FLOAT", {
                    "default": "0.0",
                    "tooltip": "当前的时间戳"
                }),
            }
        }

    RETURN_TYPES = ("STRING", )
    RETURN_NAMES = ("发送状态", )
    OUTPUT_TOOLTIPS = ("发送状态信息", )

    def process(self, 数据输入, 串口端口, 波特率, 数据格式, 换行符, 时间戳):
        try:
            # 检查串口连接
            if not self._check_serial_connection(串口端口, int(波特率)):
                return ("串口连接失败", )
            
            # 转换数据为字符串
            data_str = self._convert_data_to_string(数据输入, 数据格式, 时间戳)
            
            # 添加换行符
            if 换行符 != "无":
                line_ending = 换行符.replace("\\r", "\r").replace("\\n", "\n")
                data_str += line_ending
            
            # 发送数据
            self.serial_port.write(data_str.encode('utf-8'))
            self.serial_port.flush()
            
            status_msg = f"已发送: {len(data_str)} 字节到 {串口端口}"
            return (status_msg, )
            
        except Exception as e:
            error_msg = f"串口发送错误: {str(e)}"
            print(error_msg)
            return (error_msg, )
    
    def _check_serial_connection(self, port, baudrate):
        """检查并建立串口连接"""
        try:
            # 如果端口或波特率改变，重新连接
            if (self.serial_port is None or 
                not self.serial_port.is_open or 
                self.last_port != port or 
                self.last_baudrate != baudrate):
                
                # 关闭现有连接
                if self.serial_port and self.serial_port.is_open:
                    self.serial_port.close()
                
                # 建立新连接
                self.serial_port = serial.Serial(
                    port=port,
                    baudrate=baudrate,
                    bytesize=serial.EIGHTBITS,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    timeout=1
                )
                
                self.last_port = port
                self.last_baudrate = baudrate
            
            return self.serial_port.is_open
            
        except Exception as e:
            print(f"串口连接错误: {e}")
            return False
    
    def _convert_data_to_string(self, data, format_type, timestamp):
        """将数据转换为字符串"""
        if format_type == "JSON格式":
            return self._to_json_string(data, timestamp)
        elif format_type == "十六进制":
            return self._to_hex_string(data)
        else:  # 原始文本
            return self._to_raw_string(data)
    
    def _to_json_string(self, data, timestamp):
        """转换为JSON格式字符串"""
        try:
            if isinstance(data, np.ndarray):
                # 对于numpy数组，转换为列表
                return json.dumps({
                    "type": "numpy_array",
                    "data": data.tolist(),
                    "shape": data.shape,
                    "dtype": str(data.dtype),
                    "timestamp": timestamp
                })
            else:
                return json.dumps({
                    "type": type(data).__name__,
                    "data": str(data),
                    "timestamp": timestamp
                })
        except Exception:
            return json.dumps({"error": "无法序列化数据"})
    
    def _to_hex_string(self, data):
        """转换为十六进制字符串"""
        try:
            if isinstance(data, (int, float)):
                return hex(int(data))
            elif isinstance(data, str):
                return data.encode('utf-8').hex()
            elif isinstance(data, np.ndarray):
                return ' '.join([hex(int(x)) for x in data.flatten()])
            else:
                return str(data).encode('utf-8').hex()
        except Exception:
            return "HEX_ERROR"
    
    def _to_raw_string(self, data):
        """转换为原始字符串"""
        try:
            return str(data)
        except Exception:
            return "STR_ERROR"
    
    def __del__(self):
        """析构函数，关闭串口连接"""
        if hasattr(self, 'serial_port') and self.serial_port and self.serial_port.is_open:
            self.serial_port.close()