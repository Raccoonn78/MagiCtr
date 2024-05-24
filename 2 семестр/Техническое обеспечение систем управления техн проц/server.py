import socket
import struct
import logging
from logger_user import logs
import time
def connect_with_client():
    logs.info('Создание соедния')
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return server_socket

# Создание сокета TCP для сервера
def create_server():

    server_socket = connect_with_client()

    server_socket.bind(('localhost', 5020))  # Привязываем сокет к адресу и порту
    server_socket.listen(1)  # Ожидаем одно соединение

    logs.info("Ждем соединения с клиентом...")
    client_socket, client_address = server_socket.accept()# Принятие соединения от клиента
    logs.info(f"Соединение установлено с клиентом: {client_address}")




    # Словарь для хранения значений регистров
    registers = {
        10071: 0,
        14012: 0,
        21560: 0,
        21561: 0,
        21565: 0,
        21566: 0,
        30023: 0,
        30024: 0,
        30025: 0,
        30026: 0,
        30027: 0,
        30028: 0,
        44883: 0,
        44884: 0,
        44885: 0,
        44886: 0,
        44887: 0,
        44888: 0,
        44889: 0,
        44890: 0
    }
    # Словарь для хранения значений регистров (инициализируем дискретные входы и выходы)
    discrete_inputs = {
        10070: 1,
        14011: 0,
        21559: 0
    }

    discrete_outputs = {
        21560: 0,
        21561: 0,
        21565: 0,
        21566: 0
    }
    try:
        while True:
            # Чтение данных от клиента

            def get_data():
                return client_socket.recv(1024)
            data =  get_data()

            if not data:
                # for i in range(100):
                #     time.sleep(2)
                #     data =  get_data()
                    if data: break
            if not data: break
            # Обработка запроса клиента
            # Распаковка MBAP заголовка
            transaction_id, protocol_id, length, unit_id = struct.unpack('>HHHB', data[:7])

            # Распаковка PDU
            function_code = struct.unpack('B', data[7:8])[0]

            logs.info(function_code)
            if function_code == 2:  # Функция чтения дискретных входов
                # Отображение сообщения обмена Modbus на стороне сервера
                logs.info("Получен запрос на чтение дискретных входов от клиента")

                # Распаковка начального адреса и количества входов
                starting_address, quantity_of_inputs = struct.unpack('>HH', data[8:12])
                
                # Создание ответа
                byte_count = (quantity_of_inputs + 7) // 8
                response_mbap = struct.pack('>HHHB', transaction_id, protocol_id, 3 + byte_count, unit_id)
                response_pdu = struct.pack('BB', function_code, byte_count)
                
                # Считывание значений дискретных входов
                input_status = 0
                for i in range(quantity_of_inputs):
                    if discrete_inputs.get(starting_address + i, 0):
                        input_status |= (1 << i)
                
                response_data = struct.pack('B', input_status)
                
                # Полный ответ
                response = response_mbap + response_pdu + response_data
                
                # Отправка ответа клиенту
                client_socket.send(response)
                logs.info("Отправка ответа клиенту")

    finally:
        # Закрытие сокета
        client_socket.close()
        server_socket.close()
        return {'code':0}



if __name__ =='__main__':
    code= {'code':0}
    while code['code']==0:
        code= create_server()
        input_user=input('Введите что то ')
        if input_user =='0': break
        logs.warning(f'Создание нового подключения SERVER')
        




'''

Адрес: 10071	Функции: 0x2	Описание: Дискретный вход устройства. 
Адрес: 14012	Функции: 0x2	Описание: Дискретный вход устройства. 
Адрес: 14012	Функции: 0x2	Описание: Дискретный вход устройства. 
Адрес: 14012	Функции: 0x2	Описание: Дискретный вход устройства. 
Адрес: 14012	Функции: 0x2	Описание: Дискретный вход устройства. 
Адрес: 21560	Функции: 0x1 0x5 0xF	Описание: Дискретный выход устройства. 
Адрес: 21561	Функции: 0x1 0x5 0xF	Описание: Дискретный выход устройства. 
Адрес: 21565	Функции: 0x1 0x5 0xF	Описание: Дискретный выход устройства. 
Адрес: 21566	Функции: 0x1 0x5 0xF	Описание: Дискретный выход устройства. 
Адрес: 30023,30024	Функции:0x4	Описание: 32-битный вход устройства.  Последовательность байт: 1_0_3_2
Адрес: 30025,30026	Функции:0x4	Описание: 32-битный вход устройства.  Последовательность байт: 1_0_3_2
Адрес: 30027,30028	Функции:0x4	Описание: 32-битный вход устройства.  Последовательность байт: 1_0_3_2
Адрес: 44883,44884	Функции:0x3 0x6 0x10	Описание: 32-битный выход устройства.  Последовательность байт: 1_0_3_2
Адрес: 44885,44886	Функции:0x3 0x6 0x10	Описание: 32-битный выход устройства.  Последовательность байт: 1_0_3_2
Адрес: 44887,44888	Функции:0x3 0x6 0x10	Описание: 32-битный выход устройства.  Последовательность байт: 1_0_3_2
Адрес: 44889,44890	Функции:0x3 0x6 0x10	Описание: 32-битный выход устройства.  Последовательность байт: 1_0_3_2


'''