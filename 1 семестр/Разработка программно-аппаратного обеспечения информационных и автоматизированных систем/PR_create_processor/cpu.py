from time import time
import time
import pprint
from termcolor import colored, cprint
from colored import fg
from art import *


    

class CPU:
    """
    Гарвардкая архитектура:
        - характероне её отличие в том что памаять разделена на две части, одна для программы другая для данных

        Такой подход стабильнее, но не перезаписываем
    """
   
    CONTROL_NUMBER= 'CONTROL_NUMBER'#  0x5  #  5
    COMPARISON= 'COMPARISON' # 0x12  # 12
    ADDW= 'ADDW'#  0x11  # 11
    WRITE_ONE_READ= 'WRITE_ONE_READ'#  0x3 # 3
    WRITE_DOUBLE_READ= 'WRITE_DOUBLE_READ'#  0x2  # 2
    WRITE_MEMMORY= 'WRITE_MEMMORY'#  0x7   # 7
    MEM_DATA ='MEM_DATA'#  0x100 # запись числа в память
    
  
    write_double_read  =2  
    write_one_read  =3 
    control_number  =5  
    write_mem = 7  
    comparison  =12 
    addw  =11 
    mem_data  =100
    """
    -- Ответ будет в ячейки <99>
    -- gромежуточный ответ в <91> 
    -- Cчетчик будет в ячейке <90>
    -- Ёще один счетчик в <89> ( сколько всего элементов )
    -- Переход на нужную команду в <88>
    
    MEM_DATA 0 3                    # Запись данных
    MEM_DATA 1 3                    # Запись данных
    MEM_DATA 2 10                   # Запись данных
    MEM_DATA 3 2                    # Запись данных
    WRITE_MEMMORY 99 0              # запись числа в память
    WRITE_MEMMORY 90 0              # запись числа в память
    WRITE_MEMMORY 91 0              # запись числа в память
    WRITE_MEMMORY 92 0              # запись числа в память
    WRITE_MEMMORY 89 0              # запись числа в память
    WRITE_MEMMORY 88 8              # запись числа в память
    WRITE_ONE_READ 89 0             # запись числа в <89> из ячейки <0>  
    WRITE_ONE_READ 99 1             # запись числа в <99> из ячейки <1>  
    ADDW  90 1                      #  увеличивает число из <90> на 1 
    WRITE_DOUBLE_READ 91 90         # запись числа в 91 из значения полученного в ячейки <90>
                                    # пример: a = [2,1,100]    a[a[2]] >> a[2]==2 >> a[2] ==100 
    COMPARISON 91 99                # если число в <91> больше чем в <99> перезаписываем <99> ячейку значением из <91>
    CONTROL_NUMBER 90 1             # если число из ячейки <90> меньше чем число в ячейки <89> 
                                    # то 'pc' становится значением из ячейки <88>  
    
                                    


                                    
    регистры общего назначения 

    """

    def __init__(self):
        self.acc = 0  # Аккумулятор
        self.pc = 0  # счетчик регистра
        self.instr = 0  # регистр инструкций
        self.cycle_time_in_ms = 500
        self.MAX_MEM = 100
        self.zero_flag = True
        self.pos_flag = True
        self.cycle_time_in_ms = 500
        self.mem_prog = []  # память для программы
        self.mem_data = []  # память для данных
        self.halted = False
        self.debug = False


    def memmory_programm(self):  # создаем память для программы
        for i in range(self.MAX_MEM):
            self.mem_prog.insert(i, '000000000000000000')
        

    def memmory_data(self):  # создаем папять для данных
        for i in range(self.MAX_MEM):
            self.mem_data.insert(i, 0)


    def read_memory(self, address): # Возвращаем значение, хранящееся в памяти по адресу <адрес>
        return self.mem_data[address]


    def write_memory(self, address, value):# Записать <значение> в ячейку памяти <адрес>
        self.mem_data[address] = value


    def read_prog(self, address):# Возвращаем инструкцию из адреса ПЗУ <адрес>
        return self.mem_prog[address]


    def program(self, address, value):# Запрограммируйте местоположение ПЗУ <адрес> со значением <значение>
        #Этот метод используется для загрузки программы в память программы (так не должно быть , но мы всего лишь эмитируем процесс)
        self.mem_prog[address] = value


    def test_opcode(self, expected): #проверяет, был ли ожидаемый код операции установлен декодером
        if self.opcode != expected:
            raise ValueError(f"Недопустимый код операции, ожидается: {expected} Получено: {self.opcode}")
        return
    

    def test_operand(self): #проверяют, находится ли операнд в ожидаемом диапазоне
        if self.operand >= 100:
            raise ValueError(f"Недопустимый операнд, ожидается: 0-99. Получено: {self.operand}")
        return

    def cold_start(self):
        self.memmory_programm()

    def reset(self): # метод сброса 
        self.acc = self.pc = self.instr = 0
        self.zero_flag = self.pos_flag = True
        self.memmory_data()


    def update_acc(self, value): # обновление переменной аккамулятора 
        self.acc = value
        self.update_status()

    def update_pc(self, operand):
        self.pc=operand
        

    def update_status(self): # метод  обновления флага аккумулятора и состояния 
        self.zero_flag = self.acc == 0
        self.pos_flag = self.acc >= 0

    """
    Cоздать методы для обработки циклов выборки, декодирования и выполнения цикла команд.
    """

    def fetch(self):  # метод для обработки циклов выборки
        temp= self.read_prog(self.pc)
        self.instr = int(temp[:4], 2)
        self.tuple_args=tuple([int(temp[4:11], 2) , int(temp[11:], 2) ])
        self.pc += 1  # переходим к следующей команде
     

    def decode(self):
        
        if self.instr==1:
            self.opcode = 1
            self.operand = self.instr
            self.add()
            return
        if self.instr==2:
            self.opcode = 2
            self.operand = self.instr
            x,y=self.tuple_args
            self.write_double_read_d(x,y)
            return
        if self.instr==3:
            self.opcode = 3
            self.operand = self.instr
            x,y= self.tuple_args
            self.write_one_read_d(x,y)
            return
        if self.instr==4:
            self.opcode = 4
            self.operand = self.instr
            self.up_schet()
            return
        if self.instr==5:
            self.opcode = 5
            self.operand = self.instr
            z,c=self.tuple_args
            self.control_number_d(z,c)
            return
        if self.instr==6:
            self.opcode = 6
            self.operand = self.instr
            x,y=self.tuple_args
            self.sravnenie_d(x,y)
            return
        if self.instr==7:
            self.opcode = 7
            self.operand = self.instr
            x,y=self.tuple_args
            self.write_memory_d(x,y)
            return
        if self.instr==8:
            self.opcode = 8
            self.operand = self.instr
            x,y=self.tuple_args
            self.write_number_d(x,self.read_memory(y))
            return
        if self.instr==11:
            self.opcode = 11
            self.operand = self.instr
            c,step=self.tuple_args
            self.addw_d(c,step)
            return
        if self.instr==12:
            self.opcode = 12
            self.operand = self.instr
            z,y=self.tuple_args
            self.comparison_d(z,y)
            return
        if self.instr==0:
            self.halt()
        else:
            raise ValueError("Неизвестаный код операции")
        

    def nop(self): # метод пустоты
        if not self.opcode == 0:
            raise ValueError(f"Недопустимый код операции, ожидается: 0 получено: {self.opcode}")
        return None
        
    def lda(self): # загружает аккумулятор значением
        self.test_opcode(1)
        self.test_operand()
        self.update_acc(self.read_memory(self.operand))
 

    def sta(self):  #Этот метод принимает значение аккумулятора и сохраняет его по адресу, указанному в операнде.
        self.test_opcode(2)
        self.test_operand()
        self.write_memory(self.operand, self.acc)
   

    def and_(self):
        # Логическое И значение в ACC и ячейке памяти <operand>
        # и поместите результаты обратно в ACC, затем установите флаги состояния
        # соответственно
        self.test_opcode(3)
        self.test_operand()
        value = self.read_memory(self.operand)
        self.update_acc(self.acc & value)

    def or_(self):
        pass

    def not_(self):
        pass   

    def write_memory_d(self,x,y):
        self.write_memory(x,y)

    def write_double_read_d(self,x,y): 
        # запись число !первое!   #2
        self.write_memory(x,self.read_memory(self.read_memory(y)))# счетчик массива

    def write_one_read_d(self, x,y): 
        # запись число  #3 
        self.write_memory(x,self.read_memory(y))# счетчик массива 

    def addw_d(self,c, step=1): #11
        self.write_memory(c, self.add_m(self.read_memory(c),step)) # увеличиваем значение счетчика на 1
 
    def comparison_d(self, z,y): #12 # 
        if self.comparison_schet(z,y): #  если счетчик вышел за пределы и ячейка z больше y меняем их местами 
            self.write_memory(y,self.read_memory(z))

    def control_number_d(self, z=-2,c=-3, step=1): # 5   #  RCR - проверка числа лежащее в ячейки 'с' число на которое нужно увеличить первое значение чтобы сравнить второе число в ячейки 'c+n' и вызвать команду 'c+n+n'        
        if  not self.comparison_schet(z,z-c): 
            self.pc=self.read_memory(z-c-c)
       
    def comparison_schet(self,x,y ): # 9
        return True if self.read_memory(x)>=self.read_memory(y) else False # -3 0
        
    def sub(self): 
        # вычитание
        self.test_opcode(7)
        self.test_operand()
        value = self.read_memory(self.operand)
        self.update_acc(self.acc - value)
        
    def add_m(self, x,y): # 16
        return x+y

    def brz(self):
        pass
    
    def brp(self):
        # IFF последняя операция оставила установленным флаг нуля,
        # переход к местоположению программы <операнд>. Обратите внимание на это
        # Инструкция не изменяет ни один из флагов состояния.
        self.test_opcode(9)
        self.test_operand()
        if self.pos_flag:
            self.update_pc(self.operand)


    def trace(self):
        color = fg('red')
        # # Отображение процессора и памяти
        print( color + f"ACC: {self.acc}, PC: {self.pc}, Z: {self.zero_flag}, P: {self.pos_flag}")
        print( color + f"ROM: {self.mem_prog}")
        color = fg('green')
        print(color+'')
        print( f"MEM: {self.mem_data}")
        print( fg('white') +'')

    def step(self):
        self.fetch()
        self.decode()
        if self.debug:
            self.trace()
    
    def run(self):
        self.debug = False
        while not self.halted:
            self.step()
        self.debug = True
        self.step()
    def halt(self):
        self.halted = True



