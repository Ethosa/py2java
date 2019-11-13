import regex
import re
import py2java
from social_ethosa import timeIt

string = '''
if True:
\tif False:
        b = 346
    else:
        pass
elif True:
    if 1:
        while 123:
            pass
    elif True:
        pass
else:
    lol
for i in range(2):
    pass
for i in range(1, 5):
    pass
for i in range(1, 5, 2):
    pass
for i in range(5, 1, -2):
    pass

a = [1, 2, 3, 4, 5]
for i in a:
    print(i)

try:
    pass
except Exception as e:
    print(e)
finally:
    pass

with open("lol", "r", encoding="utf-8") as f:
    pass
with open("lol", "r", encoding="utf-8"):
    pass

a = Open()
b = 1
c = 1.1
d = "hello"
e = 'l'
array = [5, 2, 3, 1]
for i in array:
    print(i)
    print(float(i))

def testDef(a, b, c):
    def helloWorld(function):
        print("lol")
def _privatedLol():
    pass
def __protectedLol():
    pass

class test(object):
    pass

class Lol(object, Exception):
    def __init__(self):
        pass
class ban:
    """docstring for ban"""
    BAN = """BANAN"""
'''
# # (?# string1 = re.findall(r"(?P<blockIndent>[ ]*)elif[ ]*((?P<condition>[^:\r\n]+?))[ ]*:[\r\n]+(?P<body>(?P<indent>[ ]+)[^\r\n]+[\r\n]+((?P=indent)[^\r\n]+[\r\n]+)*)", string))


# string = re.sub(r"(?P<firstAssignment>(?P<variable>[_a-zA-Z]+) = [^\r\n]+)(?P<otherAssigments>([\s\S]+(?P=variable) = [^\r\n]+)*)",
#             r"var \g<firstAssignment>\g<otherAssigments>", string)

p2j = py2java.PythonToJava(useRegex=1)
print(p2j.translate(string))