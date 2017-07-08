import sys
import random
import os

ver = "0.0.3"
vmbuild = "3"
stage = "BETA"

class Stack:
    def __init__(self):
        self.obj = []
    def pop(self):
        try:
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
        self.return_addr_stack = Stack()
        self.instruction_pointer = 0
        self.code = code
        self.svar = {}
        self.dispatch_map = {
            "%":        self.mod,
            "*":        self.mul,
            "+":        self.plus,
            "-":        self.minus,
            "/":        self.div,
            "==":       self.equals,
            "print":    self.print_,
            "println":  self.println,
            "jmp":      self.jmp,
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
        }

    def setcode(self,code):
        self.code = code

    def pop(self):
        return self.data_stack.pop()

    def push(self, value):
        self.data_stack.push(value)

    def top(self):
        return self.data_stack.top()

    def clearstack(self):
        self.data_stack.clear()

    def run(self):
        self.instruction_pointer = 0
        while self.instruction_pointer < len(self.code):
            opcode = self.code[self.instruction_pointer]
            self.instruction_pointer += 1
            self.dispatch(opcode)

    def dispatch(self, op):
        if op in self.dispatch_map:
            self.dispatch_map[op]()
        elif isinstance(op, str) and op[0]=='"' and op[-1]=='"':
            self.push(op[1:-1])
        elif isinstance(op, bool):
            self.push(op)
        elif isinstance(op, int):
            self.push(op)
        elif isinstance(op, float):
            self.push(op)
        else:
            raise RuntimeError("Unknown opcode: '%s'" % op)

    def mod(self):
        last = self.pop()
        self.push(self.pop() % last)

    def plus(self):
        self.push(self.pop() + self.pop())

    def minus(self):
        last = self.pop()
        self.push(self.pop() - last)

    def mul(self):
        self.push(self.pop() * self.pop())

    def div(self):
        last = self.pop()
        l2 = self.pop()
        self.push(l2 / last)

    def print_(self):
        sys.stdout.write(str(self.pop()))
        sys.stdout.flush()

    def println(self):
        sys.stdout.write(str(self.pop()) + "\n")
        sys.stdout.flush()

    def jmp(self):
        addr = self.pop()
        if isinstance(addr, int) and 0 <= addr < len(self.code):
            self.instruction_pointer = addr
        else:
            raise RuntimeError("JMP address must be a valid integer.")

    def if_stmt(self):
        false_clause = self.pop()
        true_clause = self.pop()
        test = self.pop()
        if test == True:
            self.push(true_clause)
        else:
            self.push(false_clause)

    def cast_int(self):
        self.push(int(self.pop()))

    def cast_str(self):
        self.push(str(self.pop()))

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
        vv = self.pop()
        vn = self.pop()
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
        numlines = 350
        if os.name in ("posix","darwin"):
            os.system('clear')
        elif os.name in ("nt", "dos", "ce"):
            os.system('CLS')
        else:
            print('\n' * numlines)
