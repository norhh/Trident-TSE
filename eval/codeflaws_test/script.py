import argparse
import os
import subprocess
from sys import argv
from random import sample
import random
import re
import difflib
import json
from subprocess import STDOUT, check_output

parser = argparse.ArgumentParser(description='Run experiments')

parser.add_argument('--semfix', action='store_true', help='Runs Semfix')
parser.add_argument('--priority', action='store_true', help='Synthesizes using priority')
parser.add_argument('--klee-merge', action='store_true', help='Runs klee-path merge')
parser.add_argument('file', metavar='BUGGY_FILE', nargs=1,
                    help='C file to run the command')

args = parser.parse_args()


def get_buggy_file(path):
    file = path[:-len(path.split("-")[-1]) - 1].split("/")[-1]
    list = file.split('-')[:2] + file.split("-")[3:]
    return "-".join(list) + ".c"


def get_mode():
    if args.semfix:
        return "semfix"
    elif args.klee_merge:
        return "klee-merge"
    return "trident"


def get_non_b_file(path):
    file = path.split("/")[-1]
    list = file.split("-")[:2] + [file.split("-")[-1]]
    return "-".join(list) + ".c"


def add_compile_commands(dir, bfile):
    abs_path = os.path.abspath(bfile)
    s = """
        [
                {{
                    "directory": "/home/Trident/",
                    "command": "gcc {0} -I /llvm-3.8.1/lib/clang/3.8.1/include/",
                    "file": "{1}"
                }},
        ]""".format(abs_path, abs_path)
    with open(os.path.join(dir, 'compile_commands.json'), 'w+') as f:
        f.write(s)


def execute(bfile, priority):
    subprocess.run('cp {} {}_copy'.format(bfile, bfile), shell=True)
    if get_mode() != 'trident':
        command = "patch {} {}/semfix.transform".format(bfile, "/".join(bfile.split("/")[:-1]))
    else:
        command = "patch {} {}/trident.transform".format(bfile, "/".join(bfile.split("/")[:-1]))

    subprocess.run(command, shell=True, stdout=subprocess.DEVNULL)
    with open(bfile, encoding='utf-8') as f:
        if "__trident_choice" not in f.read():
            subprocess.run("cp {}_copy {}".format(bfile, bfile), shell=True)
            return
    data = None
    mode = get_mode()
    try:
        if priority:
            subprocess.run("./run.sh  {} {} --priority".format(bfile, mode), shell=True)
        else:
            subprocess.run("./run.sh  {} {}  --no-priority".format(bfile, mode), shell=True)

    except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
        subprocess.run("killall -9 klee", shell=True)
    subprocess.run("cp {}_copy {}".format(bfile, bfile), shell=True)
    return False


def handle_codeflaws(args):
    dir_path = args.file[0]
    bfile = os.path.join(dir_path, get_buggy_file(dir_path))
    add_compile_commands(dir_path, bfile)
    execute(bfile, args.priority)


if args.file:
    handle_codeflaws(args)