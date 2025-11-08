# Tools for Yacana

Tools for Yacana, a task-driven multi-agents framework for developers to create open source LLM-powered apps with ease.  
The GitHub sources are [here](https://github.com/rememberSoftwares/yacana) and the docs are [here](https://remembersoftwares.github.io/yacana/index.html).

## How to retrieve these tools

Currently, there is no PyPi package available, therefore you have to install manually.

Herebelow the following instructions:
```
$ pip install yacana
$ git clone "https://github.com/ychastre/yacana_tools.git"
$ pip install ./yacana_tools
```

## How to use these tools

Have a look on short documentation in ```docs``` directory.

### Examples

1. Use the FileReadTool tool with ```examples/file_read_tool_example.py```:

```python
from yacana import OllamaAgent, Task
from yacana_tools import FileReadTool

agent = OllamaAgent("example", "qwen3:4b-instruct")
file_read_tool = FileReadTool(".")
with open("test.txt", mode='w', encoding='utf-8') as fd:
    fd.write("Hello World!!!")
content = Task("Read the content of the file 'test.txt' and output only the content", agent, tools=[file_read_tool]).solve().content
print(f"The content of the file 'test.txt' is: \"{content}\"")
```

Run:
```
$ python file_read_tool_example.py

INFO: [PROMPT][To: example]: ...

INFO: [AI_RESPONSE][From: example]: ...

INFO: [PROMPT][To: example]: ...

INFO: [AI_RESPONSE][From: example]: {"file_name": "test.txt"}

INFO: [TOOL_RESPONSE][FileRead]: Hello World!!!

INFO: [PROMPT][To: example]: ...

INFO: [AI_RESPONSE][From: example]: Hello World!!!

The content of the file 'test.txt' is: "Hello World!!!"
```


2. Use the FileWriteTool tool:

```python
from yacana import OllamaAgent, Task
from yacana_tools import FileWriteTool

agent = OllamaAgent("example", "qwen3:4b-instruct")
file_write_tool = FileWriteTool(".")
Task("Write 'Hello World!!!' in the file 'test.txt'", agent, tools=[file_write_tool]).solve()
with open("test.txt", mode='r', encoding='utf-8') as fd:
    content = fd.readlines()
    print(f"The content of the file 'test.txt' is: \"{content[0]}\"")
```

Run:
```
$ python file_write_tool_example.py

INFO: [PROMPT][To: example]: ...

INFO: [AI_RESPONSE][From: example]: ...

INFO: [PROMPT][To: example]: ...

INFO: [AI_RESPONSE][From: example]: {"file_name": "test.txt", "content": "Hello World!!!"}

INFO: [TOOL_RESPONSE][FileWrite]: ...

The content of the file 'test.txt' is: "Hello World!!!"
```

## How to contribute

Prerequisites:
```
$ pip install pytest pytest-cov sphinx sphinx-rtd-theme
```

* Add your tool inside ```src/yacana_tools``` directory.

* Add your test file inside ```tests``` directory:

    Run:
    ```
    $ pytest --cov --cov-report html
    ```
    and check the correct coverage of your tool code.

* Update the documentation:
    
    Run:
    ```
    $ cd docs
    $ sphinx-quickstart
    $ nano source/conf.py
    update the file 'source/conf.py':
    add: import os
    add: import sys
    add: sys.path.insert(0, os.path.abspath('../../src'))
    replace: extensions = [] by:
             extensions = [
                'sphinx.ext.autodoc',
                'sphinx.ext.napoleon',
                'sphinx.ext.githubpages'
            ]
    replace: html_theme = '...' by:
             html_theme = 'sphinx_rtd_theme'
    $ sphinx-apidoc -f -o source ../src/yacana_tools
    $ make html
    ```
    and check the generated html files.