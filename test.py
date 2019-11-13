import py2java
import regex
import re

sourceText = """
sourceText = "test"
def main():
    print(sourceText)
class lol(object):
    \"\"\"docstring for lol\"\"\"
    _LOL = "test" # test variable
a = "True"
b = True
c = " False asd"
c = " False"
c = "a False asd"
d = False
ch = 'a'
testI = 5
testI = 6
testFloat = 1.0 # comment
asd1 = lol()
asd1 = lol()
asd2 = True
asd2 = False
asd3 = 0
asd3++
asd3 += 1
"""
translator = py2java.PythonToJava(useRegex=1, javaVersion=8)
# print(translator.compile(sourceText))
# print(re.sub(r"(?!\")(?P<indent>(?<!\")[^,\"][ ]*)False(?P<indent1>[^,\"][ ]*)(?!\")",
#     r"\g<indent>false\g<indent1>", sourceText))
print(translator.translate(sourceText))