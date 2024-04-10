import socket
import struct
import time
# Создание сокета TCP для клиента
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 5020))  # Подключаемся к серверу

# Формирование запроса к серверу для чтения дискретного входа с адреса 10071
while True:
    request = struct.pack('>BBHHHH', 0, 2, 0, 10071, 1, 1)
    print(request)
    # Отправка запроса на сервер
    client_socket.send(request)
    print(2)
    # Получение ответа от сервера
    response = client_socket.recv(1024)
    print(3)
    # Распаковка ответа
    header = struct.unpack('>BB', response[:2])
    print(header)
    print(header[1])
    if header[1] == 2:  # Проверяем, что это ответ на запрос чтения дискретных входов
        values = struct.unpack('>' + 'B' * len(response[2:]), response[2:])
        print("Значения дискретных входов:")
        for value in values:
            print(value)
    else:
        print("Ошибка: Неизвестный ответ от сервера")
    time.sleep(2)
# Закрытие сокета
client_socket.close()

