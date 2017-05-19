import scl
import tokenize
from io import StringIO

def parse(text):
    tokens = tokenize.generate_tokens(StringIO(text).readline)
    for toknum, tokval, _, _, _ in tokens:
        if toknum == tokenize.NUMBER:
            yield int(tokval)
        elif toknum in [tokenize.OP, tokenize.STRING, tokenize.NAME]:
            yield tokval
        elif toknum == tokenize.ENDMARKER:
            break
        else:
            raise RuntimeError("Unknown token %s: '%s'" %
                (tokenize.tok_name[toknum], tokval))

main = scl.Machine([])
print("SCL", scl.ver, "(" + scl.stage + ", " "VM Build", scl.vmbuild + ")")
print('Hit CTRL+C or type "exit" to quit.')

while True:
    try:
        source = input("> ")
        code = list(parse(source))
        main.setcode(code)
        main.run()
    except (RuntimeError, IndexError) as e:
        print("Error: %s" % e)
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt")
        exit()
    except EOFError as e:
        print()
    except Exception as e:
        print("Internal error: %s" % e)
repl()
