from yacana import OllamaAgent, Task
from yacana_tools import FileWriteTool

agent = OllamaAgent("example", "qwen3:4b-instruct")
file_write_tool = FileWriteTool(".")
Task("Write 'Hello World!!!' in the file 'test.txt'", agent, tools=[file_write_tool]).solve()
with open("test.txt", mode='r', encoding='utf-8') as fd:
    content = fd.readlines()
    print(f"The content of the file 'test.txt' is: \"{content[0]}\"")
