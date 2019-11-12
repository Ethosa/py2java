import regex
import py2java

string = """# hello asd
asd12
if 1+1:
    a = 123
    b = "lol"
    if 1+1:
        # lol
        pass
if False:
    if 0:
        if 1:
            print("lol")
"""
# # print(regex.findall(r"if([^:]+)", string))
# # print(regex.sub(r"if([^:]+):", r"if (\1){", string))
# string = regex.sub(r"(?P<blockIndent>[ ]*)if[ ]*((?P<condition>[^:\r\n]+?))[ ]*:[\r\n]+(?P<body>(?P<indent>[ ]+)[^\r\n]+[\r\n]+((?P=indent)[^\r\n]+[\r\n]+)*)", r"\g<blockIndent>if (\g<condition>) {\n\g<body>\g<blockIndent>}\n ", string, regex.MULTILINE)
# string = regex.sub(r"(?P<blockIndent>[ ]*)if[ ]*((?P<condition>[^:\r\n]+?))[ ]*:[\r\n]+(?P<body>(?P<indent>[ ]+)[^\r\n]+[\r\n]+((?P=indent)[^\r\n]+[\r\n]+)*)", r"\g<blockIndent>if (\g<condition>) {\n\g<body>\g<blockIndent>}\n ", string, regex.MULTILINE)
# string = regex.sub(r"(?P<blockIndent>[ ]*)if[ ]*((?P<condition>[^:\r\n]+?))[ ]*:[\r\n]+(?P<body>(?P<indent>[ ]+)[^\r\n]+[\r\n]+((?P=indent)[^\r\n]+[\r\n]+)*)", r"\g<blockIndent>if (\g<condition>) {\n\g<body>\g<blockIndent>}\n ", string, regex.MULTILINE)
# print(string)
pj = py2java.PythonToJava()
print(pj.translate(string))