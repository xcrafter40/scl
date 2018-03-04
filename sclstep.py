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

### STEP! ###
machine.tags = {}
machine.precompile()
machine.instruction_pointer = 0
while machine.instruction_pointer < len(machine.code):
    if machine.breakinstruction:
        break
    input("<enter to step> ")
    opcode = machine.code[machine.instruction_pointer]
    machine.instruction_pointer += 1
    machine.dispatch(opcode)

if True:
    machine.iwrite("DBG: P: " + str(machine.instruction_pointer - 1))
    machine.iwrite(" O: " + str(op))
    machine.iwrite(" S: " + str(machine.data_stack.obj))
    machine.iwrite(" R: " + str(machine.return_addr_stack.obj))
    machine.iwrite(" V: " + str(machine.svar))
    machine.iwriteln(" ST: " + str(machine.trace_stack.obj))

machine.breakinstruction = False
