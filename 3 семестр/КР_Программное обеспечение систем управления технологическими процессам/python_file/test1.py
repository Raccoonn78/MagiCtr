import time
from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext, ModbusSequentialDataBlock
from threading import Thread
import random
from datetime import datetime
#выводить журнал  + (реализовать верхние\нижние предупредительные и аварийные уставки)
# добавить второго пользователя 
# первый этаж - стартовый 
# добавить звук 
# лист дейсвтий пользователя 
# журнал аварий
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
 'Вытяжка': 20,
 'Фильтр': 25,
 'Вод_кал': 30,
 'Вентилятор': 35,
     
}
address_error = {
 'Вытяжка': 15,
 'Фильтр': 16,
 'Вод_кал': 17,
 'Вентилятор': 18,
     
}
address_error_status = {
 'Вытяжка': False,
 'Фильтр': False,
 'Вод_кал': False,
 'Вентилятор': False,
     
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
local_state= {}

logs_actions= []
logs_system=[]
logs_errors =[]
 
 
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

        temperature_user  = store.getValues(3, 19, count=1)[0]        #  Установить температуру (адрес 19) # int
        temperature_user_use  = store.getValues(3, 20, count=1)[0]        #  Установить температуру (адрес 20) # bool

         
        
         

        sensor_failures['check_fan']= True  if isinstance(check_fan, int) else check_fan
        sensor_failures['check_speed_fan']=   check_speed_fan
        sensor_failures['check_water_cal']=    check_water_cal
        sensor_failures['check_filtr']= True  if isinstance(check_fan, int) else check_filtr
        
        local_state ={      'Вытяжка':                      sensor_failures['check_fan'],
                            'мощность вент':                sensor_failures['check_speed_fan'],
                            'мощность вод кал':             sensor_failures['check_water_cal'],
                            'Вкл/Выкл фильтр':              sensor_failures['check_filtr'],
                            'Time':str(datetime.now())
                    }
        if logs_system and temperature_user_use:
            temp = logs_system[-1]
            if list(temp.values()) != list(local_state.values()):
                logs_system.append(local_state)
        else:
            logs_system.append(local_state)
        

        # Моделирование отказа датчиков
        for name, time_time in sensor_failure_timers.items():
            if sensor_failure_timers[name] > 0:
                sensor_failure_timers[name] -= 1
                store.setValues(3, address_error[name], [False])  # Сигнал об отказе
            elif sensor_failure_timers[name] == 0:
                store.setValues(3, address_error[name], [True])  # Сигнал об отказе
                address_error_status[name]=True
                logs_errors.append( address_error |  { 'Time':str(datetime.now())}  )

        if temperature_user_use and temperature_user: # если пользовательская настройка
            humidity =   humidity+ random.randint(1,7) if '+' == random.choice(["+","-"]) else humidity- random.randint(1,7)
            temperature =temperature + random.randint(1,7) if '+' == random.choice(["+","-"])  else temperature - random.randint(1,7)
            c_o_2 =   c_o_2 + random.randint(1,7)  if '+' == random.choice(["+","-"]) else  c_o_2 - random.randint(1,7)
            pressure =pressure + random.randint(1,7)  if '+' == random.choice(["+","-"]) else pressure - random.randint(1,7)
            airflow_speed =airflow_speed + random.randint(1,7) if '+' == random.choice(["+","-"]) else airflow_speed - random.randint(1,7)
        else:
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
        
        logs_system.append({
                            'Влажность':                    humidity,
                            'Температура':                  temperature,
                            'CO2':                          c_o_2,
                            'Давление':                     pressure,
                            'Скорость воздушного потока':   airflow_speed,
                            'Вытяжка':                      sensor_failures['check_fan'],
                            'мощность вент':                sensor_failures['check_speed_fan'],
                            'мощность вод кал':             sensor_failures['check_water_cal'],
                            'вкл выкл фильтр':              sensor_failures['check_filtr'],
                            'Time':str(datetime.now())
                            })


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
