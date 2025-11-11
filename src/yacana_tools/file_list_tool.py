"""
File List Tool for Yacana

This module provides a tool for listing files and subdirectories in the local filesystem.
"""

# pylint: disable=C0301
# pylint: disable=R0913,R0917

import os
from pathlib import Path
from yacana import Tool, ToolError, ToolType

class FileListTool(Tool):
    """
    A tool for listing files and subdirectories in the local filesystem.

    This class provides functionality to list all files and subdirectories and
    return them as a string. It ensures that the provided path is valid and that
    the directory exists before attempting to list files and subdirectories.
    This class is based to Tool class.

    Parameters
    ----------
    root_dir : str
        The root directory path from where the directory is located.
        Defaults to ".".
    optional : bool
        Whether the tool is optional.
        Defaults to False.
    max_custom_error : int
        Maximum number of custom errors allowed.
        Defaults to 5.
    max_call_error : int
        Maximum number of call errors allowed.
        Defaults to 5.
    tool_type : ToolType
        Type of tool (e.g., YACANA, OPENAI).
        Defaults to YACANA.

    Attributes
    ----------
    root_dir : str
        The root directory path where the file is located.
        Defaults to ".".

    Raises
    ------
    ValueError
        If the provided path is not a valid directory.
    """

    def __init__(self,
                 root_dir: str = ".",
                 optional: bool = False,
                 max_custom_error: int = 5,
                 max_call_error: int = 5,
                 tool_type: ToolType = ToolType.YACANA):

        # Validate that the parameter 'rootdir' is a valid directory
        root_dir = os.path.normpath(root_dir)
        root_dir = os.path.abspath(root_dir)

        if not Path(root_dir).is_dir():
            raise ValueError("Parameter 'root_dir' expected a valid directory")

        # Set all attributes
        self.root_dir = root_dir

        # Call the parent class constructor to initialize the tool
        super().__init__(
            tool_name="FileList",
            function_description="List all files and directories in a directory in the local filesystem and return the list.",
            function_ref=self.get_file_list,
            optional=optional,
            max_custom_error=max_custom_error,
            max_call_error=max_call_error,
            tool_type=tool_type
        )

    def get_file_list(self, dir_name: str = ".") -> str:
        """
        List all files and subdirectories of a directory.

        Note: this function is expected to be called the LLM.

        Parameters
        ----------
        dir_name: str
            The name of the directory where to list all files and subdirectories.
            Note: the path of this directory MUST be relative.
        
        Returns
        -------
        str
            The list of all files and subdirectories in the directory.

        Raises
        ------
        ToolError
            If the directory name is not provided or is invalid.
            If the directory does not exist.
        """

        # Validate that the directory name is provided
        if not dir_name:
            raise ToolError("Directory name was not provided or None.")

        # Validate that the path of the directory is relative
        if Path(dir_name).is_absolute():
            raise ToolError("Directory name is not a relative path.")

        # Construct the full directory path
        long_dir_name = os.path.join(self.root_dir, dir_name)

        # Normalize the full directory path
        long_dir_name = os.path.normpath(long_dir_name)

        # Validate that the full directory path is inside the root directory path
        if long_dir_name.find(self.root_dir, 0) == -1:
            raise ToolError("Directory name is not in root directory.")

        # Validate that the directory exists
        if not Path(long_dir_name).is_dir():
            raise ToolError("Directory does not exist.")

        # List all files and subdirectories in the directory
        elements = list(Path(long_dir_name).iterdir())
        content = ""
        for index, element in enumerate(elements):
            if index > 0:
                content = content + "\n"
            content = content + "* "
            if Path(element).is_dir():
                content = content + "[directory] "
            else:
                content = content + "[file] "
            content = content + element.name

        if content == "":
            content = "No file nor directory found."

        return content
