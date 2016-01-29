#!/usr/bin/env python3

"""
tiny module for crufty-feeling tiny contextless functions and constants
that just clutter the other modules more than they need to
"""

def SetREPLopts(cmdlet, optlist):
    """set envrionment variables, etc in the repl"""
    cmdlet = cmdlet.strip().split(" ")
    builtins = {
        "help": (show_help, ()),
        "docs": (show_docs, ()),
        "cmds": (show_cmds, ()),
        "vars": (show_vars, ()),
        "quit": (exit,      (0)),
        "exit": (exit,      (0)),
    }
    if cmdlet[0] in builtins:
        func, args = builtins.get(cmdlet[0])
        func(*args)
    elif cmdlet[0] in optlist and len(cmdlet) == 2:
        optlist[cmdlet[0]] = cmdlet[1]
    else:
        print("""
    sorry, don't know how to '{}'.
    if you think this is in error, please file an issue on github."""
            .format(" ".join(cmdlet))
        )
    return optlist

def show_help():
    try:
        f = open("README.md", "r")
    except (FileNotFoundError, IOError) as err:
        print(err)
        print("sorry, the 'help' utility needs 'README.md' to reside in the current directory")
    else:
        from pydoc import pager
        fc = f.read()
        f.close()
        pager(fc)

def show_docs():
    pass

def show_vars():
    pass

def show_cmds():
    pass

def EOF():
    """exit the repl"""
    print("\n{}, {}; i {} :(\n".format(hex(50159747054), "0x0" + hex(14544909)[2:], hex(4276215469)))
    exit(0)

METAMENU = """

    this is the metamenu.
    you can say:

    |: <CTRL-C> or <ENTER> to return to the REPL
    |: <EOF> to quit µCat
    |: a command like:
    |___
        |: "docs" to see all the docstrings
        |: "help" to see general help on µCat
        |: "vars" to see REPL variables in effect
        |: "cmds" to see a list of metamenu commands
    ____|: "exit" to quit µCat
    |
    |: """

MICROCAT_LOGO = """
\t███╗   ███╗ ██╗  ██████╗ ██████╗   ██████╗   ██████╗  █████╗  ████████╗
\t████╗ ████║ ██║ ██╔════╝ ██╔══██╗ ██╔═══██╗ ██╔════╝ ██╔══██╗ ╚══██╔══╝
\t██╔████╔██║ ██║ ██║      ██████╔╝ ██║   ██║ ██║      ███████║    ██║
\t██║╚██╔╝██║ ██║ ██║      ██╔══██╗ ██║   ██║ ██║      ██╔══██║    ██║
\t██║ ╚═╝ ██║ ██║ ╚██████╗ ██║  ██║ ╚██████╔╝ ╚██████╗ ██║  ██║    ██║
\t╚═╝     ╚═╝ ╚═╝  ╚═════╝ ╚═╝  ╚═╝  ╚═════╝   ╚═════╝ ╚═╝  ╚═╝    ╚═╝
"""
