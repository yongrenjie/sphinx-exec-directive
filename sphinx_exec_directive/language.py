from tempfile import NamedTemporaryFile
from pathlib import Path
import subprocess
import io
from contextlib import redirect_stdout
import re

from .runner import Runner, cd


class CRunner(Runner, default_executable="gcc", language="c"):
    def run(self):
        if self.executable in ["gcc", "clang"]:
            with NamedTemporaryFile(suffix=".c") as tempfile:
                tempfile.write(self.code_in.encode("utf-8"))
                tempfile.flush()
                filepath = Path(tempfile.name)
                compile_cmd = [self.executable, *self.args, tempfile.name]
                with cd(filepath.parent):
                    _ = subprocess.run(compile_cmd, check=True)
                    proc = subprocess.run(["./a.out"], capture_output=True, text=True)
                    self.code_out = proc.stdout
                    self.code_err = proc.stderr

        elif self.executable == "make":
            if self.project_dir is None:
                raise ValueError(":project_dir: option is needed for" "  Makefiles.")
            self.code_out, self.code_err = self.using_cmd(
                cmd=self.executable, args=self.args, dir=self.project_dir
            )

        else:
            self.raise_executable_not_found()


class CPPRunner(Runner, default_executable="g++", language="cpp"):
    def run(self):
        if self.executable in ["g++", "clang++"]:
            with NamedTemporaryFile(suffix=".cpp") as tempfile:
                tempfile.write(self.code_in.encode("utf-8"))
                tempfile.flush()
                filepath = Path(tempfile.name)
                compile_cmd = [self.executable, *self.args, tempfile.name]
                with cd(filepath.parent):
                    _ = subprocess.run(compile_cmd, check=True)
                    proc = subprocess.run(["./a.out"], capture_output=True, text=True)
                    self.code_out = proc.stdout
                    self.code_err = proc.stderr

        elif self.executable == "make":
            if self.project_dir is None:
                raise ValueError(":project_dir: option is needed for" "  Makefiles.")
            self.code_out, self.code_err = self.using_cmd(
                cmd=self.executable, args=self.args, dir=self.project_dir
            )

        else:
            self.raise_executable_not_found()


class HaskellRunner(Runner, default_executable="runghc", language="haskell"):
    def run(self):
        if self.executable == "runghc":
            self.code_out, self.code_err = self.using_pipe(
                code=self.code_in, cmd="runghc"
            )

        elif self.executable == "ghci":
            out, err = self.using_pipe(
                code=self.code_in, cmd="ghci", args=["-ignore-dot-ghci"]
            )
            out = out.replace("ghci>", "")
            out = re.sub("^.*?\n", "", out)
            out = out.replace("Leaving GHCi.\n", "")
            self.code_out = out
            self.code_err = err

        elif self.executable in ["cabal", "stack"]:
            if self.project_dir is None:
                raise ValueError(
                    ":project_dir: option is needed for" "  Cabal or Stack backends."
                )

            out, err = self.using_cmd(
                cmd=self.executable, args=self.args, dir=self.project_dir
            )
            out_stream = out.splitlines()
            for index, line in enumerate(out_stream):
                # Markers for the last line of build output. Anything
                # following this is the actual output produced by the
                # programme.
                if "Linking" in line or line == "Up to date":
                    i = index + 1
                    self.code_out = "\n".join(out_stream[i:])
                    self.code_err = err
                    break
            else:
                self.code_out = out
                self.code_err = err

        else:
            self.raise_executable_not_found()


class MatlabRunner(Runner, default_executable="matlab", language="matlab"):
    def run(self):
        if self.executable == "matlab":
            with NamedTemporaryFile(suffix=".m") as tempfile:
                tempfile.write(self.code_in.encode("utf-8"))
                tempfile.flush()
                filepath = Path(tempfile.name)
                cmd = ["matlab", "-batch", filepath.stem]
                with cd(filepath.parent):
                    proc = subprocess.run(cmd, capture_output=True, text=True)
                    self.code_out = proc.stdout
                    self.code_err = proc.stderr

        else:
            self.raise_executable_not_found()


class OCamlRunner(Runner, default_executable="ocaml", language="ocaml"):
    def run(self):
        if self.executable == "ocaml":
            with NamedTemporaryFile(suffix=".ml") as tempfile:
                tempfile.write(self.code_in.encode("utf-8"))
                tempfile.flush()
                filepath = Path(tempfile.name)
                with cd(filepath.parent):
                    proc = subprocess.run(
                        ["ocaml", tempfile.name], capture_output=True, text=True
                    )
                    self.code_out = proc.stdout
                    self.code_err = proc.stderr

        elif self.executable == "utop":
            self.code_out, self.code_err = self.using_pipe(
                code=self.code_in, cmd="utop"
            )

        elif self.executable == "dune":
            if self.project_dir is None:
                raise ValueError(":project_dir: option is needed for" "  Dune backend.")

            self.code_out, self.code_err = self.using_cmd(
                cmd=self.executable, args=self.args, dir=self.project_dir
            )

        else:
            self.raise_executable_not_found()


class PythonRunner(Runner, default_executable="exec", language="python"):
    def run(self):
        if self.executable == "exec":
            output_object = io.StringIO()
            with redirect_stdout(output_object):
                exec(self.code_in, self.context)
            self.code_out = output_object.getvalue()
            self.code_err = ""

        else:
            self.raise_executable_not_found()


class ShellRunner(Runner, default_executable="sh", language="shell"):
    def run(self):
        # TODO Change working directory (?)
        if self.executable in ["sh", "bash", "zsh", "fish"]:
            self.code_out, self.code_err = self.using_pipe(
                code=self.code_in, cmd=self.executable
            )

        else:
            self.raise_executable_not_found()
