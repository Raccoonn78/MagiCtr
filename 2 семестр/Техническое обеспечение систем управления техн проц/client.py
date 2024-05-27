import socket
import struct
import time
import logging
from logger_user import logs
from decorator import my_decorator
# Универсальная функция для распаковки ответа от сервера
# @my_decorator
def parse_modbus_response(response=0):
    # Распаковка MBAP заголовка
    transaction_id, protocol_id, length, unit_id = struct.unpack('>HHHB', response[:7])
    # Распаковка PDU
    function_code = struct.unpack('B', response[7:8])[0]

    if function_code in [1, 2, 3, 4]:
        byte_count = struct.unpack('B', response[8:9])[0]
        data = response[9:9 + byte_count]
    elif function_code in [5, 6, 15, 16]:
        address, value = struct.unpack('>HH', response[8:12])
        data = (address, value)
    else:
        raise ValueError("Unsupported function code")

    return transaction_id, protocol_id, length, unit_id, function_code, data




# Создание сокета TCP для клиента
# @my_decorator
def connect_with_server():
    logs.info('Создание соедния')
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# @my_decorator
def create_client():

    client_socket = connect_with_server()
    try:
        client_socket.connect(('localhost', 5020))  # Подключаемся к серверу
    except: return {'code':0}
    logs.info('Ждем соединение...')
    # client_socket.listen(1)  # Ожидаем одно соединение
    logs.info('Соединение создано')
    # Формирование запроса к серверу для чтения дискретного входа с адреса 10071
    try:
        while True:
            input_user=input('Введите что то ')
            if input_user =='0': return {'code':1}
            logging.warning(f'что то {input_user}')
            
            # Формирование MBAP заголовка
            transaction_id = 1  # Уникальный идентификатор транзакции
            protocol_id = 0     # Идентификатор протокола (всегда 0 для Modbus TCP)
            length = 6          # Длина PDU + Unit Identifier
            unit_id = 1         # Идентификатор устройства

            mbap_header = struct.pack('>HHHB', transaction_id, protocol_id, length, unit_id)
            # Формирование PDU
            function_code = 2  # Функция чтения дискретных входов
            starting_address = 10070  # Адрес 10071 в Modbus адресации
            quantity_of_inputs = 1  # Количество дискретных входов для чтения

            pdu = struct.pack('>BHH', function_code, starting_address, quantity_of_inputs)
            print('pdu ', pdu)
            request = mbap_header + pdu




            # request = struct.pack('>BBHHHH', 0, 2, 0, 10071, 1, 1)
            logs.info(request)
            
            
            
            # Отправка запроса на сервер
            client_socket.send(request)
            
            # Получение ответа от сервера
            response = client_socket.recv(1024)
            print('response  ', response)
            try:
                parsed_response = parse_modbus_response(response)
            except Exception as e: logs.error(e)
            logs.info('parsed_response  ', parsed_response)
            # Распаковка ответа
            logs.info(f'Распаковка ответа \n {response}')
            header = struct.unpack('>BB', response[:2])

            logs.info(header)
            logs.info(header[1])
            # Распаковка ответа
            transaction_id, protocol_id, length, unit_id, function_code, byte_count = struct.unpack('>HHHBB', response[:9])
            input_status = struct.unpack('B', response[9:10])[0]
            print(f"Значение дискретного входа: {input_status}")
            if header[1] == 2:  # Проверяем, что это ответ на запрос чтения дискретных входов
                values = struct.unpack('>' + 'B' * len(response[2:]), response[2:])
                logs.info("Значения дискретных входов:")
                for value in values:
                    print(value)
            else:
                logs.info("Ошибка: Неизвестный ответ от сервера")
            time.sleep(2)
    except:
        # Закрытие сокета
        client_socket.close()
        return {'code':0}
    finally:
        client_socket.close()

if __name__ =='__main__':
    code= {'code':0}
    while code['code']==0:
        code= create_client()
        if code['code']==1: 
            break
        logs.warning(f'Создание нового подключения CLIENT')
        
