import os
import io
import subprocess
from hashlib import md5
from contextlib import redirect_stdout
from pathlib import Path
from tempfile import NamedTemporaryFile

from docutils import nodes
from docutils.parsers.rst import directives, Directive


context = dict()


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


def execute_code(code, process, globals_dict=None):
    if process == 'python':
        if globals_dict is None:
            globals_dict = {}

        output_object = io.StringIO()
        with redirect_stdout(output_object):
            exec(code, globals_dict)
        code_out = output_object.getvalue()

    elif process == 'haskell':
        proc = subprocess.Popen(['runghc'],
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        out, err = proc.communicate(input=code.encode('utf-8'))
        # Log any stderr.
        if err is not None and err.strip() != "":
            print(err)
        code_out = out.decode('utf-8')

    elif process == 'matlab':
        # MATLAB can't pipe, so we need to dump to a tempfile.
        with NamedTemporaryFile(suffix=".m") as tempfile:
            tempfile.write(code.encode('utf-8'))
            tempfile.flush()   # mandatory, or else it will be empty
            filepath = Path(tempfile.name)
            # Then execute MATLAB.
            with cd(filepath.parent):
                comp_proc = subprocess.run(['matlab', '-batch', filepath.stem],
                                           capture_output=True, text=True)
                out = comp_proc.stdout
                err = comp_proc.stderr
        # Log any stderr.
        if err is not None and err.strip() != "":
            print(err)
        code_out = out

    else:
        raise ValueError(f"process type '{process}' not recognised.")

    return code_out


def _option_boolean(arg):
    """Copied from matplotlib plot_directive."""
    if not arg or not arg.strip():
        # no argument given, assume used as a flag
        return True
    elif arg.strip().lower() in ('no', '0', 'false'):
        return False
    elif arg.strip().lower() in ('yes', '1', 'true'):
        return True
    else:
        raise ValueError('"%s" unknown boolean' % arg)


def _option_process(arg):
    if arg is None:
        return 'python'
    else:
        return arg.lower()


class Exec(Directive):
    has_content = True
    required_arguments = 0
    optional_arguments = 1
    option_spec = {
        'context': _option_boolean,
        'cache': _option_boolean,
        'process': _option_process,
    }

    def run(self):
        # Parse options
        save_context = self.options.get('context', False)
        # Don't cache if the user requests saving context, or if the context is
        # nonempty. The reason is because the global_dict can't be updated just
        # by reading in code from a file (as opposed to executing it). I can't
        # be bothered to fix this (and truthfully I don't see an easy way,
        # short of serialising the entire contents of `context`).
        cache = (not save_context
                 and len(context) == 0
                 and self.options.get('cache', True))
        process = self.options.get('process', 'python')

        # Determine whether input is to be read from a file, or directly from
        # the exec block's contents.
        from_file = len(self.arguments) > 0

        # Get some important paths.
        # NOTE ABOUT PATHS:
        # Any variable ending in _pAD is an absolute path to a directory.
        #                        _pRD is a  relative path to a directory.
        #                        _pAF is an absolute path to a file.
        #                        _pRF is a  relative path to a file.
        top_level_sphinx_pAD = Path(setup.confdir)

        # Determine where to get source code from.
        if from_file:
            # Set the 'source file' to be the specified file. The argument to
            # the exec block is given as a relative path, so has to be made
            # absolute with respect to the top-level Sphinx directory.
            source_pAF = top_level_sphinx_pAD.joinpath(Path(self.arguments[0]))
            code_in = source_pAF.read_text()
        else:
            # Set the 'source file' to be the rst file which the code is in.
            # This path is already absolute.
            source_pAF = Path(self.state_machine.document.attributes['source'])
            code_in = "\n".join(self.content)

        # Look up the output in the cache, or execute the code.
        if cache:
            source_pRF = source_pAF.relative_to(top_level_sphinx_pAD)

            # Figure out where to dump the output.
            if from_file:
                source_identifier = source_pRF.with_suffix('')
                source_identifier = str(source_identifier).replace('/', '-')
                identifier = f"{source_identifier}-{process}-file.out"
                # ^ folder-yymmdd-filename-python-file.out
            else:
                source_identifier = source_pRF.with_suffix('')
                source_identifier = str(source_identifier).replace('/', '-')
                md5_hash = md5(code_in.encode('utf-8')).hexdigest()
                identifier = (f"{source_identifier}-{process}-"
                              f"inline-{md5_hash}.out")
                # ^ folder-yymmdd-python-inline-<HASH>.out
            build_pAD = Path(setup.app.doctreedir).parent
            output_pAF = build_pAD / "exec_directive" / identifier

            # Look for the cached output. If not found, execute it.
            cache_found = (
                output_pAF.exists()
                and source_pAF.stat().st_mtime < output_pAF.stat().st_mtime
            )
            if cache_found:
                with open(output_pAF, "r") as out_f:
                    code_out = out_f.read()
            else:
                code_out = execute_code(code_in, process, context)
                if not output_pAF.parent.exists():
                    output_pAF.parent.mkdir()
                with open(output_pAF, "w") as out_f:
                    print(code_out, file=out_f, end="")
        else:  # caching was disabled, execute it
            code_out = execute_code(code_in, process, context)

        # Reset the context if it's not meant to be preserved
        if not save_context:
            context.clear()

        node_in = nodes.literal_block(code_in, code_in)
        node_out = nodes.literal_block(code_out, code_out)
        node_in['language'] = process
        node_out['language'] = 'none'

        if code_out.strip() == "":
            return [node_in]
        else:
            return [node_in, node_out]


def setup(app):
    setup.app = app
    setup.confdir = app.confdir
    app.add_directive("exec", Exec)

    return {
        'version': '0.5',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
