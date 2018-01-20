import sys
import random
import os
import time

ver = "0.4.0"
vmbuild = "3"
stage = "STABLE"

class Stack:
    def __init__(self):
        self.obj = []
        self.protect = False

    def nopop(self):
        if self.protect:
            self.protect = False
        else:
            self.protect = True

    def pop(self):
        try:
            if self.protect:
                return self.obj[-1]
            else:
                return self.obj.pop()
        except IndexError:
            pass

    def push(self,item):
        self.obj.append(item)

    def top(self):
        return self.obj[-1]

    def clear(self):
        self.obj = []

class Machine:
    def __init__(self, code):
        self.data_stack = Stack()
        self.trace_stack = Stack()
        self.return_addr_stack = Stack()
        self.instruction_pointer = 0
        self.xdbgmode = True
        self.code = code
        self.svar = {}
        self.tags = {}
        self.debugmode = False
        self.errorid = {
            0: "no error",
            1: "internal error",
            2: "argument type error",
            3: "arithmetic error",
            4: "jump error",
            5: "conversion error",
            6: "opcode error",
            7: "thrown error",
        }
        self.breakinstruction = False
        self.currentop = "how_did_you_get_here?!"
        self.dispatch_map = {
            "%":        self.mod,
            "*":        self.mul,
            "+":        self.plus,
            "-":        self.minus,
            "/":        self.div,
            "==":       self.equals,
            "print":    self.print_,
            "println":  self.println,
            #"jmp":      self.jmp,
            "int":      self.cast_int,
            "str":      self.cast_str,
            "over":     self.over,
            "read":     self.read,
            "noop":     self.noop,
            "dup":      self.dup,
            "exit":     self.exit,
            "var":      self.var,
            "vget":     self.vget,
            "if":       self.if_stmt,
            "cs":       self.clearstack,
            "rand":     self.rand,
            "cls":      self.cls,
            "jtag":     self.jtag,
            "pop":      self.pop,
            "dbg":      self.dbg,
            "npop":     self.npop,
            "flt":      self.cast_flt,
            "wait":     self.wait,
            "sp":       self.sp,
            "ret":      self.stk_ret,
            "rtag":     self.rtag,
            "xdbg":     self.xdbg,
            "throw":    self.throw,
        }

    def xdbg(self):
        pass

    def iwriteln(self,txt):
        sys.stdout.write(str(txt) + "\n")
        sys.stdout.flush()

    def iwrite(self,txt):
        sys.stdout.write(str(txt))
        sys.stdout.flush()

    def setcode(self,code):
        self.code = code

    def pop(self):
        return self.data_stack.pop()

    def push(self, value):
        self.data_stack.push(value)

    def top(self):
        return self.data_stack.top()

    def retstack_pop(self):
        return self.return_addr_stack.pop()

    def retstack_push(self, value):
        self.return_addr_stack.push(value)

    def retstack_top(self):
        return self.return_addr_stack.top()

    def canret(self):
        if len(self.return_addr_stack.obj) > 0:
            return True
        return False

    def clearstack(self):
        self.data_stack.clear()

    def precompile(self):
        self.instruction_pointer = 0
        while self.instruction_pointer < len(self.code):
            opcode = self.code[self.instruction_pointer]
            if isinstance(opcode, str) and opcode[0:4] == "tag:":
                clean = opcode.split(":")
                self.tags[clean[1]] = self.instruction_pointer + 1
            self.instruction_pointer += 1

    def run(self):
        self.tags = {}
        self.precompile()
        self.instruction_pointer = 0
        while self.instruction_pointer < len(self.code):
            if self.breakinstruction:
                break
            opcode = self.code[self.instruction_pointer]
            self.instruction_pointer += 1
            self.dispatch(opcode)
        self.breakinstruction = False
        self.currentop = "noop"

    def dispatch(self, op):
        self.currentop = op
        if op in self.dispatch_map:
            self.dispatch_map[op]()
        elif isinstance(op, str) and op[0]=='"' and op[-1]=='"':
            self.push(op[1:-1])
        elif isinstance(op, bool):
            self.push(op)
        elif isinstance(op, int):
            self.push(op)
        elif isinstance(op, str) and op[0:4] == "tag:":
            pass
        elif isinstance(op, float):
            self.push(op)
        else:
            self.sclError(6,"invalid opcode")

        if self.debugmode:
            #self.iwriteln("")
            #self.iwriteln("Pointer: " + str(self.instruction_pointer - 1))
            #self.iwriteln("Opcode: " + str(op))
            #self.iwriteln("Stack: " + str(self.data_stack.obj))
            #self.iwriteln("Return Stack: " + str(self.return_addr_stack.obj))
            #self.iwriteln("Variable: " + str(self.svar))
            #self.iwriteln("")
            self.iwrite("DBG: P: " + str(self.instruction_pointer - 1))
            self.iwrite(" O: " + str(op))
            self.iwrite(" S: " + str(self.data_stack.obj))
            self.iwrite(" R: " + str(self.return_addr_stack.obj))
            self.iwrite(" V: " + str(self.svar))
            self.iwriteln(" ST: " + str(self.trace_stack.obj))

    def sclError(self,eno,err):
        if self.xdbgmode:
            self.iwriteln("-----")
            self.iwriteln("SCL Error")
            self.iwriteln("Stack Trace")
            if len(self.trace_stack.obj) > 0:
                for i in self.trace_stack.obj:
                    self.iwriteln("in subroutine <" + i + ">")
            else:
                self.iwriteln("in subroutine <main>")
            self.iwriteln("At location " + str(self.instruction_pointer - 1))
            self.iwriteln("Opcode: " + str(self.code[self.instruction_pointer - 1]))
            self.iwriteln("Error id [" + str(eno) + "] " + self.errorid[eno])
            self.iwriteln("Error thrown: " + err)
            self.iwriteln("-----")
            self.iwriteln("Stack Dump")
            self.iwriteln(str(self.data_stack.obj))
            self.iwriteln("Variable Dump")
            for k,v in self.svar.items():
                self.iwriteln(k + " : " + v)
            self.iwriteln("Return Stack Dump")
            self.iwriteln(str(self.return_addr_stack.obj))
            self.breakinstruction = True
        else:
            self.iwriteln("SCL Error:" + " [" + str(eno) + "] " + err)
            self.iwriteln("Error type for id " + str(eno) + ":")
            self.iwriteln(self.errorid[eno])
            self.iwriteln("=-=-=-=")
            self.iwriteln("At location " + str(self.instruction_pointer - 1))
            self.iwriteln("At Instruction: " + str(self.code[self.instruction_pointer - 1]))
            self.iwriteln("=-=-=-=")
            self.iwriteln("Stack Dump:")
            self.iwriteln(str(self.data_stack.obj))
            self.iwriteln("Variable Dump:")
            self.iwriteln(str(self.svar))
            self.breakinstruction = True

    def mod(self):
        last = self.pop()
        l2 = self.pop()
        if (isinstance(l2, int) or isinstance(l2, float)) and (isinstance(last, int) or isinstance(last, float)):
            self.push(l2 % last)
        else:
            self.sclError(2,2,"type mismatch (expected int/float)")

    def plus(self):
        last = self.pop()
        l2 = self.pop()
        if (isinstance(l2, int) or isinstance(l2, float)) and (isinstance(last, int) or isinstance(last, float)):
            self.push(l2 + last)
        else:
            self.sclError(2,"type mismatch (expected int/float)")

    def minus(self):
        last = self.pop()
        l2 = self.pop()
        if (isinstance(l2, int) or isinstance(l2, float)) and (isinstance(last, int) or isinstance(last, float)):
            self.push(l2 - last)
        else:
            self.sclError(2,"type mismatch (expected int/float)")

    def mul(self):
        last = self.pop()
        l2 = self.pop()
        if (isinstance(l2, int) or isinstance(l2, float)) and (isinstance(last, int) or isinstance(last, float)):
            self.push(l2 * last)
        else:
            self.sclError(2,"type mismatch (expected int/float)")

    def div(self):
        last = self.pop()
        l2 = self.pop()
        if (isinstance(l2, int) or isinstance(l2, float)) and (isinstance(last, int) or isinstance(last, float)):
            self.push(l2 / last)
        else:
            self.sclError(2,"type mismatch (expected int/float)")

    def print_(self):
        sys.stdout.write(str(self.pop()))
        sys.stdout.flush()

    def println(self):
        sys.stdout.write(str(self.pop()) + "\n")
        sys.stdout.flush()

    def jmp(self):
        addr = self.pop()
        if not isinstance(addr, int):
            self.sclError(2,"type mismatch (expected int)")
            return
        if not 0 <= addr < len(self.code):
            self.sclError(4,"jump out of bounds")
            return
        self.sclError("jmp address must be a valid integer")

    def if_stmt(self):
        false_clause = self.pop()
        true_clause = self.pop()
        test = self.pop()
        if test == True:
            self.push(true_clause)
        else:
            self.push(false_clause)

    def cast_int(self):
        try:
            self.push(int(self.pop()))
        except ValueError:
            self.sclError(5,"type mismatch (expected str as int)")

    def cast_str(self):
        self.push(str(self.pop()))

    def cast_flt(self):
        try:
            self.push(float(self.pop()))
        except ValueError:
            self.sclError(5,"type mismatch (expected str as float)")

    def over(self):
        b = self.pop()
        a = self.pop()
        self.push(a)
        self.push(b)
        self.push(a)

    def read(self):
        self.push(input())

    def noop(self):
        pass

    def dup(self):
        self.push(self.top())

    def exit(self):
        exit()

    def var(self):
        vn = self.pop()
        vv = self.pop()
        self.svar[vn] = vv

    def vget(self):
        vn = str(self.pop())
        self.push(self.svar[vn])

    def equals(self):
        v2 = self.pop()
        v1 = self.pop()
        self.push(True if v1 == v2 else False)

    def rand(self):
        b = self.pop()
        a = self.pop()
        self.push(random.randint(a,b))

    def cls(self):
        if os.name in ("posix","darwin"):
            os.system("clear")
        elif os.name in ("nt", "dos", "ce"):
            os.system("CLS")
        else:
            print("\n" * 350)

    def jtag(self):
        tag = self.pop()
        if isinstance(tag, str) and tag in self.tags:
            self.instruction_pointer = self.tags[tag]
        else:
            self.sclError(4,"jtag address must be a valid tag")

    def rtag(self):
        tag = self.pop()
        if isinstance(tag, str) and tag in self.tags:
            self.trace_stack.push(tag)
            self.retstack_push(self.instruction_pointer)
            self.instruction_pointer = self.tags[tag]
        else:
            self.sclError(4,"rtag address must be a valid tag")

    def stk_ret(self):
        if not self.canret():
            self.sclError(4,"no position to return to")
        else:
            self.trace_stack.pop()
            self.instruction_pointer = self.retstack_pop()

    def dbg(self):
        if self.debugmode:
            self.debugmode = False
        else:
            self.debugmode = True

    def npop(self):
        self.data_stack.nopop()

    def wait(self):
        try:
            wtime = (float(self.pop()))
        except ValueError:
            self.sclError(2,"type mismatch (expected int/float)")
        time.sleep(wtime)

    def sp(self):
        self.iwriteln(self.data_stack.obj)

    def throw(self):
        errtext = self.pop()
        errno = self.pop()
        self.sclError(errno,errtext)
