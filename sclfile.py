import scl
import interactive
import sys
import os

args = sys.argv

def iwrite(txt):
    sys.stdout.write(txt + "\n")
    sys.stdout.flush()

if len(args) < 2:
    iwrite("Correct usage:")
    iwrite(args[0] + " <file>")
    exit()

openfile = args[1]

if not os.path.exists(openfile):
    iwrite("No such file: " + openfile + "!")
    exit()

filelines = []

with open(openfile,"r") as fh:
    filelines = fh.readlines()

def convertscl(l):
    return interactive.parse(" ".join(l).replace("\n",""))

machine = scl.Machine(convertscl(filelines))
machine.run()
