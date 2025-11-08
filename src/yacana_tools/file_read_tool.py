"""
File Read Tool for Yacana

This module provides a tool for reading content from files in the local filesystem.
"""

# pylint: disable=C0301
# pylint: disable=R0913,R0917

import os
from pathlib import Path
from yacana import Tool, ToolError, ToolType

class FileReadTool(Tool):
    """
    A tool for reading content from file in the local filesystem.

    This class provides functionality to read the contents of a file and return it
    as a string. It ensures that the provided path is valid and that the file exists
    before attempting to read it.
    This class is based to Tool class.

    Parameters
    ----------
    rootdir : str
        The root directory path where the file is located.
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
    rootdir : str
        The root directory path where the file is located.
        Defaults to ".".

    Raises
    ------
    TypeError
        If the provided path is not a string.
    ValueError
        If the provided path is not a valid directory.
    """

    def __init__(self,
                 rootdir: str = ".",
                 optional: bool = False,
                 max_custom_error: int = 5,
                 max_call_error: int = 5,
                 tool_type: ToolType = ToolType.YACANA):

        # Validate that the path is a valid directory
        if not Path(rootdir).is_dir():
            raise ValueError("Parameter 'rootdir' expected a valid directory")

        # Set all attributes
        self.rootdir = os.path.normpath(rootdir)

        # Call the parent class constructor to initialize the tool
        super().__init__(
            tool_name="FileRead",
            function_description="Read or load content from a file in the local filesystem and return the content",
            function_ref=self.read_content,
            optional=optional,
            max_custom_error=max_custom_error,
            max_call_error=max_call_error,
            tool_type=tool_type
        )


    def read_content(self, file_name: str) -> str:
        """
        Read the content of a file.

        Parameters
        ----------
        file_name : str
            The name of the file to read.
            Note: the path of this file MUST be relative.
        
        Returns
        -------
        str
            The content of the file.

        Raises
        ------
        ToolError
            If the file name is not provided or is invalid.
            If the file does not exist or cannot be read.
        """

        # Validate that the file name is provided
        if not file_name:
            raise ToolError("File name was not provided or None.")

        # Validate that the path of the file is relative
        if Path(file_name).is_absolute():
            raise ToolError("File name is not a relative path.")

        # Construct the full file path
        long_file_name = os.path.join(self.rootdir, file_name)

        # Normalize the full file path
        long_file_name = os.path.normpath(long_file_name)

        # Validate that the full file path is inside the path
        if long_file_name.find(self.rootdir, 0) == -1:
            raise ToolError("File name is not in root directory.")

        # Validate that the file exists
        if not Path(long_file_name).is_file():
            raise ToolError("File does not exist.")

        # Attempt to read the file
        try:
            with open(long_file_name, mode='r', encoding='utf-8') as fd:
                content = fd.readlines()
                content = "".join(content)  # Join lines into a single string
        except OSError as error:
            raise ToolError(str(error)) from error

        return content
