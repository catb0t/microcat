#!/usr/bin/env python3
"""exposes builtins for a stack machine."""


class CoreOps(object):
    """the most basic methods for using the stack.
    cares about typing and exceptions the way your BIOS does: not at all."""

    def inspect(self):
        """getter for the stack"""
        return self.__stack__[:]

    def pop(self, idex = (-1)):
        """( x -- )
        drop and return an item from the TOS"""
        return self.__stack__.pop(idex)

    def popn(self, n = 2, idx = (-1)):
        """( z y x -- )
        drops and returns n items from the stack"""
        x = []
        for _ in range(n):
            y = self.pop(idex=idx)
            if not isnone(y):
                x.append(y)
            else:
                break
        if len(x) == n:
            return tuple(x)
        return (None, None)

    def push(self, x):
        """( -- x )
        push an item to the stack"""
        self.__stack__.append(x)

    def pushn(self, x):
        """( -- y x )
        push n items to the stack"""
        for _, obj in enumerate(x):
            self.push(obj)

    def copy(self):
        """( y x -- y x x )
        return an item from the the stack without dropping"""
        return self.__stack__[-1]

    def copyn(self, n = 2):
        """( z y x -- z y x z y x )
        return n last items from the stack without dropping"""
        result = self.__stack__[signflip(n):]
        return result

    def insert(self, item, idex):
        """( z y x -- z b y x )
        add an item to the stack at the given index"""
        self.__stack__.insert(idex, item)

    def insertn(self, items, lidex):
        """( z y x -- z b y x )
        add a list of items to the stack at the given index"""
        iter(items)
        for _, obj in enumerate(items):
            self.insert(lidex, obj)
            lidex += 1

    def remove(self, n):
        """( x -- )
        remove the nth stack item"""
        del self.__stack__[n]

    def index(self, n):
        """( -- )
        return the nth-last stack item"""
        return self.__stack__[signflip(n)]

    def clean(self):
        """empty the stack, and return the old stack"""
        stk = self.inspect()[:]
        self.__stack__.clear()
        return stk

class StackOps(object):
    """type-agnostic anonical stack-machinisms
    dup, swap, rot, drop, etc"""
    def dup(self):
        """( y x -- y x x )
        push a copy of the TOS"""
        self.push(self.copy())

    def dupn(self, n = 2):
        """( z y x -- z y x y x )
        copy n items from the TOS; push them preserving order"""
        x = self.copyn(n)
        for i in x:
            self.push(i)

    def swap(self):
        """( y x -- x y )
        swap the top two items on the stack"""
        self.pushn(self.popn())

    def rot(self):
        """( z y x w -- z w y x )
        rotates only top three items up"""
        x = self.copyn(3)
        x.insert(0, x.pop())
        for _ in x:
            self.pop()
        for i in x:
            self.push(i)

    def urot(self):
        """( z y x w -- z x w y )
        rotates only top three items down"""
        self.insert(self.pop(), -2)

    def roll(self):
        """( z y x -- y x z )
        roll the stack up"""
        self.push(self.pop(0))

    def rolln(self, n = 2):
        """( z y x -- x z y )
        roll the stack up by n"""
        for _ in range(n):
            self.roll()

    def uroll(self):
        """( z y x -- x z y )
        roll the stack down"""
        self.insert(self.pop(), 0)

    def urolln(self, n = 2):
        """( z y x -- y x z )
        roll the stack down by n"""
        for _ in range(n):
            self.uroll()

    def drop(self):
        """( y x -- y )
        silently drops from the stack"""
        self.pop()

    def dropn(self, n = 2):
        """( y x -- )
        silently drops n items from the stack"""
        self.popn(n)

    def over(self):
        """( z y x -- z y x y )
        copies second-to-top item to TOS"""
        self.push(self.index(2))

    def nip(self):
        """( y x -- x )
        silently drops second-to-top item"""
        self.pop(-2)

    def tuck(self):
        """( y x -- x y x )
        copies TOS behind second-to-top"""
        self.insert(self.copy(), -2)


class LogicOps(object):
    """math & logic operators: pretty straightforward."""

class IOOps(object):
    """input/output."""

class CodeOps(object):
    """operations that only make sense
    on a stack full of of executable opcodes"""
    pass


class FullStack(CoreOps, StackOps, LogicOps, IOOps, CodeOps):

    def __init__(self, *args, **kwargs):
        """inherit from the various interface classes
        and provide an interface to each's methods"""
        self.__stack__ = []
