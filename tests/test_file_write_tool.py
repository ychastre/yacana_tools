"""
TBC
"""

# pylint: disable=C0301

import os
import pathlib
import shutil
import sys

import pytest
from yacana import OllamaAgent, Task, MaxToolErrorIter

path = os.getcwd()
sys.path.append(path)
from src.yacana_tools.file_write_tool import FileWriteTool # pylint: disable=C0413

AGENT_MODEL = "qwen3:4b-instruct"
DIR_NAME = "tmp"
FILE_NAME = f"{DIR_NAME}/alice.txt"
FILE_CONTENT = "Hello World!!!"
NOT_EXISTING_DIR_NAME = "tmp2"

class TestFileWriteTool:
    """
    TBC
    """

    @pytest.fixture
    def file_write_tool(self):
        """
        TBC
        """

        return FileWriteTool(os.getcwd(), max_custom_error=0, max_call_error=0)

    @pytest.fixture
    def file_write_tool_with_force(self):
        """
        TBC
        """

        return FileWriteTool(os.getcwd(), force=True, max_custom_error=0, max_call_error=0)

    @pytest.fixture
    def file_write_tool_with_create_dir(self):
        """
        TBC
        """

        return FileWriteTool(os.getcwd(), create_dir=True, max_custom_error=0, max_call_error=0)

    @pytest.fixture
    def agent(self):
        """
        TBC
        """

        return OllamaAgent("Test", AGENT_MODEL, "You are test agent")

    @pytest.fixture
    def setup_and_teardown(self):
        """
        TBC
        """

        shutil.rmtree(DIR_NAME, ignore_errors=True)
        pathlib.Path(DIR_NAME).mkdir(parents=True, exist_ok=True)

        yield

        shutil.rmtree(DIR_NAME, ignore_errors=True)

    @pytest.fixture
    def setup_and_teardown_existing_file(self):
        """
        TBC
        """

        if not os.path.exists(FILE_NAME):
            pathlib.Path(DIR_NAME).mkdir(parents=True, exist_ok=True)
            with open(FILE_NAME, mode='w', encoding='utf-8') as fd:
                fd.write(FILE_NAME)

        yield

        shutil.rmtree(DIR_NAME, ignore_errors=True)

    @pytest.fixture
    def setup_and_teardown_no_existing_dir(self):
        """
        TBC
        """

        shutil.rmtree(NOT_EXISTING_DIR_NAME, ignore_errors=True)

        yield

        shutil.rmtree(NOT_EXISTING_DIR_NAME, ignore_errors=True)

    def test_init_succeeded(self):
        """
        TBC
        """

        try:
            FileWriteTool(os.getcwd())
        except ValueError:
            assert False

    def test_init_failed_not_dir_path(self):
        """
        TBC
        """

        with pytest.raises(ValueError, match="Parameter 'root_dir' expected a valid directory"):
            FileWriteTool("bob")

    def test_llm_succeeded(self, setup_and_teardown, file_write_tool, agent): # pylint: disable=W0613
        """
        TBC
        """

        task = Task(f"Write the content '{FILE_CONTENT}' in the file '{FILE_NAME}'", agent, tools=[file_write_tool])
        try:
            task.solve()
            assert os.path.exists(FILE_NAME)
            with open(FILE_NAME, mode='r', encoding='utf-8') as fd:
                content = fd.readlines()
                assert content[0].find(FILE_CONTENT) != -1
        except MaxToolErrorIter:
            assert False

    def test_llm_failed_not_provided_path(self, setup_and_teardown, file_write_tool, agent): # pylint: disable=W0613
        """
        TBC
        """

        task = Task("Write the content '{FILE_CONTENT}' in the file ''", agent, tools=[file_write_tool])
        with pytest.raises(MaxToolErrorIter):
            task.solve()

    def test_llm_failed_not_relative_path(self, setup_and_teardown, file_write_tool, agent): # pylint: disable=W0613
        """
        TBC
        """

        task = Task(f"Write the content '{FILE_CONTENT}' in '{os.getcwd()}/{FILE_NAME}'", agent, tools=[file_write_tool])
        with pytest.raises(MaxToolErrorIter):
            task.solve()

    def test_llm_failed_not_provided_content(self, setup_and_teardown, file_write_tool, agent): # pylint: disable=W0613
        """
        TBC
        """

        task = Task(f"Write in '{FILE_NAME}'", agent, tools=[file_write_tool])
        with pytest.raises(MaxToolErrorIter):
            task.solve()

    def test_llm_failed_not_canonical_path(self, setup_and_teardown, file_write_tool, agent): # pylint: disable=W0613
        """
        TBC
        """

        task = Task(f"Write the content '{FILE_CONTENT}' in the file '../{FILE_NAME}'", agent, tools=[file_write_tool])
        with pytest.raises(MaxToolErrorIter):
            task.solve()

    def test_llm_failed_not_file_path(self, setup_and_teardown, file_write_tool, agent): # pylint: disable=W0613
        """
        TBC
        """

        task = Task(f"Write the content '{FILE_CONTENT}' in the file '{DIR_NAME}'", agent, tools=[file_write_tool])
        with pytest.raises(MaxToolErrorIter):
            task.solve()

    def test_llm_failed_existing_file(self, setup_and_teardown_existing_file, file_write_tool, agent): # pylint: disable=W0613
        """
        TBC
        """

        task = Task(f"Write the content '{FILE_CONTENT}' in the file '{FILE_NAME}'", agent, tools=[file_write_tool])
        with pytest.raises(MaxToolErrorIter):
            task.solve()

    def test_llm_succeeded_force_existing_file(self, setup_and_teardown_existing_file, file_write_tool_with_force, agent): # pylint: disable=W0613
        """
        TBC
        """

        task = Task(f"Write the content '{FILE_CONTENT}' in the file '{FILE_NAME}'", agent, tools=[file_write_tool_with_force])
        try:
            task.solve()
            assert os.path.exists(FILE_NAME)
            with open(FILE_NAME, mode='r', encoding='utf-8') as fd:
                content = fd.readlines()
                assert content[0].find(FILE_CONTENT) != -1
        except MaxToolErrorIter:
            assert False

    def test_llm_failed_invalid_path(self, setup_and_teardown, file_write_tool, agent): # pylint: disable=W0613
        """
        TBC
        """

        task = Task(f"Write the content '{FILE_CONTENT}' in the file 'README.md/alice.txt'", agent, tools=[file_write_tool])
        with pytest.raises(MaxToolErrorIter):
            task.solve()

    def test_llm_failed_not_existing_dir(self, setup_and_teardown_no_existing_dir, file_write_tool, agent): # pylint: disable=W0613
        """
        TBC
        """

        task = Task(f"Write the content '{FILE_CONTENT}' in the file '{NOT_EXISTING_DIR_NAME}/alice.txt'", agent, tools=[file_write_tool])
        with pytest.raises(MaxToolErrorIter):
            task.solve()

    def test_llm_succeeded_create_dir(self, setup_and_teardown_no_existing_dir, file_write_tool_with_create_dir, agent): # pylint: disable=W0613
        """
        TBC
        """

        task = Task(f"Write the content '{FILE_CONTENT}' in the file '{NOT_EXISTING_DIR_NAME}/alice.txt'", agent, tools=[file_write_tool_with_create_dir])
        try:
            task.solve()
            assert os.path.exists(f"{NOT_EXISTING_DIR_NAME}/alice.txt")
            with open(f"{NOT_EXISTING_DIR_NAME}/alice.txt", mode='r', encoding='utf-8') as fd:
                content = fd.readlines()
                assert content[0].find(FILE_CONTENT) != -1
        except MaxToolErrorIter:
            assert False
