import os
import io
import subprocess
from hashlib import md5
from contextlib import redirect_stdout
from pathlib import Path

from docutils import nodes
from docutils.parsers.rst import directives, Directive


context = dict()


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
                                stdout=subprocess.PIPE)
        out, err = proc.communicate(input=code.encode('utf-8'))
        # Log any stderr.
        if err is not None and err.strip() != "":
            print(err)
        code_out = out.decode('utf-8')

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
    elif arg.lower() in ['python', 'haskell']:
        return arg.lower()
    else:
        raise ValueError(f"':process: {arg}' not recognised")


class Exec(Directive):
    has_content = True
    required_arguments = 0
    optional_arguments = 3
    option_spec = {
        'context': _option_boolean,
        'cache': _option_boolean,
        'process': _option_process,
    }

    def run(self):
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

        code_in = "\n".join(self.content)

        if cache:
            # Get some important paths
            top_level_sphinx_dir = Path(setup.confdir)
            # ^ ~/dphil/nbsphinx
            source_f = Path(self.state_machine.document.attributes['source'])
            # ^ ~/dphil/nbsphinx/hmbc/yymmdd.rst
            # Figure out where to dump the output.
            source_rel_f = source_f.relative_to(top_level_sphinx_dir)
            # ^ hmbc/yymmdd.rst
            source_identifier = str(source_rel_f)[:-4].replace('/', '-')
            # ^ hmbc-yymmdd
            build_dir = Path(setup.app.doctreedir).parent
            # ^ ~/dphil/nbsphinx/dirhtml (or whatever)
            md5_hash = md5(code_in.encode('utf-8')).hexdigest()
            # ^ HASH
            output_f = (build_dir
                         / "exec_directive"
                         / f"{source_identifier}-{process}-{md5_hash}")
            # ^ ~/dphil/nbsphinx/dirhtml/exec_directive/
            #     hmbc-yymmdd-python-HASH

            cache_found = (output_f.exists()
                           and
                           source_f.stat().st_mtime < output_f.stat().st_mtime)

            if cache_found:
                with open(output_f, "r") as out_f:
                    code_out = out_f.read()
            else:
                code_out = execute_code(code_in, process, context)
                if not output_f.parent.exists():
                    output_f.parent.mkdir()
                with open(output_f, "w") as out_f:
                    print(code_out, file=out_f, end="")
        else:  # cache not enabled
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
        'version': '0.4',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
