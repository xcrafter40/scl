import scl

def customsplit(text):
    buildtmp = []
    returntmp = []
    isquote = False
    for i in text:
        if i == '"':
            if isquote:
                isquote = False
                buildtmp.append('"')
                returntmp.append("".join(buildtmp))
                buildtmp = []
            else:
                buildtmp.append('"')
                isquote = True
        elif i == " ":
            if not isquote:
                returntmp.append("".join(buildtmp))
                buildtmp = []
            else:
                buildtmp.append(" ")
        else:
            buildtmp.append(i)
    if len(buildtmp) > 0:
        returntmp.append("".join(buildtmp))
        buildtmp = []
    while '' in returntmp:
        returntmp.remove('')
    return returntmp

def parse(text):
    txt = customsplit(text)
    ctr = 0
    for i in txt:
        if i.isdigit():
            txt[ctr] = int(txt[ctr])
        elif i in ["True","False"]:
            txt[ctr] = txt[ctr] == "True"
        else:
            try:
                txt[ctr] = float(txt[ctr])
            except ValueError:
                txt[ctr] = str(txt[ctr])
        ctr = ctr + 1
    return txt

main = scl.Machine([])
print("SCL", scl.ver, "(" + scl.stage + ", " "VM Build", scl.vmbuild + ")")
print('Hit CTRL+C or type "exit" to quit.')

while True:
    try:
        source = input("> ")
        code = parse(source)
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
