#!/usr/bin/env python3
"""exposes builtins for a stack machine."""

import types
import sys
import CatLogger, CatClutter

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

    # adding things together

    def add_num(self):
        """( y x -- y+x )
        add two numbers"""
        y, x = self.popn()
        self.push(x + y)

    def add_str(self):
        """( y x -- y+x )
        concatenate two strings"""
        y, x = self.popn()
        self.push(x + y)

    def add_list(self):
        """( y x -- y+x )
        concatenate two lists"""
        y, x = self.popn()
        for _, e in enumerate(y):
            x.append(y)
        self.push(x)

    # who knows what else will go here in the future

    # subtracting things

    def sub_num(self):
        """( z y x -- y-x )
        subtract y from x"""
        y, x = self.popn()
        self.push(x - y)

    def sub_str(self):
        """( y x -- y-x )
        remove a string x from a string y,
        by removing the first occurrence of y from x"""
        y, x = self.popn()
        y.remove(x)
        self.push(y)

    def sub_multi_strs(self):
        """( z y x -- y-x*z )
        remove a string x from a string y, z times
        if not z, all occurrences of x will be removed from y"""
        y, x = self.popn()
        for _ in range(z):
            y.remove(x)
        self.push(y)

    def sub_list(self):
        """( y x -- ??? )
        this function is not yet implemented."""
        CatLogger.Crit("list subtraction not yet implemented")

    # multiplying things

    def mlt_num(self):
        """( y x -- y*x )
        multiply y by x"""
        y, x = self.popn()
        self.push(y * x)

    def mlt_str(self):
        """( y x -- y*x )
        interleave two strings"""
        y, x = self.popn()
        self.push("".join(i for j in zip(x, y) for i in j))

    def mlt_numstr(self):
        """( y x -- y*x )
        copy a string y onto itself, x times"""
        y, x = self.popn()
        self.push(y * x)

    def mlt_lists(self):
        """( y x -- ??? )
        this function is not yet implemented."""
        CatLogger.Crit("list multiplication not yet implemented")

    # splitting things

    def divmod_num(self):
        """( y x -- y/x y%x )
        push a pair of numbers' quotient and then remainder (mod)"""
        y, x = self.popn()
        self.pushn([y / x, y % x])

    def divmod_str(self):
        """( y x -- ??? )
        this function is not yet implemented."""
        CatLogger.Crit("string division not yet implemented")

    def divmod_list(self):
        """( y x -- ??? )
        this function is not yet implemented."""
        CatLogger.Crit("string division not yet implemented")

    def floor_num(self):
        """( y x -- y//x )
        push the floored quotient of two numbers"""
        y, x = self.popn()
        self.push(y // x)

    # negating things

    def neg_num(self):
        """( x -- -x )
        unary minus: flip the sign of a number"""
        x = self.pop()
        self.push(signflip(x))

    def neg_str(self):
        """( "Hello" -- "olleH" )
        invert a string by reversing it"""
        x = self.pop()
        self.push(x[::-1])

    def neg_list(self):
        """( {1 2 3} -- {3 2 1} )
        invert a list by reversing it"""
        x = self.pop()
        self.push(x[::-1])

    # comparison operators

    def equ_num(self):
        """( y x -- y=x? )
        push 1 if two numbers are of equal value, else 0"""
        y, x = self.popn()
        self.push(CatClutter.bool2int(y == x))

    def equ_str(self):
        """( y x -- y=x? )
        push 1 if two strings are of equal value, else 0"""
        y, x = self.popn()
        self.push(CatClutter.bool2int(y == x))

    def equ_numstr(self):
        """( y x -- y=x? )
        push 1 if a number is equal to the sum of the characters in a string"""
        y, x = self.popn()
        if allof(isstr(y), isnum(x)):
            self.push(CatClutter.bool2int(x == CatClutter.strsum(y)))

        elif allof(isnum(y), isstr(x)):
            self.push(CatClutter.bool2int(y == CatClutter.strsum(x)))

        else:
            CatLogger.Crit("unexpected types for equ_numstr")

    def equ_list(self):
        """( y x -- y=x? )
        push 1 if two lists hold the same content in the same order, else push 0"""
        y, x = self.popn()
        self.push(CatClutter.bool2int(x == y))

    # greater?

    def gtr_num(self):
        """( y x -- y>x? )
        push 1 if y is greater than x, else push 0"""
        y, x = self.popn()
        self.push(CatClutter.bool2int(y > x))

    def gtr_str(self):
        """( y x -- y>x? )
        push 1 if the sum of the characters in y is greater than that of x"""
        y, x = self.popn()
        self.push(CatClutter.bool2int(CatClutter.strsum(y) > CatClutter.strsum(x)))

    def gtr_list(self):
        """( y x -- y>x? )
        push 1 if the length of list y is greater than the length of list x"""
        y, x = self.popn()
        self.push(CatClutter.bool2int(len(y) > len(x)))

    # less ?

    def lss_num(self):
        """( y x -- y>x? )
        push 1 if y is less than x, else push 0"""
        y, x = self.popn()
        self.push(CatClutter.bool2int(y > x))

    def lss_str(self):
        """( y x -- y>x? )
        push 1 if the sum of the characters in y is less than that of x"""
        y, x = self.popn()
        self.push(CatClutter.bool2int(CatClutter.strsum(y) < CatClutter.strsum(x)))

    def lss_list(self):
        """( y x -- y>x? )
        push 1 if the length of list y is less than the length of list x"""
        y, x = self.popn()
        self.push(CatClutter.bool2int(len(y) < len(x)))


class BitwiseOps(object):
    """bitwise operations"""

    def and(self):
        """( y x -- x&y )
        bitwise AND the bits of y with x"""
        y, x = self.popn()
        self.push(x & y)

    def or(self):
        """( y x -- y|x )
        bitwise inclusive OR the bits of y with x"""
        y, x = self.popn()
        self.push(x | y)

    def xor(self):
        """( y x -- y^x )
        bitwise XOR (exclusive) the bits of y with x"""
        y, x = self.popn()
        self.push(y ^ x)

    def not(self):
        """( x -- ~x )
        bitwise NOT the bits of x"""
        x = self.popn()
        self.push(~x)


class IOOps(object):
    """input/output."""

    def put(self):
        """( x -- )
        pops the top of the stack and prints/executes"""
        x = self.copy()
        if isnone(x):
            return
        else:
            self.drop()
            length = sys.stdout.write(str(x))
            del length
        del x

    def emit(self):
        """( x -- )
        pops the top of the stack and prints that unicode char"""
        x = self.pop()
        try:
            x = int(x)
        except TypeError:
            if isnone(x):
                return
            else:
                CatLogger.Crit(str(x) + " is not a valid UTF-8 codepoint")
        else:
            length = sys.stdout.write(chr(x))
            del length
        del x

    def get(self):
        """ ( -- x )
        push a string from stdin
        consistent of the beginning of stdin to EOL"""
        x = input()
        self.push(x)

    def get_exact(self):
        """( x -- y )
        get exactly x bytes of stdin, and push them as a string"""
        for _ in range(10):
            i = read_single_keypress()
            _ = sys.stdout.write(i)
            sys.stdout.flush()
            x += i

    def get_until(self):
        """( x -- y )
        get stdin until the character with codepoint x is read, pushing to y"""

    def reveal(self):
        """prints the entire stack, pleasantly"""
        stack = self.inspect()
        peek = repr(stack)
        sys.stdout.write("<{}> {}".format(len(stack), peek[1:len(peek) - 1]))


class CombinatorOps(object):
    """functional programming idioms:
    map, apply, curry, cons, cat, i, car/cdr, dip, etc"""


class CodeOps(object):
    """operations that only make sense
    on a stack full of of executable opcodes"""
    pass


class FullStack(
        IOOps,
        CodeOps,
        CoreOps,
        StackOps,
        LogicOps,
        BitwiseOps,
        CombinatorOps,):

    def __init__(self, *args, **kwargs):
        """inherit from the various interface classes
        and provide an interface to each's methods"""
        self.__stack__ = []