def read_text():
    file_path = 'C:\\Users\\Дмитрий\\Desktop\\МАГИСТР\\MagiCtr\\Разработка программно-аппаратного обеспечения информационных и автоматизированных систем\\PR_create_processor\\test.txt'

    f = open(file_path, 'r+')
    lines = [line.replace("\n", "").strip() for line in f.readlines()]   
    return lines
    

def main():
    #двухадресная команда add x, y (сложить содержимое ячеек x и y, а результат поместить в ячейку y)
    # архитектура гарвардская 

    cpu = CPU()    # 5
    cpu.cold_start() # создание памяти  
    cpu.reset()     # Сброс должен быть вызван перед любым доступом к памяти  
    a=0
    for i in read_text():
        command=i.upper().split(' ')
        for i in command: 
            if i =='': command.remove(i)
        if command[0]==CPU.MEM_DATA:
            cpu.mem_data[int(command[1])] = int(command[2])
        if command[0]==CPU.CONTROL_NUMBER:
            cpu.program(a, f"{cpu.control_number:b}".rjust(4,'0')+f"{int(command[1]):b}".rjust(7,'0') +f"{int(command[2]):b}".rjust(7,'0'))
            a+=1
        if command[0]==CPU.COMPARISON:
            cpu.program(a, f"{cpu.comparison:b}".rjust(4,'0')+f"{int(command[1]):b}".rjust(7,'0') +f"{int(command[2]):b}".rjust(7,'0'))
            a+=1
        if command[0]==CPU.ADDW:
            cpu.program(a, f"{cpu.addw:b}".rjust(4,'0')+f"{int(command[1]):b}".rjust(7,'0') +f"{int(command[2]):b}".rjust(7,'0'))
            a+=1
        if command[0]==CPU.WRITE_ONE_READ:
            cpu.program(a, f"{cpu.write_one_read:b}".rjust(4,'0')+f"{int(command[1]):b}".rjust(7,'0') +f"{int(command[2]):b}".rjust(7,'0'))
            a+=1
        if command[0]==CPU.WRITE_DOUBLE_READ:
            cpu.program(a, f"{cpu.write_double_read:b}".rjust(4,'0')+f"{int(command[1]):b}".rjust(7,'0') +f"{int(command[2]):b}".rjust(7,'0'))
            a+=1
        if command[0]==CPU.WRITE_MEMMORY:
            cpu.program(a, f"{cpu.write_mem:b}".rjust(4,'0')+f"{int(command[1]):b}".rjust(7,'0') +f"{int(command[2]):b}".rjust(7,'0'))
            a+=1

        
        
    
    # cpu.mem_data[0] = 8  # Сохраняем данные для загрузки в аккумулятор  # кол-во данных в массиве
    

    # cpu.mem_data[1] =1000
    # cpu.mem_data[2]=10
    # cpu.mem_data[3]=3
    # cpu.mem_data[4]=444
    # cpu.mem_data[5]=5
    # cpu.mem_data[6]=6
    # cpu.mem_data[7]=7
    # cpu.mem_data[8]=555


    # # на вход индекс первое отвечает за номер операции , 
    # # далее значения которые нужно поместить на вход операции ,
    # # у всех он разный 
    # # 99  - 1100011
    # #98 - 1100010
    # #97 -1100001
    # # 1

    # # 7 -111
    # """
    # 5 - 0101
    # 8 - 1000
    # 9-  1001
    # 10
    # 11 - 1011
    # 12 - 1100
    # 13
    # """
    
    # cpu.program(0,'000100000000000000')#  1x0  0001.1100011.1100011
    # cpu.program(1,'011111000100000001') # 7x98x1 # запись числа для промежуточного значения

    # cpu.program(2,'000100000000000000') # 1x0
    # cpu.program(3,'100011000101100001') # 8x98x97  # запись первого числа 

    # cpu.program(4,'000100000000000000') # 1x0
    # cpu.program(5,'001011000111100001') # 2x99x97 # запись счетчика массива 

    # cpu.program(6,'000100000000000000') # 1x0
    # cpu.program(7,'100100000001100011') # 9x0x99 # где будет счетчик и ответ 

    # # cpu.program(8,'000100000000000000') # 1x0
    # # cpu.program(9,'5x98x97') # 5x98x97 # где будет промежуточный результат и счетчик


    # cpu.program(8,'000100000000000000') # 1x0
    # cpu.program(9,'101111000010000001') # переход на след число цикла

    # cpu.program(10,'000100000000000000') # 1x0
    # cpu.program(11,'110011000101100011') # сравниваем

    # cpu.program(12,'000100000000000000') # 1x0
    # cpu.program(13,'001011000101100001') # записываем след число в ram

    # cpu.program(14,'000100000000000000') # 1x0
    # cpu.program(15,'010100010001100001') # 5x8(число оператора который нужно повторить)x97 # где будет промежуточный результат и счетчик

    # cpu.program(16,'000100000000000000') # 1x0
    # cpu.program(17,'110011000101100011') # # 12x98x99 сравниваем

    cpu.run()

    

if __name__ == '__main__':
    main()

