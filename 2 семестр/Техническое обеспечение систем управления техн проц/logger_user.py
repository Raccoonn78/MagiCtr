import time 
import datetime
 
 
class Logg():

    def __init__(self) -> None:
        pass

    def time_now(self):
        current_time = datetime.datetime.now()#.time()
        return current_time
    def info(self, message=''):

        print(f'[ {self.time_now()} ] INFO: {message}')

    def warning(self, message=''):

        print(f'[ {self.time_now()} ] WARNING: {message}')

    def error(self, message=''):

        print(f'[ {self.time_now()} ] ERROR: {message}')

logs= Logg()
