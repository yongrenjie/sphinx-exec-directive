import io
import os
import re
import subprocess
from pathlib import Path
from contextlib import redirect_stdout
from tempfile import NamedTemporaryFile


class cd:
    """
    Context manager for changing the current working directory. Taken from
    https://stackoverflow.com/a/13197763/7115316.
    """
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


class Runner:
    """
    A runner is "that which runs the code", i.e., an object that defines the
    entire external process.

    Methods
    -------
    execute_code :
        Executes the code stored in ``self.code_in`` using the specifications
        in the other instance variables. The output is stored in the
        ``self.code_out`` variable.
    """

    def __init__(self, code_in, language, executable,
                 project_dir, args, context):
        """
        Parameters
        ----------
        code_in : string
            The code to be executed.
        language : string
            The language the code is written in. If syntax highlighting is
            desired, must be set to one of the available lexers in Pygments
            (see https://pygments.org/languages/).
        executable : string, optional
            The executable used to run the code, or some kind of identifier
            which dictates how the code will be run. Can be None, in which case
            a default must be chosen.
        args : list of string, optional
            Command-line arguments to be passed to the executable. Defaults to
            an empty list.
        project_dir : string, optional
            Directory to run a command from. Only necessary for certain
            runners.
        context : dict, optional
            Preserved variables for use in context-sharing Python code blocks.
            Defaults to an empty dictionary.
        """
        self.code_in = code_in
        self.language = language
        self.executable = executable
        self.args = [] if args is None else args
        self.project_dir = project_dir
        self.context = {} if context is None else context

    def execute_code(self):
        try:
            func = getattr(self, f'execute_code_{self.language}')
        except AttributeError:
            raise ValueError(f'Language {self.language} is not supported.')
        func()
    
    def execute_code_python(self):
        if self.executable is None:
            self.executable = 'exec'

        if self.executable == 'exec':
            output_object = io.StringIO()
            with redirect_stdout(output_object):
                exec(self.code_in, self.context)
            self.code_out = output_object.getvalue()

        else:
            raise ValueError(make_error_message(self.executable,
                                                self.language))

    def execute_code_c(self):
        if self.executable is None:
            self.executable = 'gcc'

        if self.executable in ['gcc', 'clang']:
            with NamedTemporaryFile(suffix='.c') as tempfile:
                tempfile.write(self.code_in.encode('utf-8'))
                tempfile.flush()
                filepath = Path(tempfile.name)
                compile_cmd = [self.executable, *self.args, tempfile.name]
                with cd(filepath.parent):
                    _ = subprocess.run(compile_cmd, check=True)
                    proc = subprocess.run(['./a.out'], capture_output=True,
                                          text=True)
                    out = proc.stdout
                    err = proc.stderr
                log_stderr(err)
                self.code_out = out

        elif self.executable == 'make':
            if self.project_dir is None:
                raise ValueError(':project_dir: option is needed for'
                                 '  Makefiles.')
            out, _ = using_cmd(cmd=self.executable,
                               args=self.args,
                               dir=self.project_dir)
            self.code_out = out

        else:
            raise ValueError(make_error_message(self.executable,
                                                self.language))

    def execute_code_cpp(self):
        if self.executable is None:
            self.executable = 'g++'

        if self.executable in ['g++', 'clang++']:
            with NamedTemporaryFile(suffix='.cpp') as tempfile:
                tempfile.write(self.code_in.encode('utf-8'))
                tempfile.flush()
                filepath = Path(tempfile.name)
                compile_cmd = [self.executable, *self.args, tempfile.name]
                with cd(filepath.parent):
                    _ = subprocess.run(compile_cmd, check=True)
                    proc = subprocess.run(['./a.out'], capture_output=True,
                                          text=True)
                    out = proc.stdout
                    err = proc.stderr
                log_stderr(err)
                self.code_out = out

        elif self.executable == 'make':
            if self.project_dir is None:
                raise ValueError(':project_dir: option is needed for'
                                 '  Makefiles.')
            out, _ = using_cmd(cmd=self.executable,
                               args=self.args,
                               dir=self.project_dir)
            self.code_out = out

        else:
            raise ValueError(make_error_message(self.executable,
                                                self.language))

    def execute_code_haskell(self):
        # Default Haskell runner is runghc.
        if self.executable is None:
            self.executable = 'runghc'

        if self.executable == 'runghc':
            out, _ = using_pipe(code=self.code_in,
                                cmd='runghc')
            self.code_out = out

        elif self.executable == 'ghci':
            out, _ = using_pipe(code=self.code_in,
                                cmd='ghci',
                                args=['-ignore-dot-ghci'])
            out = out.replace('ghci>', '')
            out = re.sub('^.*?\n', '', out)
            out = out.replace('Leaving GHCi.\n', '')
            self.code_out = out

        elif self.executable in ['cabal', 'stack']:
            if self.project_dir is None:
                raise ValueError(':project_dir: option is needed for'
                                 '  Cabal or Stack backends.')

            out, _ = using_cmd(cmd=self.executable,
                               args=self.args,
                               dir=self.project_dir)
            out_stream = out.splitlines()
            for index, line in enumerate(out_stream):
                # Markers for the last line of build output. Anything
                # following this is the actual output produced by the
                # programme.
                if 'Linking' in line or line == 'Up to date':
                    i = index + 1
                    self.code_out = '\n'.join(out_stream[i:])
                    break
            else:
                self.code_out = out

        else:
            raise ValueError(make_error_message(self.executable,
                                                self.language))

    def execute_code_matlab(self):
        with NamedTemporaryFile(suffix='.m') as tempfile:
            tempfile.write(self.code_in.encode('utf-8'))
            tempfile.flush()
            filepath = Path(tempfile.name)
            cmd = ['matlab', '-batch', filepath.stem]
            with cd(filepath.parent):
                proc = subprocess.run(cmd, capture_output=True, text=True)
                out = proc.stdout
                err = proc.stderr
            log_stderr(err)
            self.code_out = out

    def execute_code_ocaml(self):
        if self.executable is None:
            self.executable = 'ocaml'

        if self.executable == 'ocaml':
            with NamedTemporaryFile(suffix='.ml') as tempfile:
                tempfile.write(self.code_in.encode('utf-8'))
                tempfile.flush()
                filepath = Path(tempfile.name)
                with cd(filepath.parent):
                    proc = subprocess.run(['ocaml', tempfile.name],
                                          capture_output=True, text=True)
                    out = proc.stdout
                    err = proc.stderr
                log_stderr(err)
                self.code_out = out

        elif self.executable == 'utop':
            out, _ = using_pipe(code=self.code_in, cmd='utop')
            self.code_out = out

        elif self.executable == 'dune':
            if self.project_dir is None:
                raise ValueError(':project_dir: option is needed for'
                                 '  Dune backend.')

            out, _ = using_cmd(cmd=self.executable,
                               args=self.args,
                               dir=self.project_dir)
            self.code_out = out
            # out_stream = out.splitlines()
            # for index, line in enumerate(out_stream):
            #     # Markers for the last line of build output. Anything
            #     # following this is the actual output produced by the
            #     # programme.
            #     if 'Linking' in line or line == 'Up to date':
            #         i = index + 1
            #         self.code_out = '\n'.join(out_stream[i:])
            #         break
            # else:
            #     self.code_out = out

        else:
            raise ValueError(make_error_message(self.executable,
                                                self.language))

    def execute_code_shell(self):
        out, _ = using_pipe(code=self.code_in, cmd='sh')
        self.code_out = out


