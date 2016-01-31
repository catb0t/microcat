#!/usr/bin/env python3

#          ____         _
#  _   _  / __/  ___ _ | |_
# | | | |/ /    /  _` || __|
# | |_| |\ \__  µ (_| || |_
# |  _,_| \___\ \___,_| \__|
# |_/
#


"""µCat - a concatenative stack-based JIT-compiled language

Usage: MicroCat.py [ -o FILENAME ] [ SCRIPT... ]

Options:

    -o         --output     write compiled bytecode to this file instead of running
    -h,        --help       print this help & exit
    --version               print the version & filename then exit

Omission of all above arguments will result in reading from STDIN.

Mandatory arguments to long options are mandatory for short options too.
issues, source, contact: github.com/catb0t/mouse16
"""

import readline
import os
from docopt import docopt

import CatCompile, CatExec, CatClutter

__version__ = "0.1"


def main():
    """main entry point."""
    args = docopt.docopt(__doc__, version=__file__ + " " + __version__)

    fs = args["SCRIPT"]

    if fs:
        for _, e in enumerate(fs):
            runfile(e, args)
    else:
        interpret(args)


def runfile(fname, args):
    """open a file for reading
    first in binary; if the first byte of the file is 0xFF or the filename ends in "microcat_bin",
    the file is executed directly as bytecode.
    else, the contents of the file are read as text and compiled, then run"""
    try:
        fio = open(fname, "rb")
    except (FileNotFoundError, IOError) as err:
        print(err)
        print("stat: cannot stat '{}': no such file or directory"
            .format(fname)
        )
    else:
        fcontents = fio.read()
        fio.close()
        if fcontents[0] == 255 or fname.endswith("microcat_bin"):
            bc = fcontents
        else:
            fio = open(fname, "rt")
            fcontents = fio.read()
            fio.close()
            bc = CatCompile.Compile(fcontents, flags=args)
        if args["-o"]:
            fio = open(args["-o"], "")
        CatExec.Execute(bc, flags=args)


def interpret(args):
    """an interpreter suite"""
    print(
        "flags:" + " ".join([
            str(list(args.keys())[i]) + ":" + str(list(args.values())[i])
            for i in range(len(list(args.keys())))
        ]) + "\n", end=""
    )
    print(
        """press <CTRL-C> or run \"{} --help\" in your shell for help on {}
        {}
        µCat interpreter""".format(
            __file__, os.path.basename(__file__), CatClutter.MICROCAT_LOGO
        )
    )
    shopt = {
        "shnum_type": "int",
        "implicit_print": True,
    }
    shellnum = 0

    while True:
        try:
            line = input("\n µCat 🐱  "
                + str(eval(shopt["shnum_type"] + "(shellnum)")) + " )  "
            )
        except KeyboardInterrupt:
            try:
                cmdlet = input(CatClutter.METAMENU)
            except KeyboardInterrupt:
                pass
            except EOFError:
                CatClutter.EOF()
            else:
                if cmdlet:
                    shopt = CatClutter.SetREPLopts(cmdlet, shopt)
            # end metamenu
        except EOFError:
            CatClutter.EOF()
        else:
            shellnum += 1
            bc = CatCompile.Compile(line, flags=args)
            CatExec.Execute(bc, flags=args, interp_opts=shopt)

if __name__ == "__main__":
    main()
