#!/usr/bin/env python3
"""exposes builtins for a stack machine."""


class DataTape(object):
    """canonical stack-machinisms defined here
    dup, swap, rot, drop, etc"""
    pass


class CodeTape(object):
    """operations that only make sense
    on a stackfull of of executable opcodes"""
    pass


class FullStack(DataTape, CodeTape):

    def __init__(self, *args, **kwargs):
        """inherit from the data and code stacks
        and provide an interface to each"""
        self.__stack__ = []
