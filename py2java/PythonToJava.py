# -*- coding utf-8 -*-
# authors: Ethosa, Konard

from retranslator import Translator
import regex

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
        # # ...
        # // ...
        (r"#([^\r\n]+)", r"//\1",None, 0),
        # if CONDITION: # smth
        # if (CONDITION){ # smth }
        (r"(?P<blockIndent>[ ]*)if[ ]*((?P<condition>[^:\r\n]+?))[ ]*:[\r\n]+(?P<body>(?P<indent>[ ]+)[^\r\n]+[\r\n]+((?P=indent)[^\r\n]+[\r\n]+)*)", r"\g<blockIndent>if (\g<condition>) {\n\g<body>\g<blockIndent>}\n ", None, 70),

    ]

    LAST_RULES = []
