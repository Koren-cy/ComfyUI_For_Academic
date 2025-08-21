import pandas as pd
from sqlalchemy import create_engine

class ImportPostgreSQL:
    """
    从PostgreSQL数据库读取数据
    """
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "主机": ("STRING", {
                    "multiline": False,
                    "default": "localhost"
                }),
                "端口": ("STRING", {
                    "multiline": False,
                    "default": "5432"
                }),
                "数据库名": ("STRING", {
                    "multiline": False,
                    "default": "postgres"
                }),
                "用户名": ("STRING", {
                    "multiline": False,
                    "default": "postgres"
                }),
                "密码": ("STRING", {
                    "multiline": False,
                    "default": ""
                }),
                "SQL查询": ("STRING", {
                    "multiline": True,
                    "default": "SELECT * FROM table_name;"
                }),
            },
        }

    RETURN_TYPES = ("DATAFRAME",)
    RETURN_NAMES = ("数据帧",)

    def process(self, 主机, 端口, 数据库名, 用户名, 密码, SQL查询):
        try:
            connection_string = f"postgresql://{用户名}:{密码}@{主机}:{端口}/{数据库名}"
            engine = create_engine(connection_string)
            dataframe = pd.read_sql_query(SQL查询.strip(), engine)
            engine.dispose()
            
            return (dataframe,)
            
        except Exception as e:
            print(f"连接PostgreSQL数据库时出错: {str(e)}")
            return (pd.DataFrame(),)