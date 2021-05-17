import random
import threading
import time
import logging

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S',
                    level=logging.INFO)

platosDisponibles = 3
semaforoCocinero = threading.Semaphore(1)
semaforoComensal = threading.Semaphore(3)


class Cocinero(threading.Thread):
    def __init__(self):
        super().__init__()
        self.name = 'Cocinero'

    def run(self):
        global platosDisponibles
        while True:
            semaforoCocinero.acquire()
            try:
                while platosDisponibles > 0:
                    pass
                logging.info('Reponiendo los platos...')
                platosDisponibles = 3
            finally:
                semaforoCocinero.release()


class Comensal(threading.Thread):
    def __init__(self, numero):
        super().__init__()
        self.name = f'Comensal {numero}'

    def run(self):
        global platosDisponibles
        semaforoComensal.acquire()
        try:
            if platosDisponibles > 0:
                platosDisponibles -= 1
                logging.info(f'¡Qué rico! Quedan {platosDisponibles} platos')
            else:
                semaforoCocinero.acquire()
        finally:
            semaforoComensal.release()


Cocinero().start()

for i in range(5):
    Comensal(i).start()
