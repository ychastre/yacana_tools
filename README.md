# Tools for Yacana

Tools for Yacana, a task-driven multi-agents framework for developers to create open source LLM-powered apps with ease.  
The GitHub source of Yacana is [here](https://github.com/rememberSoftwares/yacana) and its documentation is [here](https://remembersoftwares.github.io/yacana/index.html).

There are the following tools available:

* File Read
* File Write
* File List
* File Tree

## How to retrieve these tools

Currently, there is no PyPi package available, therefore you have to install manually.

Herebelow the following instructions:
```
$ pip install yacana
$ git clone "https://github.com/ychastre/yacana_tools.git"
$ pip install ./yacana_tools
```

## How to use these tools

Have a look at the documentation avalaible [here](https://ychastre.github.io/yacana_tools/).

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

2. Use the FileListTool tool:

```python
import pathlib
from yacana import OllamaAgent, Task
from yacana_tools import FileListTool

if not pathlib.Path('docs').exists():
    pathlib.Path('docs').mkdir(parents=True, exist_ok=True)
    pathlib.Path('docs/sources').mkdir(parents=True, exist_ok=True)
    pathlib.Path('docs/build').mkdir(parents=True, exist_ok=True)
    with open('docs/alice.txt', mode='w', encoding='utf-8') as fd:
        fd.write('alice')
    with open('docs/bob.txt', mode='w', encoding='utf-8') as fd:
        fd.write('bob')

agent = OllamaAgent("example", "qwen3:4b-instruct")
file_list_tool = FileListTool(".")
content = Task("Get the list of files and directories in the directory 'docs' and output only the content. If no file nor no directory found, output ONLY 'no file nor directory found.'", agent, tools=[file_list_tool]).solve().content
print(f"All files and directories in 'docs' are:\n{content}")

```

Run:
```
$ python file_write_tool_example.py

INFO: [PROMPT][To: example]: ...

INFO: [AI_RESPONSE][From: example]: ...

INFO: [PROMPT][To: example]: ...

INFO: [AI_RESPONSE][From: example]: ...{"dir_name": "docs"}

INFO: [TOOL_RESPONSE][FileList]: ...

INFO: [PROMPT][To: example]: ...

INFO: [AI_RESPONSE][From: example]: * [file] alice.txt
* [file] bob.txt
* [directory] build
* [directory] sources

All files and directories in 'docs' are:
* [file] alice.txt
* [file] bob.txt
* [directory] build
* [directory] sources
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
    replace: html_theme = 'alabaster' by:
             html_theme = 'sphinx_rtd_theme'
    add: add_module_names = False
    $ sphinx-apidoc -f -o source ../src/yacana_tools
    $ nano source/index.rst
    update the file 'source/index.rst':
    remove: Add your content using ``reStructuredText`` syntax. See the
            `reStructuredText <https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html>`_
            documentation for details.
    replace: .. toctree::
                :maxdepth: 2
                :caption: Contents:
            by:
            .. toctree::
                :maxdepth: 2
                :caption: Contents:

                modules
    $ nano source/yacana_tools.rst
    update the file 'source/yacana_tools.rst":
    remove: Submodules
            ----------
    remove: Module contents
            ---------------

            .. automodule:: yacana_tools
                :members:
                :show-inheritance:
                :undoc-members:
    replace: yacana\_tools.file\_list\_tool module
        by:
            file\_list\_tool module
    $ make html
    ```
    and check the generated html files.