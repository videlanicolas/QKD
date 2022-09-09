from math import pow, sqrt
from random import randint

from numpy import matrix


class QuBit:
    def __init__(self, initial_state):
        if initial_state:
            self.__state = matrix(
                [
                    [0],
                    [1],
                ]
            )
        else:
            self.__state = matrix(
                [
                    [1],
                    [0],
                ]
            )
        self.__measured = False
        self.__H = (1 / sqrt(2)) * matrix(
            [
                [1, 1],
                [1, -1],
            ]
        )
        self.__X = matrix(
            [
                [0, 1],
                [1, 0],
            ]
        )

    def __repr__(self):
        aux = ""
        val10 = round((matrix([1, 0]) * self.__state).item(), 2)
        if val10 and val10 != 1.0:
            aux += f"{val10}|0>"
        val01 = round((matrix([0, 1]) * self.__state).item(), 2)
        if val01 and val01 != 1.0:
            if aux:
                aux += " + "
            aux += f"{val01}|1>"
        return aux

    def measure(self):
        if self.__measured:
            raise Exception("Qubit already measured!")
        M = 1000000
        m = randint(0, M)
        self.__measured = True
        if m < round(pow(matrix([1, 0]) * self.__state, 2), 2) * M:
            return 0
        else:
            return 1

    def hadamard(self):
        if self.__measured:
            raise Exception("Qubit already measured!")
        self.__state = self.__H * self.__state

    def X(self):
        if self.__measured:
            raise Exception("Qubit already measured!")
        self.__state = self.__X * self.__state


