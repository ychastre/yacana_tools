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
from src.yacana_tools.file_list_tool import FileListTool # pylint: disable=C0413

AGENT_MODEL = "qwen3:4b-instruct"
DIR_NAME = "tmp"

class TestFileListTool:
    """
    TBC
    """

    @pytest.fixture
    def setup_and_teardown(self):
        """
        TBC
        """

        pathlib.Path(DIR_NAME).mkdir(parents=True, exist_ok=True)

        yield

        shutil.rmtree(DIR_NAME)

    @pytest.fixture
    def setup_and_teardown_1_file(self):
        """
        TBC
        """

        pathlib.Path(DIR_NAME).mkdir(parents=True, exist_ok=True)
        with open(f"{DIR_NAME}/alice.txt", mode='w', encoding='utf-8') as fd:
            fd.write("alice")

        yield

        shutil.rmtree(DIR_NAME)

    @pytest.fixture
    def setup_and_teardown_many_files(self):
        """
        TBC
        """

        pathlib.Path(DIR_NAME).mkdir(parents=True, exist_ok=True)
        with open(f"{DIR_NAME}/alice.txt", mode='w', encoding='utf-8') as fd:
            fd.write("alice")
        with open(f"{DIR_NAME}/bob.txt", mode='w', encoding='utf-8') as fd:
            fd.write("bob")
        with open(f"{DIR_NAME}/martin.txt", mode='w', encoding='utf-8') as fd:
            fd.write("martin")

        yield

        shutil.rmtree(DIR_NAME)

    @pytest.fixture
    def setup_and_teardown_1_dir(self):
        """
        TBC
        """

        pathlib.Path(f"{DIR_NAME}/toto").mkdir(parents=True, exist_ok=True)

        yield

        shutil.rmtree(DIR_NAME)

    @pytest.fixture
    def setup_and_teardown_many_dirs(self):
        """
        TBC
        """

        pathlib.Path(f"{DIR_NAME}/toto").mkdir(parents=True, exist_ok=True)
        pathlib.Path(f"{DIR_NAME}/titi").mkdir(parents=True, exist_ok=True)
        pathlib.Path(f"{DIR_NAME}/tata").mkdir(parents=True, exist_ok=True)

        yield

        shutil.rmtree(DIR_NAME)

    @pytest.fixture
    def setup_and_teardown_many_files_many_dirs(self):
        """
        TBC
        """

        pathlib.Path(DIR_NAME).mkdir(parents=True, exist_ok=True)
        pathlib.Path(f"{DIR_NAME}/toto").mkdir(parents=True, exist_ok=True)
        pathlib.Path(f"{DIR_NAME}/titi").mkdir(parents=True, exist_ok=True)
        pathlib.Path(f"{DIR_NAME}/tata").mkdir(parents=True, exist_ok=True)
        with open(f"{DIR_NAME}/alice.txt", mode='w', encoding='utf-8') as fd:
            fd.write("alice")
        with open(f"{DIR_NAME}/bob.txt", mode='w', encoding='utf-8') as fd:
            fd.write("bob")
        with open(f"{DIR_NAME}/martin.txt", mode='w', encoding='utf-8') as fd:
            fd.write("martin")

        yield

        shutil.rmtree(DIR_NAME)

    @pytest.fixture
    def file_list_tool(self):
        """
        TBC
        """

        return FileListTool(".", max_custom_error=0, max_call_error=0)

    @pytest.fixture
    def agent(self):
        """
        TBC
        """

        return OllamaAgent("Test", AGENT_MODEL, "You are test agent")

    def test_init_succeeded(self):
        """
        TBC
        """

        try:
            FileListTool(os.getcwd())
        except ValueError:
            assert False

    def test_init_failed_invalid_dir(self):
        """
        TBC
        """

        with pytest.raises(ValueError):
            FileListTool("bob")

    def test_llm_succeeded_empty_only_file(self, setup_and_teardown, file_list_tool, agent):
        """
        TBC
        """

        task = Task(f"List only files in the directory '{DIR_NAME}'. If no file found, output ONLY 'No file found'.", agent, tools=[file_list_tool])
        try:
            result = task.solve()
            assert "No file found" in result.content
        except MaxToolErrorIter:
            assert False

    def test_llm_succeeded_empty_only_dir(self, setup_and_teardown, file_list_tool, agent):
        """
        TBC
        """

        task = Task(f"List only directories in the directory '{DIR_NAME}'. If no directory found, output ONLY 'No directory found'.", agent, tools=[file_list_tool])
        try:
            result = task.solve()
            assert "No directory found" in result.content
        except MaxToolErrorIter:
            assert False

    def test_llm_succeeded_empty(self, setup_and_teardown, file_list_tool, agent):
        """
        TBC
        """

        task = Task(f"List all files and directories in the directory '{DIR_NAME}'. If no file and no directory found, output ONLY 'No file nor directory found'.", agent, tools=[file_list_tool])
        try:
            result = task.solve()
            assert "No file nor directory found" in result.content
        except MaxToolErrorIter:
            assert False

    def test_llm_succeeded_1_file_only_file(self, setup_and_teardown_1_file, file_list_tool, agent):
        """
        TBC
        """

        task = Task(f"List only files in the directory '{DIR_NAME}'. If no file found, output ONLY 'No file found'.", agent, tools=[file_list_tool])
        try:
            result = task.solve()
            assert "alice.txt" in result.content
            assert not "No file found" in result.content
        except MaxToolErrorIter:
            assert False

    def test_llm_succeeded_1_file_only_dir(self, setup_and_teardown_1_file, file_list_tool, agent):
        """
        TBC
        """

        task = Task(f"List only directories in the directory '{DIR_NAME}'. If no directory found, output ONLY 'No directory found'.", agent, tools=[file_list_tool])
        try:
            result = task.solve()
            assert "No directory found" in result.content
        except MaxToolErrorIter:
            assert False

    def test_llm_succeeded_1_file(self, setup_and_teardown_1_file, file_list_tool, agent):
        """
        TBC
        """

        task = Task(f"List all files and directories in the directory '{DIR_NAME}'. If no file and no directory found, output ONLY 'No file nor directory found'.", agent, tools=[file_list_tool])
        try:
            result = task.solve()
            assert "alice.txt" in result.content
            assert not "No file nor directory found" in result.content
        except MaxToolErrorIter:
            assert False

    def test_llm_succeeded_many_files_only_file(self, setup_and_teardown_many_files, file_list_tool, agent):
        """
        TBC
        """

        task = Task(f"List only files in the directory '{DIR_NAME}'. If no file found, output ONLY 'No file found'.", agent, tools=[file_list_tool])
        try:
            result = task.solve()
            assert "alice.txt" in result.content
            assert "bob.txt" in result.content
            assert "martin.txt" in result.content
            assert not "No file found" in result.content
        except MaxToolErrorIter:
            assert False

    def test_llm_succeeded_many_files_only_dir(self, setup_and_teardown_many_files, file_list_tool, agent):
        """
        TBC
        """

        task = Task(f"List only directories in the directory '{DIR_NAME}'. If no directory found, output ONLY 'No directory found'.", agent, tools=[file_list_tool])
        try:
            result = task.solve()
            assert "No directory found" in result.content
        except MaxToolErrorIter:
            assert False

    def test_llm_succeeded_many_files(self, setup_and_teardown_many_files, file_list_tool, agent):
        """
        TBC
        """

        task = Task(f"List all files and directories in the directory '{DIR_NAME}'. If no file and no directory found, output ONLY 'No file nor directory found'.", agent, tools=[file_list_tool])
        try:
            result = task.solve()
            assert "alice.txt" in result.content
            assert "bob.txt" in result.content
            assert "martin.txt" in result.content
            assert not "No file nor directory found" in result.content
        except MaxToolErrorIter:
            assert False

    def test_llm_succeeded_1_dir_only_file(self, setup_and_teardown_1_dir, file_list_tool, agent):
        """
        TBC
        """

        task = Task(f"List only files in the directory '{DIR_NAME}'. If no file found, output ONLY 'No file found'.", agent, tools=[file_list_tool])
        try:
            result = task.solve()
            assert "No file found" in result.content
        except MaxToolErrorIter:
            assert False

    def test_llm_succeeded_1_dir_only_dir(self, setup_and_teardown_1_dir, file_list_tool, agent):
        """
        TBC
        """

        task = Task(f"List only directories in the directory '{DIR_NAME}'. If no directory found, output ONLY 'No directory found'.", agent, tools=[file_list_tool])
        try:
            result = task.solve()
            assert "toto" in result.content
            assert not "No directory found" in result.content
        except MaxToolErrorIter:
            assert False

    def test_llm_succeeded_1_dir(self, setup_and_teardown_1_dir, file_list_tool, agent):
        """
        TBC
        """

        task = Task(f"List all files and directories in the directory '{DIR_NAME}'. If no file and no directory found, output ONLY 'No file nor directory found'.", agent, tools=[file_list_tool])
        try:
            result = task.solve()
            assert "toto" in result.content
            assert not "No file nor directory found" in result.content
        except MaxToolErrorIter:
            assert False

    def test_llm_succeeded_many_dirs_only_file(self, setup_and_teardown_many_dirs, file_list_tool, agent):
        """
        TBC
        """

        task = Task(f"List only files in the directory '{DIR_NAME}'. If no file found, output ONLY 'No file found'.", agent, tools=[file_list_tool])
        try:
            result = task.solve()
            assert "No file found" in result.content
        except MaxToolErrorIter:
            assert False

    def test_llm_succeeded_many_dirs_only_dir(self, setup_and_teardown_many_dirs, file_list_tool, agent):
        """
        TBC
        """

        task = Task(f"List only directories in the directory '{DIR_NAME}'. If no directory found, output ONLY 'No directory found'.", agent, tools=[file_list_tool])
        try:
            result = task.solve()
            assert "toto" in result.content
            assert "titi" in result.content
            assert "tata" in result.content
            assert not "No directory found" in result.content
        except MaxToolErrorIter:
            assert False

    def test_llm_succeeded_many_dirs(self, setup_and_teardown_many_dirs, file_list_tool, agent):
        """
        TBC
        """

        task = Task(f"List all files and directories in the directory '{DIR_NAME}'. If no file and no directory found, output ONLY 'No file nor directory found'.", agent, tools=[file_list_tool])
        try:
            result = task.solve()
            assert "toto" in result.content
            assert "titi" in result.content
            assert "tata" in result.content
            assert not "No file nor directory found" in result.content
        except MaxToolErrorIter:
            assert False

    def test_llm_succeeded_many_files_many_dirs_only_file(self, setup_and_teardown_many_files_many_dirs, file_list_tool, agent):
        """
        TBC
        """

        task = Task(f"List only files in the directory '{DIR_NAME}'. If no file found, output ONLY 'No file found'.", agent, tools=[file_list_tool])
        try:
            result = task.solve()
            assert "alice.txt" in result.content
            assert "bob.txt" in result.content
            assert "martin.txt" in result.content
            assert not "No file found" in result.content
        except MaxToolErrorIter:
            assert False

    def test_llm_succeeded_many_files_many_dirs_only_dir(self, setup_and_teardown_many_files_many_dirs, file_list_tool, agent):
        """
        TBC
        """

        task = Task(f"List only directories in the directory '{DIR_NAME}'. If no directory found, output ONLY 'No directory found'.", agent, tools=[file_list_tool])
        try:
            result = task.solve()
            assert "toto" in result.content
            assert "titi" in result.content
            assert "tata" in result.content
            assert not "No directory found" in result.content
        except MaxToolErrorIter:
            assert False

    def test_llm_succeeded_many_files_many_dirs(self, setup_and_teardown_many_files_many_dirs, file_list_tool, agent):
        """
        TBC
        """

        task = Task(f"List all files and directories in the directory '{DIR_NAME}'. If no file and no directory found, output ONLY 'No file nor directory found'.", agent, tools=[file_list_tool])
        try:
            result = task.solve()
            assert "alice.txt" in result.content
            assert "bob.txt" in result.content
            assert "martin.txt" in result.content
            assert "toto" in result.content
            assert "titi" in result.content
            assert "tata" in result.content
            assert not "No file nor directory found" in result.content
        except MaxToolErrorIter:
            assert False

    def test_llm_failed_not_provided_path(self, setup_and_teardown, file_list_tool, agent):
        """
        TBC
        """

        task = Task("List all files and directoriesin the directory ''. If no file found, output ONLY 'No file found'.", agent, tools=[file_list_tool])
        with pytest.raises(MaxToolErrorIter):
            task.solve()

    def test_llm_failed_not_relative_path(self, setup_and_teardown, file_list_tool, agent):
        """
        TBC
        """

        task = Task(f"List all files and directoriesin the directory '{os.getcwd()}/{DIR_NAME}'. If no file found, output ONLY 'No file found'.", agent, tools=[file_list_tool])
        with pytest.raises(MaxToolErrorIter):
            task.solve()

    def test_llm_failed_missing_dir(self, file_list_tool, agent):
        """
        TBC
        """

        task = Task(f"List all files and directoriesin the directory '{DIR_NAME}'. If no file found, output ONLY 'No file found'.", agent, tools=[file_list_tool])
        with pytest.raises(MaxToolErrorIter):
            task.solve()

    def test_llm_failed_not_canonical_path(self, setup_and_teardown, file_list_tool, agent):
        """
        TBC
        """

        task = Task(f"List all files and directories in the directory '../{DIR_NAME}'. If no file found, output ONLY 'No file found'.", agent, tools=[file_list_tool])
        with pytest.raises(MaxToolErrorIter):
            task.solve()
