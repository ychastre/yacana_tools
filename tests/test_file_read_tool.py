"""
TBC
"""

# pylint: disable=C0301,W0613,W0621

import os
import pathlib
import platform
import shutil
import sys

import pytest

from yacana import OllamaAgent, Task, MaxToolErrorIter
path = os.getcwd()
sys.path.append(path)
from src.yacana_tools.file_read_tool import FileReadTool # pylint: disable=C0413

AGENT_MODEL = "qwen3:4b-instruct"
DIR_NAME = "tmp"
FILE_NAME = f"{DIR_NAME}/alice.txt"
FILE_CONTENT = "Hello World!!!"

class TestFileReadTool:
    """
    TBC
    """

    @pytest.fixture
    def setup_and_teardown(self):
        """
        TBC
        """

        pathlib.Path(DIR_NAME).mkdir(parents=True, exist_ok=True)
        with open(FILE_NAME, "w", encoding="utf-8") as f:
            f.write(FILE_CONTENT)

        yield

        if os.path.exists(FILE_NAME):
            shutil.rmtree(DIR_NAME)

    @pytest.fixture
    def set_write_only_test_file(self):
        """
        TBC
        """

        os.chmod(FILE_NAME, mode=0o222)

    @pytest.fixture
    def file_read_tool(self):
        """
        TBC
        """

        return FileReadTool(os.getcwd(), max_custom_error=0, max_call_error=0)

    @pytest.fixture
    def agent(self):
        """
        TBC
        """

        return OllamaAgent("Test", AGENT_MODEL, "You are test agent")

    def test_init_successed(self):
        """
        TBC
        """

        try:
            FileReadTool(os.getcwd())
        except ValueError:
            assert False

    def test_init_failed_not_dir_path(self):
        """
        TBC
        """

        with pytest.raises(ValueError, match="Parameter 'root_dir' expected a valid directory"):
            FileReadTool("bob")

    def test_llm_successed(self, setup_and_teardown, file_read_tool, agent):
        """
        TBC
        """

        task = Task(f"Read the content of the file '{FILE_NAME}'", agent, tools=[file_read_tool])
        try:
            result = task.solve()
            assert result.content is not None
            assert result.content.find(FILE_CONTENT, 0) != -1
        except MaxToolErrorIter:
            assert False

    def test_llm_failed_not_provided_path(self, setup_and_teardown, file_read_tool, agent):
        """
        TBC
        """

        task = Task("Read the content of the file ''", agent, tools=[file_read_tool])
        with pytest.raises(MaxToolErrorIter):
            task.solve()

    def test_llm_failed_not_relative_path(self, setup_and_teardown, file_read_tool, agent):
        """
        TBC
        """

        task = Task(f"Read the content of the file '{os.getcwd()}/{FILE_NAME}'", agent, tools=[file_read_tool])
        with pytest.raises(MaxToolErrorIter):
            task.solve()

    def test_llm_failed_missing_file(self, file_read_tool, agent):
        """
        TBC
        """

        task = Task(f"Read the content of the file '{FILE_NAME}'", agent, tools=[file_read_tool])
        with pytest.raises(MaxToolErrorIter):
            task.solve()

    def test_llm_failed_is_directory_path(self, setup_and_teardown, file_read_tool, agent):
        """
        TBC
        """

        task = Task(f"Read the content of the file '{DIR_NAME}'", agent, tools=[file_read_tool])
        with pytest.raises(MaxToolErrorIter):
            task.solve()

    def test_llm_failed_write_only_file(self, setup_and_teardown, set_write_only_test_file, file_read_tool, agent):
        """
        TBC
        """

        if platform.system() == "Windows":
            assert True
        else:
            task = Task(f"Read the content of the file '{FILE_NAME}'", agent, tools=[file_read_tool])
            with pytest.raises(MaxToolErrorIter):
                task.solve()

    def test_llm_failed_not_canonical_path(self, setup_and_teardown, file_read_tool, agent):
        """
        TBC
        """

        task = Task(f"Read the content of the file '../{FILE_NAME}'", agent, tools=[file_read_tool])
        with pytest.raises(MaxToolErrorIter):
            task.solve()
