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
