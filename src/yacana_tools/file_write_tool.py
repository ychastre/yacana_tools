"""
File Write Tool for Yacana

This module provides a tool to write or save content to a file in the local filesystem.
"""

# pylint: disable=C0301
# pylint: disable=R0913,R0917

import os
from pathlib import Path
from yacana import Tool, ToolError, ToolType

class FileWriteTool(Tool):
    """
    A tool for writing content to a file in the local filesystem.

    This class provides functionality to write the contents of a file.
    It ensures that the provided path is valid and that the file exists
    before attempting to write it.
    This class is based to Tool class.

    Parameters
    ----------
    rootdir : str
        The root directory path where the file will be written.
        Defaults to ".".
    create_dir : bool
        If True, the directory will be created if it doesn't exist.
        Defaults to False.
    force : bool
        If True, the file will be overwritten if it already exists.
        Defaults to False.
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
        The root directory path where the file will be written.
        Defaults to ".".
    create_dir : bool
        If True, the directory will be created if it doesn't exist.
        Defaults to False.
    force : bool
        If True, the file will be overwritten if it already exists.
        Defaults to False.

    Raises
    ------
    ValueError
        If the provided path is not a valid directory.
    """

    def __init__(self,
                 rootdir: str = ".",
                 create_dir: bool = False,
                 force: bool = False,
                 optional: bool = False,
                 max_custom_error: int = 5,
                 max_call_error: int = 5,
                 tool_type: ToolType = ToolType.YACANA):

        # Validate that 'path' is a valid directory
        if not Path(rootdir).is_dir():
            raise ValueError("Parameter 'rootdir' expected a valid directory")

        # Set all attributes
        self.rootdir = os.path.normpath(rootdir)
        self.create_dir = create_dir
        self.force = force

        # Initialize the parent Tool class
        super().__init__(
            tool_name="FileWrite",
            function_description="Write or save content to file in local filesystem",
            function_ref=self.write_content,
            optional=optional,
            max_custom_error=max_custom_error,
            max_call_error=max_call_error,
            tool_type=tool_type
        )


    def write_content(self,
                     file_name: str,
                     content: str) -> None:
        """
        Write the provided content to a file.

        Parameters
        ----------
        file_name : str
            The name of the file to be written.
            Note: the path of this file MUST be relative.
        content : str
            The content to be written to the file.
        
        Returns
        -------
        None

        Raises
        ------
        ToolError
            If the file name is not provided or is invalid.
            If the file does not exist or cannot be written.
            If the content is not provided or is invalid.
        """

        # Validate that 'file_name' is not empty
        if not file_name:
            raise ToolError("File name was not provided or None.")

        # Validate that the path of the file is relative
        if Path(file_name).is_absolute():
            raise ToolError("File name has not a relative path.")

        # Validate that 'content' is not empty
        if not content or content == "":
            raise ToolError("Content was not provided or is empty.")

        # Construct the full path to the file
        long_file_name = os.path.join(self.rootdir, file_name)

        # Normalize the full file path
        long_file_name = os.path.normpath(long_file_name)

        # Validate that the full file path is inside the path
        if long_file_name.find(self.rootdir, 0) == -1:
            raise ToolError("File name has not in root directory.")

        long_dir_name = os.path.dirname(long_file_name)

        # Check if the directory exists
        if Path(long_dir_name).exists():
            # Check if the directory is a valid directory
            if Path(long_dir_name).is_dir():
                # Check if the file exists
                if Path(long_file_name).exists():
                    # Check if the file is a valid file
                    if Path(long_file_name).is_file():
                        # If force is False and file exists, raise an error
                        if not self.force:
                            raise ToolError("File already exists but cannot be overwritten.")
                    else:
                        # If the file is not a valid file, raise an error
                        raise ToolError("File name is not a valid path.")
            else:
                # If the path is not a valid directory, raise an error
                raise ToolError("File name is not a valid path.")
        else:
            # If the directory does not exist and create_dir is True, create it
            if self.create_dir:
                try:
                    Path(long_dir_name).mkdir(parents=True, exist_ok=True)
                except OSError as error:
                    raise ToolError(str(error)) from error
            else:
                # If the directory does not exist and create_dir is False, raise an error
                raise ToolError("File cannot be written because directory does not exist.")

        # Write the content to the file
        try:
            with open(long_file_name, mode='w', encoding='utf-8') as fd:
                fd.write(content)
        except OSError as error:
            raise ToolError(str(error)) from error
