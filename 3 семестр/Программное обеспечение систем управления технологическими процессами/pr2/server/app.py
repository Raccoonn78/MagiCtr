from opcua import Server, ua
from datetime import datetime
import random
import time
from logger import logger
from DB import DB 

def sleeper():
    time.sleep(0.5)
    logger.info(f'...')
    time.sleep(0.2)
# Настройка базы данных SQLite для архивации
DB.query("""
CREATE TABLE IF NOT EXISTS signals (
    timestamp       DATETIME,
    signal_name     TEXT,
    value           REAL
)
""")
URL = "opc.tcp://0.0.0.0:4840/freeopcua/server/"

# Инициализация OPC UA сервера
server = Server()
server.set_endpoint(URL)
server.set_server_name("OPC UA Server Example")

# Создание структуры узлов
root_node = server.nodes.objects

# Node 4
node4 = root_node.add_object("ns=2;i=1001", "Node4")  # Уникальный NodeId для Node4
var_rw_bool = node4.add_variable("ns=2;i=2001", "Var_RW_H", False, ua.VariantType.Boolean)  # Уникальный NodeId
var_rw_bool.set_writable()

# Node 3
node3 = root_node.add_object("ns=2;i=1002", "Node3")  # Уникальный NodeId для Node3
var_r_int16 = node3.add_variable("ns=2;i=2002", "Var_R", 0, ua.VariantType.Int16)  # Уникальный NodeId
var_rwh_double = node3.add_variable("ns=2;i=2003", "Var_RW_H", 0.0, ua.VariantType.Double)  # Уникальный NodeId
var_rh_int8 = node3.add_variable("ns=2;i=2004", "Var_RH", 0, ua.VariantType.Byte)  # Уникальный NodeId

var_r_int16.set_read_only()
var_rwh_double.set_writable()

# Node 1 -> Node 2
node1 = root_node.add_object("ns=2;i=1003", "Node1")  # Уникальный NodeId для Node1
node2 = node1.add_object("ns=2;i=1004", "Node2")  # Уникальный NodeId для Node2
var_rh_int16 = node2.add_variable("ns=2;i=2005", "Var_RH", 0, ua.VariantType.Int16)  # Уникальный NodeId
var_rw_int64 = node2.add_variable("ns=2;i=2006", "Var_RW", 0, ua.VariantType.Int64)  # Уникальный NodeId

var_rh_int16.set_read_only()
var_rw_int64.set_writable()

# Функция обновления переменных
def update_signals():
    # Генерация случайных значений для переменных
    var_rw_bool.set_value(random.choice([True, False]))
    var_r_int16.set_value(random.randint(-32768, 32767))
    var_rwh_double.set_value(random.uniform(0, 100))
    var_rh_int8.set_value(random.randint(0, 255))  # Byte имеет диапазон от 0 до 255
    var_rh_int16.set_value(random.randint(-32768, 32767))
    var_rw_int64.set_value(random.randint(-9223372036854775808, 9223372036854775807))

    # Сохранение в базу данных (архивируемые переменные)
    timestamp = datetime.now()
    logger.info(f'\033[1;32;40mSTART...\033[1;37;40m')

    logger.info(f'\033[1;32;40mДобавление данных Var_RW_H в БД...\033[1;37;40m')
    sleeper()
    
    DB.query("INSERT INTO signals (timestamp, signal_name, value) VALUES (?, ?, ?)", 
                   (timestamp, "Var_RW_H", var_rw_bool.get_value()))
    
    logger.info(f'\033[1;32;40mДобавление данных Var_RW_H_double в БД...\033[1;37;40m')
    sleeper()
    
    DB.query("INSERT INTO signals (timestamp, signal_name, value) VALUES (?, ?, ?)", 
                   (timestamp, "Var_RW_H_double", var_rwh_double.get_value()))
    
    logger.info(f'\033[1;32;40mДобавление данных Var_RH_int8 в БД...\033[1;37;40m')
    sleeper()
    
    DB.query("INSERT INTO signals (timestamp, signal_name, value) VALUES (?, ?, ?)", 
                   (timestamp, "Var_RH_int8", var_rh_int8.get_value()))
    
    logger.info(f'\033[1;32;40mДобавление данных Var_RH_int16 в БД...\033[1;37;40m')
    sleeper()
    
    DB.query("INSERT INTO signals (timestamp, signal_name, value) VALUES (?, ?, ?)", 
                   (timestamp, "Var_RH_int16", var_rh_int16.get_value()))
    
    logger.info(f'\033[1;32;40mEND...\033[1;37;40m')
    sleeper()
    

# Запуск сервера
server.start()
print("Server started at {}".format(server.endpoint))

try:
    for i in range(3):
        update_signals()
        time.sleep(5)
    
except KeyboardInterrupt:
    logger.warning(f'\033[1;31;40m(∩ᄑ_ᄑ)⊃━☆ﾟ* STOPPING SERVER......ლ(ಠ_ಠ ლ)________(⊙_⊙)\033[1;37;40m')
finally:
    server.stop()
