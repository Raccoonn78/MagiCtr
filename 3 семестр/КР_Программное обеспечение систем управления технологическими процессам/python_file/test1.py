import time
from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext, ModbusSequentialDataBlock
from threading import Thread
import random
from datetime import datetime

# Создаем таблицу регистров (100 значений) с правильной инициализацией
store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, [0] * 100),  # Дискретные входы
    co=ModbusSequentialDataBlock(0, [0] * 100),  # Катушки (битовые значения)
    hr=ModbusSequentialDataBlock(0, [50] * 100),  # 100 значений в Holding Registers
    ir=ModbusSequentialDataBlock(0, [0] * 100)  # Входные регистры
)

context = ModbusServerContext(slaves=store, single=True)


# Таймеры отказа датчиков
sensor_failure_timers = {
 '1': 20,
 '2': 25,
 '3': 30,
 '4': 35,
     
}
address_error = {
 '1': 15,
 '2': 16,
 '3': 17,
 '4': 18,
     
}

# Счетчик времени для плавного уменьшения влажности
humidity_decrease_counter = 0

# Флаги отказов датчиков
sensor_failures = {
    "humidity": False,
    "temperature": False,
    "irrigation": False,
    "ventilation": False,
    "check_fan":False,
    "check_speed_fan":60,
    "check_water_cal":60,
    "check_filtr":False
}

def main_function( humidity_decrease_counter ):

    while True:
        # Чтение значений из Modbus регистров
        humidity = store.getValues(3, 1, count=1)[0]        # Влажность (адрес 1)
        temperature = store.getValues(3, 2, count=1)[0]     # Температура (адрес 2)
        c_o_2 = store.getValues(3, 4, count=1)[0]           # CO2 (адрес 4)
        pressure = store.getValues(3, 5, count=1)[0]        # Давление (адрес 5)
        airflow_speed = store.getValues(3, 6, count=1)[0]        # Скорость воздушного потока (адрес 6)
        check_fan = store.getValues(3, 11, count=1)[0]        # вкл выкл вент (адрес 11)
        check_speed_fan = store.getValues(3, 12, count=1)[0]        # мощность вент (адрес 12)
        check_water_cal = store.getValues(3, 13, count=1)[0]        # мощность вод кал (адрес 13)
        check_filtr = store.getValues(3, 14, count=1)[0]        # вкл выкл фильтр (адрес 14)
        print(f'check_speed_fan {check_speed_fan}')
        print(f'check_water_cal {check_water_cal}')
        sensor_failures['check_fan']= True  if isinstance(check_fan, int) else check_fan
        sensor_failures['check_speed_fan']=   check_speed_fan
        sensor_failures['check_water_cal']=    check_water_cal
        sensor_failures['check_filtr']= True  if isinstance(check_fan, int) else check_filtr
        # sensor_failures['1']= True  if sensor_failure_timers['1']==0 else sensor_failure_timers['1']
        # sensor_failures['2']= True  if sensor_failure_timers['2']==0 else sensor_failure_timers['2']
        # sensor_failures['3']= True  if sensor_failure_timers['3']==0 else sensor_failure_timers['3']
        # sensor_failures['4']= True  if sensor_failure_timers['4']==0 else sensor_failure_timers['4']
        

        # Моделирование отказа датчиков
        for name, time_time in sensor_failure_timers.items():
            if sensor_failure_timers[name] > 0:
                sensor_failure_timers[name] -= 1
                store.setValues(3, address_error[name], [False])  # Сигнал об отказе
            elif sensor_failure_timers[name] == 0:
                store.setValues(3, address_error[name], [True])  # Сигнал об отказе


        humidity =   humidity+ random.randint(1,7) if '+' == random.choice(["+","-"]) else humidity- random.randint(1,7)
        temperature =temperature + random.randint(1,7) if '+' == random.choice(["+","-"])  else temperature - random.randint(1,7)
        c_o_2 =   c_o_2 + random.randint(1,7)  if '+' == random.choice(["+","-"]) else  c_o_2 - random.randint(1,7)
        pressure =pressure + random.randint(1,7)  if '+' == random.choice(["+","-"]) else pressure - random.randint(1,7)
        airflow_speed =airflow_speed + random.randint(1,7) if '+' == random.choice(["+","-"]) else airflow_speed - random.randint(1,7)
     

        # Запись значений в Modbus
        store.setValues(3, 1, [humidity])           # Влажность (адрес 1)
        store.setValues(3, 2, [temperature])         # Температура (адрес 2)
        store.setValues(3, 4, [c_o_2])  # CO2 (адрес 4)
        store.setValues(3, 5, [pressure])  # Давление (адрес 5)
        store.setValues(3, 6, [airflow_speed])  # Скорость воздушного потока (адрес 6)
        store.setValues(3, 11, [sensor_failures['check_fan']])  # вкл выкл (адрес 11)
        store.setValues(3, 12, [sensor_failures['check_speed_fan']])  # вкл выкл (адрес 12)
        store.setValues(3, 13, [sensor_failures['check_water_cal']])  # вкл выкл (адрес 13)
        store.setValues(3, 14, [sensor_failures['check_filtr']])  # вкл выкл (адрес 14)

        print(f"Влажность={humidity}%, Температура={temperature}°C, "
              f"CO2 {c_o_2}%, "
              f"Давление {pressure}мм рт. ст., "
              f"Скорость воздушного потока {airflow_speed}об/мин, "
              f"Заглушка {'открыта' if  sensor_failures['check_fan'] else 'закрыта'} {sensor_failures['check_fan']}, "
              f"Фильтр {'вкл' if  sensor_failures['check_filtr'] else 'выкл'} {sensor_failures['check_fan']}, "
              f"скорость вод кал {check_water_cal}, "
              f"скорость вент{sensor_failures['check_speed_fan']}, "
              f"Errors: {sensor_failure_timers}"
              )

        time.sleep(2)  # Обновление каждые 5 секунд

# Запускаем обновление данных в отдельном потоке
Thread(target=main_function, daemon=True,  args=(humidity_decrease_counter, ) ).start()

# Запускаем сервер
print("Modbus-TCP сервер запущен на 127.0.0.1:5020...")
StartTcpServer(context, address=("127.0.0.1", 5020))
