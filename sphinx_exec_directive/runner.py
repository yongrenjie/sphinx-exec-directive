import os
import subprocess
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Optional


class cd:
    """
    Context manager for changing the current working directory.
    Taken from https://stackoverflow.com/a/13197763
    """

    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, _etype, _value, _traceback):
        os.chdir(self.savedPath)


class Runner(ABC):
    """
    A runner is "that which runs the code", i.e., an object that defines the
    entire external process. This is an abstract base class and must be
    subclassed for each language used.

    Methods
    -------
    execute_code :
        Executes the code stored in ``self.code_in`` using the specifications
        in the other instance variables. The output is stored in the
        ``self.code_out`` variable.
    """

    default_executable: str
    language: str

    _REGISTRY = {}

    def __init_subclass__(cls, /, language, default_executable, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.default_executable = default_executable
        cls.language = language
        cls._REGISTRY[language] = cls

    @classmethod
    def get_runner(cls, language):
        try:
            return cls._REGISTRY[language]
        except KeyError:
            raise ValueError(f"No runner for language '{language}'.")

    def __init__(
        self, code_in, executable=None, project_dir=None, args=None, context=None
    ):
        """
        Parameters
        ----------
        code_in : string
            The code to be executed.
        language : string
            The language the code is written in.
        executable : string, optional
            The executable used to run the code, or some kind of identifier
            which dictates how the code will be run. Can be None, in which case
            a default must be chosen.
        args : list of string, optional
            Command-line arguments to be passed to the executable. Defaults to
            an empty list.
        project_dir : string or pathlib.Path, optional
            Directory to run a command from. Only necessary for certain
            runners. Defaults to current working directory.
            (TODO: What is CWD when Sphinx is building?)
        context : dict, optional
            Preserved variables for use in context-sharing Python code blocks.
            Defaults to an empty dictionary.
        """
        self.code_in = code_in
        self.executable = self.default_executable if executable is None else executable
        self.args = [] if args is None else args
        self.project_dir = Path.cwd() if project_dir is None else Path(project_dir)
        self.context = {} if context is None else context

    @abstractmethod
    def run(self) -> None:
        """
        This method must be implemented by subclasses. It must set the `code_out`
        and `code_err` instance attributes to be strings containing the standard
        output and standard error of the code, respectively.
        """
        raise NotImplementedError

    def raise_executable_not_found(self) -> None:
        msg = (
            f"The executable '{self.executable}' is not recognised for"
            f" the language '{self.language}'."
        )
        raise ValueError(msg)

    @staticmethod
    def using_pipe(
        code: str, cmd: str, args: Optional[list[str]] = None
    ) -> tuple[str, str]:
        """
        Execute code by piping code into a command.

        Parameters
        ----------
        code : string
            The code to be executed.
        cmd : string
            The executable to be used.
        args : list of string, optional
            Extra command-line arguments to be passed.

        Returns
        -------
        (out, err) : tuple of string
            Standard output and standard error.
        """
        if args is None:
            args = []
        proc = subprocess.run([cmd] + args, input=code, capture_output=True, text=True)
        out = proc.stdout
        err = proc.stderr
        return out, err

    @staticmethod
    def using_cmd(
        cmd: str, args: Optional[list[str]] = None, dir: Optional[str | Path] = None
    ) -> tuple[str, str]:
        """
        Execute pre-existing code by simply running a given command.

        Parameters
        ----------
        cmd : string
            The executable to be used.
        args : list of string, optional
            Extra command-line arguments to be passed.
        dir : string or Path, optional
            Directory the command is to be run from. If not specified, uses the
            user's home directory.

        Returns
        -------
        out : string
            Standard output.
        err : string
            Standard error.
        """
        if dir is None:
            dir = Path.home()
        else:
            dir = Path(dir)
        if args is None:
            args = []
        with cd(dir):
            proc = subprocess.run([cmd] + args, capture_output=True, text=True)
            out = proc.stdout
            err = proc.stderr
        return out, err

    @staticmethod
    def log_stderr(err):
        # TODO: Use Sphinx logging
        if err is not None and len(err.strip()) > 0:
            print(err)
