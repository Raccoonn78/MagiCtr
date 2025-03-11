
import argparse
import logging

from pyModbusTCP.server import ModbusServer

# init logging
logging.basicConfig()
# parse args
parser = argparse.ArgumentParser()
parser.add_argument('-H', '--host', type=str, default='127.0.0.1', help='Host (default: localhost)')
parser.add_argument('-p', '--port', type=int, default=502, help='TCP port (default: 502)')
parser.add_argument('-d', '--debug', action='store_true', help='set debug mode')
args = parser.parse_args()
# logging setup
if args.debug:
    logging.getLogger('pyModbusTCP.server').setLevel(logging.DEBUG)
# start modbus server
print(args.host, args.port)
server = ModbusServer(host=args.host, port=args.port)
print('START')
server.start()
# 16550
# from opcua import Server
# from opcua import ua
# import time
# import random

# # Создание объекта сервера
# server = Server()

# # Устанавливаем конечную точку сервера
# server.set_endpoint("opc.tcp://192.168.56.1:55000/freeopcua/server/")  # Указываем ваш IP и порт 

# # Устанавливаем имя сервера
# server.set_server_name("OPC UA Server")

# # Настройка области (namespace) сервера
# uri = "urn:BurnerControl:Server"
# idx = server.register_namespace(uri)

# # Создание объекта, который будет содержать переменные
# objects = server.nodes.objects

# admin_object = objects.add_object(idx, "Admin Object")

# temp = admin_object.add_variable(idx, "temp", 30)
# temp.set_writable()  # Делаем переменную доступной для записи

# error_chance = admin_object.add_variable(idx, 'error_chance', 0)
# error_chance.set_writable()

# required_temperature = admin_object.add_variable(idx, 'required_temperature', 50)
# required_temperature.set_writable()

# min_temp = admin_object.add_variable(idx, 'min_temp', 20)
# min_temp.set_writable()

# burner_object = objects.add_object(idx, "Burner_Control")

# # Переменная для чтения: Состояние Горелки
# burner_state = burner_object.add_variable(idx, "Burner_State", False)  # Изначально выключена
# burner_state.set_writable()  # Доступна для записи

# # Переменная для клапана
# valve_state = burner_object.add_variable(idx, "Valve_State", False)  # Изначально клапан закрыт
# valve_state.set_writable()  # Доступна для записи

# # Запуск сервера
# server.start()
# print("Server started at {}".format(server.endpoint))

# try:
#     while True:
#         # Получаем текущее состояние горелки
#         current_burner_state = burner_state.get_value()
#         current_temp = temp.get_value()
#         req_temp = required_temperature.get_value()
#         min_t = min_temp.get_value()
#         err_chance = error_chance.get_value()
#         random_chance = random.randint(1, 100)  # Генерируем случайное число от 1 до 100
#         random_chance1 = random.randint(1, 100)

#         # Логика управления температурой
#         if current_burner_state:
#             if current_temp < 100:
#                 temp.set_value(current_temp + 2)  # Увеличиваем температуру
#         else:
#             if current_temp > 0:
#                 temp.set_value(current_temp - 1)  # Уменьшаем температуру

#         # Логика управления клапаном
#         if abs(current_temp - req_temp) <= 2 and err_chance <= random_chance:
#             valve_state.set_value(True)
#             while current_temp > min_t + 3:
#                 current_temp -= 3
#                 temp.set_value(current_temp)
#                 time.sleep(2)  # Пауза для плавного снижения температуры
#         else:
#             valve_state.set_value(False)

#         if err_chance >= random_chance1:
#             print("Error threshold exceeded. Stopping server.")
#             break

#         print(
#             f"current_temp: {current_temp}, current_burner_state: {current_burner_state}, req_temp: {req_temp}, min_temp: {min_t}, error_chance: {err_chance}, random_chance: {random_chance},random_chance1: {random_chance1} valve_state: {valve_state.get_value()}")

#         # Задержка для плавного изменения температуры
#         time.sleep(2)  # Уменьшаем задержку для более частого обновления

# except KeyboardInterrupt:
#     print("Server stopped manually")

# finally:
#     # Остановка сервера
#     server.stop()
#     print("Server stopped")
