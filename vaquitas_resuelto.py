import os
import random
import time
import threading

inicioPuente = 10
largoPuente = 20
finPuente = inicioPuente + largoPuente

cantVacas = 5

semaforoIndividual = threading.Semaphore(1)
semaforoGrupal = threading.Semaphore(cantVacas)


class Vaca(threading.Thread):
    def __init__(self):
        super().__init__()
        self.posicion = 0
        self.velocidad = random.uniform(0.1, 0.9)

    def avanzar(self):
        semaforoGrupal.acquire()
        try:
            while self.posicion < inicioPuente:
                time.sleep(1 - self.velocidad)
                self.posicion += 1
            try:
                semaforoIndividual.acquire()
                while self.posicion >= inicioPuente:
                    time.sleep(1 - self.velocidad)
                    self.posicion += 1
                    if self.posicion == finPuente:
                        semaforoIndividual.release()
            finally:
                semaforoIndividual.release()
        finally:
            semaforoGrupal.release()

    def dibujar(self):
        print(' ' * self.posicion + '🐮')

    def run(self):
        while True:
            self.avanzar()


vacas = []
for i in range(cantVacas):
    v = Vaca()
    vacas.append(v)
    v.start()


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def dibujarPuente():
    print(' ' * inicioPuente + '=' * largoPuente)


while True:
    cls()
    print('Apretá Ctrl + C varias veces para salir...')
    print()
    dibujarPuente()
    for v in vacas:
        v.dibujar()
    dibujarPuente()
    time.sleep(0.2)
