

from logger_user import logs

def my_decorator(fn):
    def wrapped():
        try:
            return fn()
        except Exception as e:
            logs.error("Error:", e)

    return wrapped