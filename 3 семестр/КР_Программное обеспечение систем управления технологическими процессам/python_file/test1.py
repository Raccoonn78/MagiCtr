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
 'Вытяжка': 20, # 20
 'Фильтр':25,  # 25
 'Вод_кал': 30,  # 30 
 'Вентилятор': 35, # 35 
     
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
        check_fan2 = store.getValues(3, 23, count=1)[0]        # вкл выкл вент (адрес 23)
        
        check_speed_fan = store.getValues(3, 12, count=1)[0]        # мощность вент (адрес 12)
        check_water_cal = store.getValues(3, 13, count=1)[0]        # мощность вод кал (адрес 13)
        check_filtr = store.getValues(3, 14, count=1)[0]        # вкл выкл фильтр (адрес 14)
        check_filtr2 = store.getValues(3, 22, count=1)[0]         # вкл выкл фильтр (адрес 22)
        temperature_user  = store.getValues(3, 21, count=1)[0]        #  Установить температуру (адрес 21) # int
        temperature_user_use  = store.getValues(3, 20, count=1)[0]        #  Установить температуру (адрес 20) # bool

        alarm_temperature = False
        alarm_humidity = False
        alarm_c_o_2 = False
        alarm_pressure = False
        alarm_airflow_speed = False


        went_error  = store.getValues(3, 29, count=1)[0] #  Вентиляция error 
        airflow_error  = store.getValues(3, 32, count=1)[0] # Вентилятор error 
        filtr_error  = store.getValues(3, 30, count=1)[0] # Фильтр error 
        whater_Cal_error  = store.getValues(3, 31, count=1)[0] # Вод кал error 
         

        print(f'went_error {went_error} {type(went_error)} filtr_error {filtr_error}  whater_Cal_error {whater_Cal_error}  airflow_error {airflow_error }    temperature_user {temperature_user} ')
        if temperature_user_use==1:
            temperature_user_use=True
        else:
            temperature_user_use=False
        
        
         
        sensor_failures['check_fan']=   True  if check_fan2 else False 
        sensor_failures['check_speed_fan']=   check_speed_fan
        sensor_failures['check_water_cal']=    check_water_cal
        sensor_failures['check_filtr']= True  if check_filtr2 else False #True  if isinstance(check_filtr, int) else check_filtr
        
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
            if temperature_user > temperature:
                sensor_failures['check_fan']= True   
                if check_speed_fan>40:
                    check_speed_fan=check_speed_fan-1
                elif check_speed_fan<40:
                    check_speed_fan=check_speed_fan+1
                sensor_failures['check_speed_fan']=   check_speed_fan
                if check_water_cal>40:
                    check_water_cal=check_water_cal-1
                elif check_water_cal<40:
                    check_water_cal=check_water_cal+1
                sensor_failures['check_water_cal']=    check_water_cal
                sensor_failures['check_filtr']= True   
                temperature =temperature +  1

                if humidity>40:
                    humidity =   humidity -1
                elif humidity<40:
                    humidity =   humidity +1
                if c_o_2>40:
                    c_o_2 =   c_o_2 -1
                elif c_o_2<40:
                    c_o_2 =   c_o_2 +1
                if pressure>40:
                    pressure =   pressure -1
                elif pressure<40:
                    pressure =   pressure +1
                if airflow_speed>40:
                    airflow_speed =   airflow_speed -1
                elif c_o_2<40:
                    airflow_speed =   airflow_speed +1 
            elif temperature_user < temperature:
                sensor_failures['check_fan']= True   
                if check_speed_fan<70:
                    check_speed_fan=check_speed_fan+1
                elif check_speed_fan>70:
                    check_speed_fan=check_speed_fan-1
                sensor_failures['check_speed_fan']=   check_speed_fan
                if check_water_cal<70:
                    check_water_cal=check_water_cal+1
                elif check_water_cal>70:
                    check_water_cal=check_water_cal-1
                sensor_failures['check_water_cal']=    check_water_cal
                sensor_failures['check_filtr']= True   
                temperature =temperature -  1

                if humidity>30:
                    humidity =   humidity -1
                elif humidity<40:
                    humidity =   humidity +1
                if c_o_2>30:
                    c_o_2 =   c_o_2 -1
                elif c_o_2<30:
                    c_o_2 =   c_o_2 +1
                if pressure>30:
                    pressure =   pressure -1
                elif pressure<30:
                    pressure =   pressure +1
                if airflow_speed>30:
                    airflow_speed =   airflow_speed -1
                elif c_o_2<30:
                    airflow_speed =   airflow_speed +1
        else:
            # sensor_failures['check_filtr']= False
            # sensor_failures['check_fan']= False   
            humidity =   humidity+ random.randint(1,7) if '+' == random.choice(["+","-"]) else humidity- random.randint(1,7)
            temperature =temperature + random.randint(1,7) if '+' == random.choice(["+","-"])  else temperature - random.randint(1,7)
            c_o_2 =   c_o_2 + random.randint(1,7)  if '+' == random.choice(["+","-"]) else  c_o_2 - random.randint(1,7)
            pressure =pressure + random.randint(1,7)  if '+' == random.choice(["+","-"]) else pressure - random.randint(1,7)
            airflow_speed =airflow_speed + random.randint(1,7) if '+' == random.choice(["+","-"]) else airflow_speed - random.randint(1,7)


        if temperature> 80 or temperature <10:
            alarm_temperature=True
        if humidity> 70 or humidity < 10:
            alarm_humidity=True
        if c_o_2> 50 or c_o_2 < 10:
            alarm_c_o_2=True
        if pressure> 60 or pressure < 10:
            alarm_pressure=True
        if airflow_speed> 80   :
            alarm_airflow_speed=True
          
        if went_error==1:
            print('dsffsdfsdfsdfsdf')
            store.setValues(3, 15, [True])
        else: 
            store.setValues(3, 15, [False])
         
        if filtr_error==1:
            store.setValues(3, 16, [True])
        else: 
            store.setValues(3, 16, [False])
         
        if whater_Cal_error==1:
            store.setValues(3, 17, [True])
        else: 
            store.setValues(3, 17, [False])
         
        if   airflow_error==1:
            store.setValues(3, 18, [True])
        else: 
            store.setValues(3, 18, [False])
        # Запись значений в Modbus
        store.setValues(3, 1, [humidity])           # Влажность (адрес 1)
        store.setValues(3, 2, [temperature])         # Температура (адрес 2)
        store.setValues(3, 4, [c_o_2])  # CO2 (адрес 4)
        store.setValues(3, 5, [pressure])  # Давление (адрес 5)
        store.setValues(3, 6, [airflow_speed])  # Скорость воздушного потока (адрес 6)
        store.setValues(3, 11, [sensor_failures['check_fan']])  # вкл выкл (адрес 11)
        store.setValues(3, 12, [sensor_failures['check_speed_fan']])  # мощность вент (адрес 12)
        store.setValues(3, 13, [sensor_failures['check_water_cal']])  # мощность вод кал (адрес 13)
        store.setValues(3, 14, [sensor_failures['check_filtr']])  # вкл выкл фильтр (адрес 14)
        store.setValues(3, 21, [temperature_user])  #  
        store.setValues(3, 20, [temperature_user_use])  #  
        
        store.setValues(3, 22, [check_filtr2])  #  


        store.setValues(3, 24, [alarm_temperature])  #  
        store.setValues(3, 25, [alarm_humidity])  #  
        store.setValues(3, 26, [alarm_c_o_2])  #  
        store.setValues(3, 27, [alarm_airflow_speed])  #      
        store.setValues(3, 28, [alarm_pressure])  #  
        

         


        print(  f"Влажность={humidity}%, Температура={temperature}°C, "
                f"CO2 {c_o_2}%, "
                f"Давление {pressure}мм рт. ст., "
                f"Скорость воздушного потока {airflow_speed}об/мин, "
                f"Заглушка {'открыта' if  sensor_failures['check_fan'] else 'закрыта'} {sensor_failures['check_fan']}, "
                f"Фильтр {'вкл' if  sensor_failures['check_filtr'] else 'выкл'} {sensor_failures['check_filtr']}, "
                f"check_filtr2 {check_filtr2} "
                f"скорость вод кал {check_water_cal}, "
                f"скорость вент{sensor_failures['check_speed_fan']}, "
                f"Errors: {sensor_failure_timers}, "
                f"temperature_user {temperature_user},"
                f"temperature_user_use {temperature_user_use}"
              )

        time.sleep(2)  # Обновление каждые 5 секунд

# Запускаем обновление данных в отдельном потоке
Thread(target=main_function, daemon=True,  args=(humidity_decrease_counter, ) ).start()

# Запускаем сервер
print("Modbus-TCP сервер запущен на 127.0.0.1:5020...")
StartTcpServer(context, address=("127.0.0.1", 5020))
