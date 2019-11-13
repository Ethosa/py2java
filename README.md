<h1 align="center">Python to Java language Translator</h1>
Install: ```pip install py2java```
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
