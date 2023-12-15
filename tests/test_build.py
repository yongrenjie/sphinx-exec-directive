import os
import platform
import sys
import shutil
import warnings
from subprocess import PIPE, Popen
from pathlib import Path

import pytest


def test_sphinx_build(tmp_path):
    """
    Ensure that Sphinx build completes without errors or warnings.

    Note that this doesn't check in any way that the output is actually correct
    in any way. In order to do so, set the environment variable

        SPHINX_EXEC_DIRECTIVE_OPENHTML=1

    This will use either `open` or `xdg-open` to open the built HTML pages so
    that they can be inspected for correctness.
    """
    source_dir = tmp_path / "rst_source"
    shutil.copytree(Path(__file__).parent / "rst_source", source_dir)
    build_dir = tmp_path / "build_html"

    cmd = [
        sys.executable,
        "-m",
        "sphinx",
        "-W",
        "-E",
        "-b",
        "html",
        str(source_dir),
        str(build_dir),
    ]
    proc = Popen(cmd, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    out, err = proc.communicate()

    assert (
        proc.returncode == 0
    ), f"sphinx build failed with stdout:\n{out}\nstderr:\n{err}\n"
    if err:
        pytest.fail(f"sphinx build emitted the following warnings:\n{err}")

    # open HTML if requested
    if os.environ.get("SPHINX_EXEC_DIRECTIVE_OPENHTML", "") == "1":
        s = platform.system()
        if s == "Darwin":
            Popen(["open", f"{str(build_dir)}/index.html"])
        elif s == "Linux":
            Popen(["xdg-open", f"{str(build_dir)}/index.html"])
        else:
            warnings.warn("unsupported operating system for opening html")

    assert build_dir.is_dir()