def using_pipe(code, cmd, args=None):
    """
    Execute code by piping code into a command.

    Parameters
    ----------
    code : string
        The code to be run.
    cmd : string
        The executable to be used.
    args : list of string, optional
        Extra command-line arguments to be passed.
    
    Returns
    -------
    out : string
        Standard output.
    err : string
        Standard error.
    """
    cmd = [cmd] + (args if args is not None else [])
    proc = subprocess.run(cmd, input=code,
                          capture_output=True, text=True)
    out = proc.stdout
    err = proc.stderr

    log_stderr(err)
    return out, err


def using_cmd(cmd, args=None, dir='~'):
    """
    Execute pre-existing code by simply running a given command.

    Parameters
    ----------
    cmd : string
        The executable to be used.

    args : list of string, optional
        Extra command-line arguments to be passed.

    dir : string or pathlib.Path, optional
        Directory the command is to be run from. If not specified, uses the
        user's home directory.
    
    Returns
    -------
    out : string
        Standard output.
    err : string
        Standard error.
    """
    cmd = [cmd] + (args if args is not None else [])
    with cd(dir):
        proc = subprocess.run(cmd, capture_output=True, text=True)
        out = proc.stdout
        err = proc.stderr
    log_stderr(err)
    return out, err


def log_stderr(err):
    # TODO: Use Sphinx logging
    if err is not None and len(err.strip()) > 0:
        print(err)


def make_error_message(exec, lang):
    return (f"The executable '{exec}' is not recognised for the language"
            f" '{lang}'.")
