# scl
Syntax like Forth, programmed in Python!

### Sample Code
Hello world:
`"hello world!" println`

Add 2 numbers:
`"Number 1:" println read int "Number 2:" println read int + println`

Even or odd number:
`"Number: " println read int 2 % 0 == "It's even" "It's odd" if println`

Guess my number (SCL 0.3+):
`1 10 rand "rn" var  "i'm thinking of a number between 1 and 10" println  tag:guess "your guess: " print read int "rn" vget  == "win" "lose" if jtag  tag:lose "try again!" println "guess" jtag  tag:win "you win!" println "end" jtag  tag:end noop`

### How it works
This entire language uses stacks to organize data. For example:
`3 3 + println` pushes 3 and 3 to the stack. + Adds them together and pushes 6.
Finally, println prints the data on the stack. (6)

### Using the API
The entire VM is in an API. How to use:
```python
machine = scl.Machine([])
```
The commands you can do with that object:
```python
# set the code
machine.setcode([5, "println"]) #prints 5

#run the machine
machine.run()

#stack functions
machine.pop()
machine.push("hello world!")
machine.top()

#manual operation
#doesn't parse the stack, everything is manual
machine.push("hello world!")
machine.println()
```
### Command Index
* (%)
* (*)
* (+)
* (-)
* (/)
* ==
* print
* println
* jmp
* int
* str
* over
* read
* noop
* dup
* exit
* var
* vget
* if
* cs
* rand
* cls
* jtag
* npop
* flt
* wait
* sp
* ret
* rtag
* throw

### Credits
Thanks a ton to CSLarsen for the backbone of SCL

https://csl.name/post/vm/
