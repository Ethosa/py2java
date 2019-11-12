# -*- coding utf-8 -*-
# authors: Ethosa, Konard

from retranslator import Translator

class PythonToJava(Translator):
    def __init__(self, codeString="", extra=[]):
        """initialize class
        
        Keyword Arguments:
            codeString {str} -- source code on C# (default: {""})
            extra {list} -- include your own rules (default: {[]})
        """
        self.codeString = codeString
        self.extra = extra
        self.Transform = self.compile = self.translate # callable objects

        # create little magic ...
        self.rules = PythonToJava.FIRST_RULES[:]
        self.rules.extend(self.extra)
        self.rules.extend(PythonToJava.LAST_RULES)
        Translator.__init__(self, codeString, self.rules)

    # Rules for translate code
    FIRST_RULES = [
        # TAB (\t)
        # 4 spaces (    )
        (r"\t", r"    ", None, 0),
        # True
        # true
        (r"True", r"true", None, 0),
        # False
        # false
        (r"False", r"false", None, 0),
        # pass
        # 
        (r"pass", r"", None, 0),
        # print
        # System.out.println
        (r"print", r"System.out.println", None, 0),
        # str(object)
        # object.toString()
        (r"\bstr\((?P<name>[^\)]+)\)", r"\g<name>.toString()", None, 0),
        # int(object)
        # (int)(object)
        (r"\bint\((?P<name>[^\)]+)\)", r"(int)(\g<name>)", None, 0),
        # float(object)
        # (float)(object)
        (r"\bfloat\((?P<name>[^\)]+)\)", r"(float)(\g<name>)", None, 0),
        # len(object)
        # object.length
        (r"\blen\((?P<name>[^\)]+)\)", r"\g<name>.length", None, 0),
        # [1, 2, 3]
        # {1, 2, 3}
        (r"\[(?P<array>[^\]]+)\]", r"{\g<array>}", None, 0),
        # a = "smth" # hello world
        # a = "smth"; # hello world
        (r"([^\r\n#: ])([ ]*)(#[^\r\n]+)?([\r\n]+)", r"\1;\2\3\4", None, 0),
        # # ...
        # // ...
        (r"#([^\r\n]+)", r"//\1",None, 0),
        # while CONDITION: # smth
        # while (CONDITION){ # smth }
        (r"(?P<blockIndent>[ ]*)while[ ]*((?P<condition>[^:\r\n]+?))[ ]*:[\r\n]+(?P<body>(?P<indent>[ ]+)[^\r\n]+[\r\n]+((?P=indent)[^\r\n]+[\r\n]+)*)", r"\g<blockIndent>while (\g<condition>) {\n\g<body>\g<blockIndent>}\n ", None, 70),
        # else: smth
        # else {smth}
        (r"(?P<blockIndent>[ ]*)else[ ]*:[\r\n]+(?P<body>(?P<indent>[ ]+)[^\r\n]+[\r\n]+((?P=indent)[^\r\n]+[\r\n]+)*)", r"\g<blockIndent>else{\n\g<body>\g<blockIndent>}\n", None, 70),
        # elif CONDITION: smth
        # else if (CONDITION) {smth}
        (r"(?P<blockIndent>[ ]*)elif[ ]*((?P<condition>[^:\r\n]+?))[ ]*:[\r\n]+(?P<body>(?P<indent>[ ]+)[^\r\n]+[\r\n]+((?P=indent)[^\r\n]+[\r\n]+)*)", r"\g<blockIndent>else if (\g<condition>){\n\g<body>\g<blockIndent>}\n", None, 70),
        # if CONDITION: # smth
        # if (CONDITION){ # smth }
        (r"(?P<blockIndent>[ ]*)if[ ]*((?P<condition>[^:\r\n]+?))[ ]*:[\r\n]+(?P<body>(?P<indent>[ ]+)[^\r\n]+[\r\n]+((?P=indent)[^\r\n]+[\r\n]+)*)", r"\g<blockIndent>if (\g<condition>) {\n\g<body>\g<blockIndent>}\n ", None, 70),
        # range(2)
        # range(0, 2, 1)
        (r"range\((?P<number1>\d+)\)", r"range(0, \g<number1>, 1)", None, 70),
        # range(1, 2)
        # range(1, 2, 1)
        (r"range\((?P<number1>\d+),[ ]*(?P<number2>\d+)\)", r"range(\g<number1>, \g<number2>, 1)", None, 70),
        # for i in range(2): smth
        # for (int i = 0; i < 2; i += 1){ smth }
        (r"(?P<blockIndent>[ ]*)for[ ]*((?P<variableName>\S+))[ ]*in[ ]*range\((?P<number1>\d*), (?P<number2>\d*), (?P<number3>\d*)\)[ ]*:[\r\n]+(?P<body>(?P<indent>[ ]+)[^\r\n]+[\r\n]+((?P=indent)[^\r\n]+[\r\n]+)*)", r"\g<blockIndent>for (int \g<variableName> = \g<number1>; \g<variableName> < \g<number2>; \g<variableName> += \g<number3>){\n\g<body>\g<blockIndent>}\n", None, 70),
        # for i in range(2): smth
        # for (int i = 0; i < 2; i += 1){ smth }
        (r"(?P<blockIndent>[ ]*)for[ ]*((?P<variableName>\S+))[ ]*in[ ]*range\((?P<number1>\d*), (?P<number2>\d*), -(?P<number3>\d*)\)[ ]*:[\r\n]+(?P<body>(?P<indent>[ ]+)[^\r\n]+[\r\n]+((?P=indent)[^\r\n]+[\r\n]+)*)", r"\g<blockIndent>for (int \g<variableName> = \g<number1>; \g<variableName> > \g<number2>; \g<variableName> -= \g<number3>){\n\g<body>\g<blockIndent>}\n", None, 70),
        # for i in range(2): smth
        # for (int i = 0; i < 2; i += 1){ smth }
        (r"(?P<blockIndent>[ ]*)for[ ]*((?P<variableName>\S+))[ ]*in[ ]*(?P<arrayName>\S+)[ ]*:[\r\n]+(?P<body>(?P<indent>[ ]+)[^\r\n]+[\r\n]+((?P=indent)[^\r\n]+[\r\n]+)*)", r"\g<blockIndent>for (int \g<variableName> = 0; \g<variableName> < \g<arrayName>.length; \g<variableName>++){\n\g<body>\g<blockIndent>}\n", None, 70),
        # try: smth
        # try{ smth }
        (r"(?P<blockIndent>[ ]*)try[ ]*:[\r\n]+(?P<body>(?P<indent>[ ]+)[^\r\n]+[\r\n]+((?P=indent)[^\r\n]+[\r\n]+)*)", r"\g<blockIndent>try{\n\g<body>\g<blockIndent>}\n", None, 70),
        # except Exception as e: smth
        # catch (Exception e) { smth }
        (r"(?P<blockIndent>[ ]*)except[ ]*(?P<exceptionName>\S+)[ ]*as[ ]*(?P<except>\S+):[\r\n]+(?P<body>(?P<indent>[ ]+)[^\r\n]+[\r\n]+((?P=indent)[^\r\n]+[\r\n]+)*)", r"\g<blockIndent>catch (\g<exceptionName> \g<except>){\n\g<body>\g<blockIndent>}\n", None, 70),
        # finally:
        # finally{
        (r"(?P<blockIndent>[ ]*)finally[ ]*:[\r\n]+(?P<body>(?P<indent>[ ]+)[^\r\n]+[\r\n]+((?P=indent)[^\r\n]+[\r\n]+)*)", r"\g<blockIndent>finally{\n\g<body>\g<blockIndent>}\n", None, 70),
        # with open(...) as f:
        # try(open f = new open(...)){
        (r"(?P<blockIndent>[ ]*)with[ ]*(?P<className>[_a-zA-Z0-9]+)(?P<brackets>.+)[ ]*as[ ]*(?P<name>\S+)[ ]*:[\r\n]+(?P<body>(?P<indent>[ ]+)[^\r\n]+[\r\n]+((?P=indent)[^\r\n]+[\r\n]+)*)", r"\g<blockIndent>try (\g<className> \g<name> = new \g<className>\g<brackets>){\n\g<body>\g<blockIndent>}\n", None, 70),
        # with open(...):
        # try(new open(...)){
        (r"(?P<blockIndent>[ ]*)with[ ]*(?P<className>[_a-zA-Z0-9]+)(?P<brackets>.+)[ ]*:[\r\n]+(?P<body>(?P<indent>[ ]+)[^\r\n]+[\r\n]+((?P=indent)[^\r\n]+[\r\n]+)*)", r"\g<blockIndent>try (new \g<className>\g<brackets>){\n\g<body>\g<blockIndent>}\n", None, 70),
        # a = "hello world"
        # a = "hi"
        # var a = "hello world"
        # a = "hi"
        (r"(?P<firstAssignment>(?P<variable>[_a-zA-Z]+)[ ]*=[ ]*[^\r\n]+)(?P<otherAssigments>([\s\S]+(?P=variable) = [^\r\n]+)*)", r"var \g<firstAssignment>\g<otherAssigments>", None, 0),
        # {            }
        # {}
        (r"[ ]*{\s+}", r" {}", None, 0),
        # 
        # 
        (r"", r"", None, 0)
    ]

    LAST_RULES = []
