# view:
#    vstack:
#           text:
#           button:
#           button:
# model:
#   count : Int = 0
# ==========================================
# inspired by https://quickbirdstudios.com/blog/swiftui-vs-android-jetpack-compose/

name = "AppBody"
ktlvl = 0
swlvl = 0
num_elements = 0

kt = open(name + ".kt", mode='w')
sw = open(name + ".swift", mode='w')
ktm = open(name + "Model.kt", mode='w')
swm = open(name + "Model.swift", mode='w')


def fwd(k, s):
    global ktlvl
    global swlvl
    if k:
        ktlvl = ktlvl + 1
    if s:
        swlvl = swlvl + 1


def rev(k, s):
    global ktlvl
    global swlvl
    if k:
        ktlvl = ktlvl - 1
    if s:
        swlvl = swlvl - 1


def closeFiles():
    swm.close()
    ktm.close()
    sw.close()
    kt.close()


def tab(k, s):
    if k:
        kt.write("\t"*ktlvl)
    if s:
        sw.write("\t"*swlvl)


def startHead():
    tab(True, True)
    kt.write("@Composable\nfun "+name+"() {\n")
    sw.write("struct "+name+" : View {\n")
    fwd(True, True)


def endHead():
    tab(True, True)
    kt.write("}\n")
    sw.write("}\n")
    rev(True, True)


def VStack():
    tab(True, False)
    kt.write("Center {\n")
    fwd(True, False)

    tab(True, False)
    kt.write("Column {\n")
    fwd(True, False)

    tab(False, True)
    sw.write("VStack {\n")
    fwd(False, True)


def VStackEnd():
    endHead()


def fnBody(f, fnname, indents=1):
    t = "\t" * indents
    f.write("\n" + t + fnname+"() {\n")
    f.write(t + "}\n")


def genModel():
    global num_elements
    swm.write("struct "+name+"Model {\n")
    num = num_elements
    while num_elements:
        swm.write("//Tap"+str(num_elements) + " ,")
        num_elements = num_elements - 1
    fnBody(swm, "onAction", 1)
    while num:
        swm.write("//SetText"+str(num) + " ,")
        num = num - 1
    fnBody(swm, "getTextOf", 1)
    swm.write("}\n")


def plh(elm):  # placeholder of element
    if elm.startswith("Text"):
        return ['textKT', 'textSw']
    if elm.startswith("Button"):
        return ['textKT', 'textSw']


def Element(elm):
    global num_elements
    tab(True, True)
    kt.write(elm+"("+plh(elm)[0]+")\n")
    sw.write(elm+"("+plh(elm)[1]+")\n")
    num_elements = num_elements + 1


def actOn(token):
    if token.startswith('view'):
        startHead()
    if token.startswith('vstack'):
        VStack()
    if token.startswith('text'):
        Element("Text")
    if token.startswith('button'):
        Element("Button")


def parseLine(line):
    if line.endswith(':'):
        actOn(line)


def parseFile(blipName):
   # Gen Swift and KT files

    with open(name+".blip") as bl:
        line = bl.readline()
        cnt = 1
        while line:
            parseLine(line.strip())
            line = bl.readline()
            cnt += 1
        rev(True, True)
    while ktlvl:
        tab(True, False)
        rev(True, False)
        kt.write("} //~"+str(ktlvl)+"+\n")

    while swlvl:
        tab(False, True)
        rev(False, True)
        sw.write("} //~"+str(swlvl)+"+\n")

    endHead()
  # GenModel of View
    genModel()
    closeFiles()


parseFile(name)
