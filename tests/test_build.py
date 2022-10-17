import sys
import shutil
from subprocess import PIPE, Popen
from pathlib import Path

import pytest


def test_sphinx_build(tmp_path):
    """
    Ensure that Sphinx build completes without errors or warnings.
    """
    source_dir = tmp_path / 'rst_source'
    shutil.copytree(Path(__file__).parent / 'rst_source', source_dir)
    build_dir = tmp_path / 'build_html'

    cmd = [sys.executable, '-m', 'sphinx', '-W', '-E', '-b', 'html',
           str(source_dir), str(build_dir)]
    proc = Popen(cmd, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    out, err = proc.communicate()

    assert proc.returncode == 0, \
        f"sphinx build failed with stdout:\n{out}\nstderr:\n{err}\n"
    if err:
        pytest.fail(f"sphinx build emitted the following warnings:\n{err}")

    assert build_dir.is_dir()
