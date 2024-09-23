from __future__ import annotations

from typing import Protocol, Self

import numpy

class IFunction(Protocol):
    def to_discrete(self, start: float, stop: float, number: int) -> tuple[numpy.ndarray[float], numpy.ndarray[float]]:
        X: numpy.ndarray[float] = numpy.linspace(start, stop, number)
        Y: numpy.ndarray[float] = numpy.array([self(x) for x in X])
        return X, Y

    @staticmethod
    def f(x: float) -> float:
        pass
    
    @staticmethod
    def from_parameter_array(array: numpy.ndarray) -> Self:
        pass

class Polynomial(IFunction):
    """y = a0 + a1 * x + a2 * x^2 + a3 * x^3 + ..."""
    coefficients: list[float]

    def __init__(self, coefficients: list[float]):
        self.coefficients = coefficients

    def __str__(self):
        strings: list[str] = []

        for i in range(0, len(self.coefficients)):
            coefficient: float = self.coefficients[i]
            if (coefficient == 0):
                continue

            if i == 0:
                strings.append(f"{coefficient:e}")
            else:
                if i == 1:
                    strings.append(f"{coefficient:e}x")
                else:
                    strings.append(f"{coefficient:e}x^{i}")
        
        if (len(strings)) == 0:
            return "0"

        return " + ".join(strings)

    def __call__(self, x) -> float:
        return self.f(x, *self.coefficients)
    
    @property
    def order(self) -> int:
        return len(self.coefficients)

    @staticmethod
    def f(x: float, *coefficients):
        sum: float = 0

        for i in range(0, len(coefficients)):
            sum += coefficients[i] * pow(x, i)

        return sum
    
    @staticmethod
    def from_parameter_array(array: numpy.ndarray) -> Self:
        return Polynomial(array)

class Power(IFunction):
    """y = Ax^r"""
    A: float
    r: float
    
    def __init__(self, A: float, r: float):
        self.A = A
        self.r = r

    def __str__(self):
        return f"{self.A}x^{self.r}"

    def __call__(self, x) -> float:
        return self.f(x, self.A, self.r)

    @staticmethod
    def f(x: float, A: float, r: float) -> float:
        return A * pow(x, r)
    
    @staticmethod
    def from_parameter_array(array: numpy.ndarray) -> Self:
        return Power(*array)

class PowerWithOffset(IFunction):
    """y = Ax^r + C"""
    A: float
    r: float
    C: float
    
    def __init__(self, A: float, r: float, C: float):
        self.A = A
        self.r = r
        self.C = C

    def __str__(self):
        return f"{self.A}x^{self.r} + {self.C}"

    def __call__(self, x) -> float:
        return self.f(x, self.A, self.r, self.C)

    @staticmethod
    def f(x: float, A: float, r: float, C: float) -> float:
        return A * pow(x, r) + C
    
    @staticmethod
    def from_parameter_array(array: numpy.ndarray) -> Self:
        return PowerWithOffset(*array)