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
    A runner is "that which runs the code", i.e., an object that
    defines the entire external process.
    """
    def __init__(self, code_in, language, executable,
                 project_dir, args, context):

        # The code to be executed.
        self.code_in = code_in

        # The language the code is written in. If syntax highlighting is
        # desired, must be set to one of the available lexers in Pygments
        # (see https://pygments.org/languages/).
        self.language = language

        # The executable used to run the code, or some kind of identifier which
        # dictates how the code will be run.
        self.executable = executable

        # Command-line arguments to be passed to the executable.
        if args is None:
            self.args = []
        else:
            self.args = args

        # Optional; to be used for running code within projects.
        self.project_dir = project_dir

        # Context to be used for running Python code blocks.
        self.context = context

    def execute_code(self):
        """Executes `self.code_in` using the remaining instance variables. This
        method must set the `self.code_out` instance variable."""

        if self.language == 'python':
            if self.context is None:
                self.context = {}
            output_object = io.StringIO()
            with redirect_stdout(output_object):
                exec(self.code_in, self.context)
            self.code_out = output_object.getvalue()

        elif self.language == 'haskell':
            post_process = []
            payload = []

            # check that the runner with field is set
            # and set post-process hooks
            if not self.executable:
                self.executable = 'runghc' # default is runghc, no hooks

            if self.executable == 'ghci':
                # TODO: properly add in an args argument to execute_code_with_pipe
                self.executable = 'ghci -ignore-dot-ghci'.split()
                # if running with ghci then we post process the output to remove
                # ghci specific text
                post_process += [lambda s: s.replace("ghci>",""),
                                 lambda s: re.sub("^.*?\n", "", s),
                                 lambda s: s.replace("Leaving GHCi.\n", "").rstrip()
                                ]

            # do the business
            if self.executable in ['cabal', 'stack']:
                if self.project_dir is None:
                    raise ValueError("Project_dir must be set to run with Cabal or Stack backends")

                with cd(Path(self.project_dir)):
                    payload   = [self.executable] + self.args
                    comp_proc = subprocess.run(payload, capture_output=True, text=True)
                    out = comp_proc.stdout
                    err = comp_proc.stderr

                    out_stream = self.code_out.splitlines()
                    for index, line in enumerate(out_stream):
                        if "Linking" in line:
                            i = index + 1
                            self.code_out = '\n'.join(out_stream[i:])
                            break # only want first hit, and we are guarenteed
                                  # that linking is in the list because you
                                  # cannot run a binary without linking!

                # Log
                if err is not None and err.strip() != '':
                    print(err) # should use sphinx logger


            else:
                self.code_out = execute_code_with_pipe(self.executable,
                                                       self.code_in,
                                                       post_process)

        elif self.language == 'matlab':
            # MATLAB can't pipe, so we need to dump to a tempfile.
            with NamedTemporaryFile(suffix='.m') as tempfile:
                tempfile.write(self.code_in.encode('utf-8'))
                tempfile.flush()   # mandatory, or else it will be empty
                filepath = Path(tempfile.name)
                # Then execute MATLAB.
                with cd(filepath.parent):
                    comp_proc = subprocess.run(['matlab', '-batch', filepath.stem],
                                               capture_output=True, text=True)
                    out = comp_proc.stdout
                    err = comp_proc.stderr
            # Log any stderr.
            if err is not None and len(err.strip()) > 0:
                print(err)
            self.code_out = out

        elif self.language == 'shell':
            self.code_out = execute_code_with_pipe(['sh'], self.code_in)

        else:
            raise ValueError(f"language '{self.language}' not recognised.")


def execute_code_with_pipe(command, code_in, post_process=None):
    proc = subprocess.Popen(command,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    out, err = proc.communicate(input=code_in.encode("utf-8"))

    # apply all post processing functions now that we have output
    out = out.decode('utf-8')
    if post_process is not None:
        for f in post_process:
            out = f(out)

    # Log any stderr.
    if err is not None and len(err.strip()) > 0:
        print(err)

    return out
