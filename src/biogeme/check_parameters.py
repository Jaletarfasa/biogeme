"""Functions to verify the validity of parameters

:author: Michel Bierlaire
:date: Thu Dec  1 16:22:34 2022

"""
import numbers
import biogeme.optimization as opt


def zero_one(x):
    """Return true if x is between zero and one

    :param x: value of the parameter to check
    :type x: float
    """
    if 0 <= x <= 1:
        return (True, None)
    return False, 'Value must be between zero and one'


def is_number(x):
    """Return true if x is a number

    :param x: value of the parameter to check
    :type x: float
    """
    if isinstance(x, numbers.Number):
        return (True, None)
    return False, 'Value must be a number'


def is_positive(x):
    """Return true if x is positive

    :param x: value of the parameter to check
    :type x: float
    """
    if x > 0:
        return (True, None)
    return False, 'Value must be positive'


def is_non_negative(x):
    """Return true if x is non_negative

    :param x: value of the parameter to check
    :type x: float
    """
    if x >= 0:
        return (True, None)
    return False, 'Value must be non negative'


def is_integer(x):
    """Return true if x is integer

    :param x: value of the parameter to check
    :type x: float
    """
    if isinstance(x, numbers.Integral):
        return (True, None)
    return False, 'Value must be an integer'


def check_algo_name(x):
    """Return true if x is a valid algorithm name

    :param x: value of the parameter to check
    :type x: float
    """
    possibilities = list(opt.algorithms.keys())
    if x in possibilities:
        return True, None
    return False, f'Value must be in: {possibilities}'


def is_boolean(x):
    """Return true if x is a boolean

    :param x: value of the parameter to check
    :type x: float
    """
    if isinstance(x, bool):
        return True, None
    return False, 'Value must be boolean'
