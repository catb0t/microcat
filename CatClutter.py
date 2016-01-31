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
        "vars": (show_vars, (optlist)),
        "quit": (exit,      (0)),
        "exit": (exit,      (0)),
    }
    if cmdlet[0] in builtins:
        func, args = builtins.get(cmdlet[0])
        func(args)

    elif cmdlet[0] in optlist and len(cmdlet) == 2:
        nval = cmdlet[1]

        if cmdlet[0] == "shnum_type":
            if nval in ("int", "hex", "oct", "bin"):
                optlist[cmdlet[0]] = nval
            else:
                print(
                    "junk base for shellnum counter: '{}' not (int, hex, oct, bin)"
                    .format(nval)
                )
        else:
            if nval.lower() in ("true", "false"):
                nval = True if nval.lower() == "true" else False
            optlist[cmdlet[0]] = nval
    else:
        print("""
    sorry, don't know how to '{}'.
    if you think this is in error, please file an issue on github."""
            .format(" ".join(cmdlet))
        )
    return optlist


def show_help(*args):
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


def show_docs(*args):
    pass


def show_vars(optlist):
    print(
        "\n\tREPL envrionment variables in effect:\n\n"
        + "\t\n".join(
            "\tNAME: " + str(list(optlist.keys())[i])
            + "\n\tVALUE:\t" + str(list(optlist.values())[i]) + "\n"
            for i in range(len(list(optlist.keys())))
        )
    )


def show_cmds(*args):
    print("-> undefined")


def EOF(code = 0):
    """exit the repl"""
    print("\n{}, {}; i {} :(\n".format(hex(50159747054), "0x0" + hex(14544909)[2:], hex(4276215469)))
    exit(code)

METAMENU = r"""
             ____        _
     _   _  / __/ ___ _ | |_
    | | | |/ /   /  _` || __|
    | |_| |\ \__ µ (_| || |_
    |  _,_| \___\\___,_| \__|
    |_/

    this is the metamenu.
    you can say:
     _
    /-> <CTRL-C> or <ENTER> to return to the REPL
    |-> <EOF> to quit µCat
    |-> a command like:
    \___
        \-> help  : to see µCat's README
        |-> docs  : to see all the docstrings
        |-> vars  : to see REPL variables in effect
        |-> cmds  : to see a list of metamenu commands
        |-> exit  : to quit µCat
     ___/-> var x : set var to x
    /
    \_<- """

MICROCAT_LOGO = r"""
\t███╗   ███╗ ██╗  ██████╗ ██████╗   ██████╗   ██████╗  █████╗  ████████╗
\t████╗ ████║ ██║ ██╔════╝ ██╔══██╗ ██╔═══██╗ ██╔════╝ ██╔══██╗ ╚══██╔══╝
\t██╔████╔██║ ██║ ██║      ██████╔╝ ██║   ██║ ██║      ███████║    ██║
\t██║╚██╔╝██║ ██║ ██║      ██╔══██╗ ██║   ██║ ██║      ██╔══██║    ██║
\t██║ ╚═╝ ██║ ██║ ╚██████╗ ██║  ██║ ╚██████╔╝ ╚██████╗ ██║  ██║    ██║
\t╚═╝     ╚═╝ ╚═╝  ╚═════╝ ╚═╝  ╚═╝  ╚═════╝   ╚═════╝ ╚═╝  ╚═╝    ╚═╝
"""

isnum    = lambda n: isinstance(n, (int, float))
isarr    = lambda a: isinstance(n, (list, tuple, dict))
isint    = lambda n: isinstance(n, int)
isflt    = lambda n: isinstance(n, float)
isstr    = lambda s: isinstance(n, str)
strsum   = lambda s: sum(map(ord, s))
bool2int = lambda v: int(v)
signflip = lambda n: n * -1
iseven   = lambda n: int(n) % 2 == 0
toeven   = lambda n: int(n - 1) if not iseven(n) else int(n)
isnone   = lambda x: isinstance(x, type(None))
nop      = lambda*a: None

# I don't /want/ to pass a tuple to any/all

allof = lambda *args: all([i for i in args])
anyof = lambda *args: any([i for i in args])

isascii = (lambda struni:
            (len(__import__("unicodedata")
                .normalize('NFD', struni)
                .encode('ascii', 'replace'))
                    == len(struni)))
