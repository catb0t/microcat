#!/usr/bin/env python3
"""execs bytes as opcodes."""

import sys
import CatLogger, CatStack, CatClutter

class Executer(object):

    def __init__(self, code, *args, **kwargs):
        """takes in numbers and does stuff."""
        self.stk = Stack()

    def Run(self):