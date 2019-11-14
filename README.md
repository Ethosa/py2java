<h1 align="center">Python to Java language Translator</h1>

This library uses the Translator class from [retranslator library](https://github.com/linksplatform/RegularExpressions.Transformer/tree/master/python).

Installing: ```pip install py2java```

import:
```python
from py2java import PythonToJava
```
Usage:
```python
sourceText = """
sourceText = "test"
def main():
    print(sourceText)
class lol(object):
    \"\"\"docstring for lol\"\"\"
    _LOL = "test" # test variable
"""
translator = PythonToJava(useRegex=1)
print(translator.compile(sourceText))
```

using java controller:
```python
jc = PythonToJava(useRegex=1, javaVersion=8) # standart javaVersion is 10
```
