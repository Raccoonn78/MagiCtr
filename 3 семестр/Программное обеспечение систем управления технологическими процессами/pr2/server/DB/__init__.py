import sqlite3
import time
from logger import logger
print(f"""\033[1;34;40m
╔╗──╔╗╔╗╔╗╔═══╗╔══╗╔╗╔╗╔══╗╔══╗─────╔══╗─╔╗──╔╗╔╗╔╗╔════╗╔═══╗╔╗╔╗╔╗╩╔╗
║║──║║║║║║║╔═╗║║╔╗║║║║║║╔╗║║╔╗║─────║╔╗║─║║──║║║║║║╚═╗╔═╝║╔═╗║║║║║║║─║║
║╚╗╔╝║║║║║║╚═╝║║║║║║╚╝║║║║║║╚╝╚╗────║║║║─║╚╗╔╝║║║║║──║║──║╚═╝║║║║║║║─║║
║╔╗╔╗║║║╔║║╔══╝║║║║║╔╗║║║║║║╔═╗║────║║║║─║╔╗╔╗║║║╔║──║║──║╔══╝║║╔║║║─╔║
║║╚╝║║║╚╝║║║───║╚╝║║║║║║╚╝║║╚═╝║───╔╝╚╝╚╗║║╚╝║║║╚╝║──║║──║║───║╚╝║║╚═╝║
╚╝──╚╝╚══╝╚╝───╚══╝╚╝╚╝╚══╝╚═══╝───╚════╝╚╝──╚╝╚══╝──╚╝──╚╝───╚══╝╚═══╝
\n
█──█─█──█─█───█─████─────████─████─────████─███
█──█─█─█──██─██─█──█─────█──█─█────────█──█───█
█─██─██───█─█─█─█──█─███─█──█─████─███───██─███
██─█─█─█──█───█─█──█─────█──█────█─────██─────█
█──█─█──█─█───█─████─────████─████─────████─███

""")
time.sleep(2)
print(f'\033[1;37;40m')
logger.info(f'\x1b[32 fЗапуск приложения')
time.sleep(2)

class DB():


    def __init__(self, engine=None) -> None:
        logger.info(f'\x1b[32Инициализация БазыДанных')
        self.conn = sqlite3.connect("DB/opcua_archive.db")
        engine = self.conn.cursor()
        self.__engine= engine
        ...

    @property
    def e(self):
        return self.__engine
    
    def query(self,  query:str,  args=None   ):
        
        if not args:
            response = self.e.execute(query )
        else:
            response = self.e.execute(query, args )
        self.conn.commit()
        return response

    def main(self):
        ...
    
    def __del__(self):
        self.e.close()

DB=DB()
