#!/usr/bin/env python3


"""µCat - a concatenative stack-based language

Usage: MicroCat.py [ SCRIPT... ]

Options:

    -h,        --help       print this help & exit
    --version    print the version & filename then exit

Omission of all above arguments will result in reading from STDIN.

Mandatory arguments to long options are mandatory for short options too.
issues, source, contact: github.com/catb0t/mouse16
"""

import readline
import os
import sys
from docopt import docopt

import CatCompile, CatExec, CatStack

__version__ = "0.1"


def main():
    args = docopt.docopt(__doc__, version=__file__ + " " + __version__)

    fs = args["SCRIPT"]
    if fs:
        for _, e in enumerate(fs):
            runfile(e, args)
    else:
        interpret(args)

def runfile(fname, args):
    try:
        os.stat(fname)
    except (FileNotFoundError, IOError) as err:
        print(err)
        print("stat: cannot stat '{}': no such file or directory"
            .format(fname)
        )
    else:
        fio = open(fname, "rb")
        fcontents = fio.read()
        fio.close()
        if fcontents[0] == 255:
            bc = fcontents
        else:
            bc = CatCompile.Compile(fcontents, args)
        CatExec.Execute(fcontents, args)


def interpret(args):
    print(
        "flags:" + " ".join([
            str(list(args.keys())[i]) + ":" + str(list(args.values())[i])
            for i in range(len(list(args.keys())))
        ]) + "\n", end=""
    )
    print(
        """run \"{} --help\" in your shell for help on {}
        {}
        µCat interpreter""".format(
            __file__, os.path.basename(__file__),
"""
\t███╗   ███╗ ██╗  ██████╗ ██████╗   ██████╗   ██████╗  █████╗  ████████╗
\t████╗ ████║ ██║ ██╔════╝ ██╔══██╗ ██╔═══██╗ ██╔════╝ ██╔══██╗ ╚══██╔══╝
\t██╔████╔██║ ██║ ██║      ██████╔╝ ██║   ██║ ██║      ███████║    ██║
\t██║╚██╔╝██║ ██║ ██║      ██╔══██╗ ██║   ██║ ██║      ██╔══██║    ██║
\t██║ ╚═╝ ██║ ██║ ╚██████╗ ██║  ██║ ╚██████╔╝ ╚██████╗ ██║  ██║    ██║
\t╚═╝     ╚═╝ ╚═╝  ╚═════╝ ╚═╝  ╚═╝  ╚═════╝   ╚═════╝ ╚═╝  ╚═╝    ╚═╝
"""
        )
    )
    shellnum = 0
    while True:
        try:
            line = list(input("\n µCat 🐱  " + hex(shellnum) + " )  "))
        except KeyboardInterrupt:
            print("\naborted: no debugger yet (EOF to exit)")
        except EOFError:
            print("\nbye\n")
            exit(0)
        else:
            shellnum += 1
            bc = CatCompile.Compile(line)
            CatExec.Execute(bc)

if __name__ == "__main__":
    main()
