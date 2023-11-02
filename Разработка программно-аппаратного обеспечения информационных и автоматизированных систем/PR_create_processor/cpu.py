

from time import time
import time
import pprint
from termcolor import colored, cprint
from colored import fg
from art import *

def time_sleep():
    # tprint('loading__CPU')
    time.sleep(1)
    print('...')
    time.sleep(1)
    print('...')
    time.sleep(1)
    print('...')
    time.sleep(1)

    


class CPU:
    """
    Гарвардкая архитектура:
        - характероне её отличие в том что памаять разделена на две части, одна для программы другая для данных

        Такой подход стабильнее, но не перезаписываем
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
            self.mem_prog.insert(i, 0)
        

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
        self.instr = self.read_prog(self.pc)
        self.pc += 1  # переходим к следующей команде


    def decode1(self): # метод для декодирования 
        """
        Проверить, находится ли значение инструкции в определенном диапазоне.

        Например, значение инструкции в диапазоне от 0 до 99 будет указывать, что инструкция является NOP или инструкцией без операции. 

        Если значение инструкции находится в диапазоне от 100 до 199, то это должна быть инструкция LDA или «Загрузка аккумулятора».
        """
        if self.instr in range(0, 100):
            self.opcode = 0
            self.operand = self.instr
            self.nop()

        elif self.instr in range(100, 200):
            self.opcode = 1
            self.operand = self.instr - 100
            self.lda()

        elif self.instr in range(200, 300):
            self.opcode = 2
            self.operand = self.instr - 200
            self.sta()

        elif self.instr in range(300, 400):
            self.opcode = 3
            self.operand = self.instr - 300
            self.and_()

        elif self.instr in range(400, 500):
            self.opcode = 4
            self.operand = self.instr - 400
            self.or_()

        elif self.instr in range(500, 600):
            self.opcode = 5
            self.operand = self.instr - 500
            self.not_()

        elif self.instr in range(600, 700):
            self.opcode = 6
            self.operand = self.instr - 600
            self.add()

        elif self.instr in range(700, 800):
            self.opcode = 7
            self.operand = self.instr - 700
            self.sub()

        elif self.instr in range(800, 900):
            self.opcode = 8
            self.operand = self.instr - 800
            self.brz()


        elif self.instr in range(900, 1000):
            self.opcode = 9
            self.operand = self.instr - 900
            self.brp()

        else:
            raise ValueError("Неизвестаный код операции")

        pass


        # методы для выполнение команд
    

    def decode(self):
      
        if self.instr==1:
            self.fetch()
            if self.instr==1:
                self.program(self.pc-1, self.read_prog(self.pc-1) +self.read_prog(self.pc-2) )
                self.opcode = 1
                self.operand = self.instr
                self.add()
                return
            if self.instr==2:
                self.program(self.pc-1, self.read_prog(self.pc-1) +self.read_prog(self.pc-2) )
                self.opcode = 2
                self.operand = self.instr
                self.write_first()
                return
            if self.instr==3:
                self.program(self.pc-1, self.read_prog(self.pc-1) +self.read_prog(self.pc-2) )
                self.opcode = 3
                self.operand = self.instr
                self.write_number()
                return
            if self.instr==4:
                self.program(self.pc-1, self.read_prog(self.pc-1) +self.read_prog(self.pc-2) )
                self.opcode = 4
                self.operand = self.instr
                self.up_schet()
                return
            if self.instr==5:
                self.program(self.pc-1, self.read_prog(self.pc-1) +self.read_prog(self.pc-2) )
                self.opcode = 5
                self.operand = self.instr
                self.control_number()
                return
            if self.instr==6:
                self.program(self.pc-1, self.read_prog(self.pc-1) +self.read_prog(self.pc-2) )
                self.opcode = 6
                self.operand = self.instr
                self.sravnenie()
                return
            if self.instr==7:
                self.program(self.pc-1, self.read_prog(self.pc-1) +self.read_prog(self.pc-2) )
                self.opcode = 7
                self.operand = self.instr
                self.write_schetchick()
                return
            if self.instr==8:
                self.program(self.pc-1, self.read_prog(self.pc-1) +self.read_prog(self.pc-2) )
                self.opcode = 8
                self.operand = self.instr
                self.write_ram()
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

    def add(self): # сумма
        while self.read_memory(0) != 0:
            self.test_opcode(1) # проверка 
            self.test_operand() # проверка 

            value = self.read_memory(1) # читаем список значений из памяти 
            all_sum= value[-(self.read_memory(0))]+self.read_memory(2) # 
            self.write_memory(2,all_sum) 
            self.write_memory(0,self.read_memory(0)-1)
            # получаем из нулевой ячкйки памяти значение (кол-во элементов )
            # получаем список чесиле
            # суммируем значение которое лежит в ячейки пяти три , с число 
            # так как в ячейки два лежит список, и нам нужно понимать какой элемент мы суммируем
            # то мы дуем уменьшать число в нулевой ячейки для того чтобы поремещатться по массиму 
            # и забирать из него значения
            # дальше просто уменьшаем кол-во элементов в первой ячейки данные на 1 
            # и перезаписываем ее обратно, а сумму записываем в ячейку три  
            #

            
         # заканчиваем суммироватьт
        self.halt()
    
    def write_schetchick(self):# присваиваем счетчику 1 так как числа начиаются с первой ячейки # 7
        self.write_memory(-3,1)
    def write_ram(self): # 8  # типо записи в оперативу 
        self.write_memory(-2, self.read_memory( self.read_memory(-3)))
       

    def write_first(self): # запись число !первое!   #2
        value = self.read_memory(-3) # счетчик массива 
        x=self.read_memory(value)
        self.write_memory(-1,x)

    def write_number(self): # запись число  #3 
        value = self.read_memory(-2) # счетчик массива 
        # x=self.read_memory(value)
        self.write_memory(-1,value)

    def up_schet(self): # переход к следующему числу списка  #4 
        value = self.read_memory(-3)
        self.write_memory(-3,value+1)

    def control_number(self): # 5
        x=self.read_memory(-2)
        if self.sravnenie(x):
            self.write_number()
        self.write_ram() # возможно нужно вынксти как такт 
        
    def sravnenie(self, x ): # 6
        y = self.read_memory(-1)
        return 1 if x>y else None
        
    def sub(self): # вычитание
        
        self.test_opcode(7)
        self.test_operand()
        value = self.read_memory(self.operand)
        self.update_acc(self.acc - value)
        
    


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
        color = fg('green')
        # # Отображение процессора и памяти
        # print( fg('red') + f'Opcode: {self.opcode}, Operand: {self.operand}')
        print( color + f"ACC: {self.acc}, PC: {self.pc}, Z: {self.zero_flag}, P: {self.pos_flag}")
        print( color + f"ROM: {self.mem_prog}")
        print( color + f"MEM: {self.mem_data}")
        print( fg('white') +'')

    def step(self):
    
        self.fetch()
        self.decode()
        if self.debug:
            self.trace()
    
    def run(self):
        self.debug = True
        while not self.halted:
            self.step()
        self.debug = True

    def halt(self):
        self.halted = True





def program_iterations(cpu=None, iterations=1):

    while iterations > 0:
        cpu.step()
        print("00    LDA  0")
        cpu.step()
        print("01    SUB  1")
        cpu.step()
        print("02    STA  3")
        print("--- Loop ---")
        iterations -= 1


def main():
    #двухадресная команда add x, y (сложить содержимое ячеек x и y, а результат поместить в ячейку y)
    # архитектура гарвардская 
    # 
    """
    Последовательность команд :
    7,8,2,4,5,4,8 ,5,4,8 ,5,4,8 ,5,4,8 ... столько раз сколько чисел в списке
    """
    cpu = CPU()    # 5

    cpu.cold_start() # создание памяти  
    cpu.reset()     # Сброс должен быть вызван перед любым доступом к памяти  
    cpu.mem_data[0] = 7  # Сохраняем данные для загрузки в аккумулятор  # кол-во данных в массиве
 
    cpu.mem_data[1] =9
    cpu.mem_data[2]=10
    cpu.mem_data[3]=3
    cpu.mem_data[4]=444
    cpu.mem_data[5]=5
    cpu.mem_data[6]=6
    cpu.mem_data[7]=7

    cpu.program(0,1)
    cpu.program(1,7)

    cpu.program(2,1)
    cpu.program(3,8)

    cpu.program(4,1)
    cpu.program(5,2)

    cpu.program(6,1)
    cpu.program(7,4)

    cpu.program(8,1)
    cpu.program(9,5)

    cpu.program(10,1)
    cpu.program(11,4)

    cpu.program(12,1)
    cpu.program(13,5)

    cpu.program(14,1)
    cpu.program(15,4)

    cpu.program(16,1)
    cpu.program(17,5)

    cpu.program(18,1)
    cpu.program(19,4)

    cpu.program(20,1)
    cpu.program(21,5)

    cpu.program(22,1)
    cpu.program(23,4)

    cpu.program(24,1)
    cpu.program(25,5)

    cpu.program(26,1)
    cpu.program(27,4)

    cpu.program(28,1)
    cpu.program(29,5)

    


    
  
    cpu.run()

    
    
    
def main_second():

    cpu=CPU()

    cpu.memmory_programm()

    cpu.reset()     # Сброс должен быть вызван перед любым доступом к памяти  
    cpu.mem_data[2] = 7  # Сохраняем данные для загрузки в аккумулятор 
    cpu.mem_data[3] = 10
    cpu.program(0, 102)
    cpu.program(1, 201)
    cpu.program(2, 303)
    cpu.program(3, 900)


    cpu.fetch()
    cpu.decode()   

    cpu.fetch()
    cpu.decode()   

    cpu.fetch()
    cpu.decode()  

    cpu.fetch()
    cpu.decode()   
    
    color ='1' #fg('white')
        # # Отображение процессора и памяти
    print( color + f'Opcode: {cpu.opcode}, Operand: {cpu.operand}')
    print( color + f"ACC: {cpu.acc}, PC: {cpu.pc}, Z: {cpu.zero_flag}, P: {cpu.pos_flag}")
    print( color + f"ROM: {cpu.mem_prog}")
    print( color + f"MEM: {cpu.mem_data}")


def test_main(cpu=None, iterations=1):

    cpu=CPU()

    cpu.memmory_programm()

    cpu.reset() 

    cpu.mem_data[0] = 9  # Сохраняем данные для загрузки в аккумулятор 
    cpu.mem_data[1] = 6
    cpu.mem_data[2] = 0

    cpu.program(0, 100)     # LDA 0
    cpu.program(1, 701)     # SUB 1
    cpu.program(2, 203)     # STA 3

    cpu.debug = True
    program_iterations(cpu, iterations)


# test_main()
if __name__ == '__main__':
    main()




# while self.read_memory(0) != 0:
   
            

#             value = self.read_memory(1) # читаем список значений из памяти 
#             max_data =self.read_memory(2) # максимальный элемент
     
#             data_max_now=value[-(self.read_memory(0))]   if  value[-(self.read_memory(0))] > self.read_memory(2) else self.read_memory(2)
#             self.write_memory(2,data_max_now) 
#             self.write_memory(0,self.read_memory(0)-1)
