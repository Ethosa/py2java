# -*- coding utf-8 -*-
# authors: Ethosa, Konard

from retranslator import Translator

class PythonToJava(Translator):
    def __init__(self, codeString="", extra=[], useRegex=False):
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
        Translator.__init__(self, codeString, self.rules, useRegex)

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
        # self
        # this
        (r"self", r"this", None, 0),
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
        # input()
        # System.in.read()
        (r"input\((?P<params>[\S ]*)\)", r"System.in.read(\g<params>)", None, 0),
        # from java.utils import *
        # import java.utils.*
        (r"(?P<blockIndent>[ ]*)from[ ]*(?P<libname>[_a-zA-Z0-9.]+)[ ]*import[ ]*(?P<what>[\S]+)", r"\g<blockIndent>import \g<libname>.\g<what>", None, 0),
        # [1, 2, 3]
        # {1, 2, 3}
        (r"\[(?P<array>[^\]]+)\]", r"{\g<array>}", None, 0),
        # """ ... multiline comment """
        # /* ... multiline comment */
        (r"\n(?P<blockIndent>[ ]*)\"\"\"(?P<comment>([\s\S](?<!\"\"\"))+)\"\"\"", r"\n\g<blockIndent>/*\g<comment>*/",None, 0),
        # a = "smth" # hello world
        # a = "smth"; # hello world
        (r"([^\r\n#: /])([ ]*)(#[^\r\n]+)?([\r\n]+)", r"\1;\2\3\4", None, 0),
        # # ...
        # // ...
        (r"#([^\r\n]+)", r"//\1",None, 0),
        # class Test(object): smth
        # class Test extends object { smth }
        (r"(?P<blockIndent>[ ]*)class[ ]*(?P<className>[_a-zA-Z0-9]+)[ ]*\((?P<extends>[^:][\S ]+)\)[ ]*:[\r\n]+(?P<body>(?P<indent>[ ]+)[^\r\n]+[\r\n]+((?P=indent)[^\r\n]+[\r\n]+)*)", r"\g<blockIndent>class \g<className> extends \g<extends>{\n\g<body>\g<blockIndent>}\n\n",None, 10),
        # class Test: smth
        # class Test { smth }
        (r"(?P<blockIndent>[ ]*)class[ ]*(?P<className>[_a-zA-Z0-9]+)[ ]*:[\r\n]+(?P<body>(?P<indent>[ ]+)[^\r\n]+[\r\n]+((?P=indent)[^\r\n]+[\r\n]+)*)", r"\g<blockIndent>class \g<className> {\n\g<body>\g<blockIndent>}\n",None, 10),
        # def asd(a)
        # def asd(Object a)
        (r"(?P<blockIndent>[ ]*)def[ ]*(?P<functionName>[a-zA-Z0-9_]+)\((?P<ignore>(Object [a-zA-Z0-9]+(, )?)*)(?P<firstParam>(?!Object)[a-zA-Z0-9]+)(?P<other>[\s\S]+)*\)[ ]*:", r"\g<blockIndent>def \g<functionName>(\g<ignore>Object \g<firstParam>\g<other>):", None, 0),
        # def __asd():
        # protected void asd(){ smth }
        (r"(?P<blockIndent>[ ]*)def[ ]*__(?P<functionName>[a-zA-Z0-9_])(?!__)(?P<funcParams>[\S ]+)[ ]*:[\r\n]+(?P<body>(?P<indent>[ ]+)[^\r\n]+[\r\n]+((?P=indent)[^\r\n]+[\r\n]+)*)", r"\g<blockIndent>protected void \g<functionName>\g<funcParams>{\n\g<body>\g<blockIndent>}\n",None, 70),
        # def _asd():
        # private void asd(){ smth }
        (r"(?P<blockIndent>[ ]*)def[ ]*_(?P<functionName>[a-zA-Z0-9_])(?!_)(?P<funcParams>[\S ]+)[ ]*:[\r\n]+(?P<body>(?P<indent>[ ]+)[^\r\n]+[\r\n]+((?P=indent)[^\r\n]+[\r\n]+)*)", r"\g<blockIndent>private void \g<functionName>\g<funcParams>{\n\g<body>\g<blockIndent>}\n",None, 70),
        # def asd():
        # public void asd(){ smth }
        (r"(?P<blockIndent>[ ]*)def[ ]*(?P<functionName>[a-zA-Z0-9_])(?P<funcParams>[\S ]+)[ ]*:[\r\n]+(?P<body>(?P<indent>[ ]+)[^\r\n]+[\r\n]+((?P=indent)[^\r\n]+[\r\n]+)*)", r"\g<blockIndent>public void \g<functionName>\g<funcParams>{\n\g<body>\g<blockIndent>}\n",None, 70),
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
        # a = "hello world"
        # a = "hi"
        # var a = "hello world"
        # a = "hi"
        (r"(?P<firstAssignment>(?P<variable>[_a-zA-Z]+)[ ]*=[ ]*[^\r\n]+)(?P<otherAssigments>([\s\S]+(?P=variable) = [^\r\n]+)*)", r"var \g<firstAssignment>\g<otherAssigments>", None, 0),
        # for i in range(2): smth
        # for (int i = 0; i < 2; i += 1){ smth }
        (r"(?P<blockIndent>[ ]*)for[ ]*((?P<variableName>\S+))[ ]*in[ ]*range\((?P<number1>\d*), (?P<number2>\d*), (?P<number3>\d*)\)[ ]*:[\r\n]+(?P<body>(?P<indent>[ ]+)[^\r\n]+[\r\n]+((?P=indent)[^\r\n]+[\r\n]+)*)", r"\g<blockIndent>for (int \g<variableName> = \g<number1>; \g<variableName> < \g<number2>; \g<variableName> += \g<number3>){\n\g<body>\g<blockIndent>}\n", None, 70),
        # for i in range(5, 1, -2): smth
        # for (int i = 5; i > 1; i -= 2){ smth }
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
        # {            }
        # {}
        (r"[ ]*{\s+}", r" {}", None, 0),
        # 
        # 
        (r"", r"", None, 0)
    ]

    LAST_RULES = []
