from __future__ import annotations

from collections import OrderedDict
import inspect
from inspect import Parameter, Signature
from typing import Any, Callable, Union

import numpy
import pandas
import scipy
import scipy.optimize

from .functions import IFunction

def fit_function(function: IFunction, X: Union[list, numpy.ndarray[float], pandas.Series], Y: Union[list, numpy.ndarray[float], pandas.Series], initial_values: numpy.ndarray[float] = None, fixed_parameters: dict[str, Any] = None, *arguments, **keyword_arguments):
    if type(X) == pandas.Series:
        X = X.to_list()
    
    if type(Y) == pandas.Series:
        Y = Y.to_list()
    
    optimum: numpy.ndarray
    covariance: numpy.ndarray

    f = function.f
    signature: Signature = inspect.signature(f)
    parameters: OrderedDict[str, Parameter] = signature.parameters

    if fixed_parameters:
        def reduced_f(x, *reduced_arguments) -> float:
            reduced_parameters: numpy.ndarray = numpy.ndarray(len(parameters) - 1)

            reduced_argument_index: int = 0
            for i, (key, value) in enumerate(parameters.items()):
                if i == 0:
                    continue

                if fixed_parameters and key in fixed_parameters:
                    reduced_parameters[i - 1] = fixed_parameters[key]
                else:
                    reduced_parameters[i - 1] = reduced_arguments[reduced_argument_index]
                    reduced_argument_index += 1

            return function.f(x, *reduced_parameters)

        f = reduced_f

    if not initial_values and "bounds" in keyword_arguments:
        bounds = keyword_arguments["bounds"]
        initial_values = minimize(f, X, Y, bounds)

    optimum, covariance = scipy.optimize.curve_fit(f, X, Y, initial_values, nan_policy = "omit", *arguments, **keyword_arguments)
    parameter_array: numpy.ndarray = numpy.ndarray(len(parameters) - 1)

    optimum_index: int = 0
    for i, (key, value) in enumerate(parameters.items()):
        if i == 0:
            continue
        
        if fixed_parameters and key in fixed_parameters:
            parameter_array[i - 1] = fixed_parameters[key]
        else:
            parameter_array[i - 1] = optimum[optimum_index]
            optimum_index += 1

    return function.from_parameter_array(parameter_array)

def minimize(function: Callable, X, Y, bounds):
    """Minimize the sum of squares of a function with the given parameter bounds."""
    def objective_function(parameters):
        sum: float = 0
        for i in range(0, len(X)):
            x = X[i]
            y = Y[i]

            sum += pow(function(x, *parameters) - y, 2.0)
        return sum
    
    return scipy.optimize.differential_evolution(objective_function, bounds).x