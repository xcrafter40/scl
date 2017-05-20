# scl
Syntax like Forth, programmed in Python!

### Sample Code
Hello world:
`"hello world!" println"`
Add 2 numbers:
`"Number 1:" println read int "Number 2:" println read int + println`
Even or odd number:
`"Number: " println read int 2 % 0 == 12 16 if jmp "It's even" println 18 jmp "It's odd" println noop`
### How it works
This entire language uses stacks to organize data. For example:
`3 3 + println` adds together 3 and 3 and prints them

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
mach
