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

import CatExec, CatClutter

runner = CatExec.Execute()

__version__ = "0.1"


def main():
    "main entry point."
    args = docopt.docopt(__doc__, version=__file__ + " " + __version__)

    fs = args["SCRIPT"]

    if fs:
        for _, e in enumerate(fs):
            runfile(e, args)
    else:
        interpret(args)


def runfile(fname, args):
    "open a file for reading"
    runner = CatExec.Executer()
    try:
        fio = open(fname, "rt")
    except (FileNotFoundError, IOError) as err:
        print(err)
        print("stat: cannot stat '{}': no such file or directory"
            .format(fname)
        )
    else:
        with fcontents as fio.read(): f = fcontents
        if args["-o"]: out = open(args["-o"], "wt")
        runner.Run(f, flags=args)


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
    # repl options
    shopt = {
        "shnum_type": "int",
        "implicit_print": True,
    }
    # repl counter (I don't know why, it's just cool)
    shellnum = 0
    runner   = CatExec.Executer()

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
            runner.Run(line, flags=args, interp_opts=shopt)

if __name__ == "__main__":
    main()
