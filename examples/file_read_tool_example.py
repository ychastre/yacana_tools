from yacana import OllamaAgent, Task
from yacana_tools import FileReadTool

agent = OllamaAgent("example", "qwen3:4b-instruct")
file_read_tool = FileReadTool(".")
with open("test.txt", mode='w', encoding='utf-8') as fd:
    fd.write("Hello World!!!")
content = Task("Read the content of the file 'test.txt' and output only the content", agent, tools=[file_read_tool]).solve().content
print(f"The content of the file 'test.txt' is: \"{content}\"")
