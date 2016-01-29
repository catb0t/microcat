#!/usr/bin/env python3

from logging import basicConfig, DEBUG, debug, info, warn, error, critical

basicConfig(level=DEBUG)

def Dbg(msg):
    debug(msg=msg)

def Inf(msg):
    info(msg=msg)

def Warn(msg):
    warning(msg=msg)

def Err(msg):
    error(msg=msg)

def Crit(msg):
    critical(msg=msg)