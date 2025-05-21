celery = Celery(
    'background',
    broker=config.message_queue,
    backend=config.message_queue,
    include=['background.tasks']
)
celery.conf.update(
    task_serializer='json',
    result_serializer='json',
    result_backend='redis',
)
celery.conf.beat_schedule = {
    'start_tasks': {
        'task': 'check',
        'schedule': 60
    },
    'regular_messages': {
        'task': 'regular_messages',
        'schedule': 60*30
    },
    'tree': {
        'task': 'regular_search_from_hh_vacancy',
        'schedule': 60*60*20
    } 
}



'''
Запуск  celery 
Запустить redis (redis-server.exe)
запустить сам celery  \server\scripts\start_background.bat

Создание задачи 
создать функцию в папке tasks слеедующего вида

@celery.task(name='название модуля', bind=True, rate_limit='5/s')
@galileo_task(name='название модуля', log=True, single=True)
def название функции(self,  ...     use_celery=False   ):
    galileo.чтото.чтото( ...,  use_celery=False )

rate_limit - частоста вызова 
single в декораторе,  True значит что можно запустить только одну функцию , а все такие же будут вставать в очередь 
в функию передаете все параметры которые будут использоваться, кроме подключение к БД и экземпляр current_user !!!!!
в init.py  делаем импрот всего нашего ФАЙЛА
подключение к БД передаем внутри фукнкции celery (смотри пример в notification)
и точно  так же current_user (смотри пример в cube)


Переходим к редактированию функции которую ставиим в очередь 
Нунжо добавить аргумент use_celery =False  (при вызове например в роутах ставите True) !!!!!!!!ВАЖНО 
внутри функции делаем следующую проверку 
    if use_celery:
        from background import tasks
        qwe =tasks.название функции.delay( ... , use_celery=False)
        return {
            'message': 'Задача   создана',
            'recipients': [],
            'is_send': True,
            'traceback_str': None, 'qwe':qwe
        }
Когда celery вызывет вашу функцию то аргумент use_celery будет False


если задача может прерваться , при перезапуске celery , то ее нужно сбрасывать , иначе она встанет в бесконечную очередь 
нужно тогда добавить задачу в автосброс , заходим в background_run.py и в tasks_names =[.....  добавляем название вашей задачи 

'''