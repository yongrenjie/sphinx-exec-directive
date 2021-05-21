import os
import io
from hashlib import md5
from contextlib import redirect_stdout
from pathlib import Path

from docutils import nodes
from docutils.parsers.rst import directives, Directive


context = dict()


def execute_code(code, globals_dict=None):
    if globals_dict is None:
        globals_dict = {}

    output_object = io.StringIO()
    with redirect_stdout(output_object):
        exec(code, globals_dict)
    code_out = output_object.getvalue()

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


class Exec(Directive):
    has_content = True
    required_arguments = 0
    optional_arguments = 2
    option_spec = {
        'context': _option_boolean,
        'cache': _option_boolean,
    }

    def run(self):
        save_context = self.options.get('context', False)
        # Don't cache if the user requests saving context. The reason is
        # because the global_dict can't be updated just by reading in code from
        # a file (as opposed to executing it). I can't be bothered to fix this.
        cache = not save_context and self.options.get('cache', True)

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
                         / f"{source_identifier}-{md5_hash}")
            # ^ ~/dphil/nbsphinx/dirhtml/exec_directive/hmbc-yymmdd-HASH

            cache_found = (output_f.exists()
                           and
                           source_f.stat().st_mtime < output_f.stat().st_mtime)

            if cache_found:
                with open(output_f, "r") as out_f:
                    code_out = out_f.read()
            else:
                code_out = execute_code(code_in, context)
                if not output_f.parent.exists():
                    output_f.parent.mkdir()
                with open(output_f, "w") as out_f:
                    print(code_out, file=out_f, end="")
        else:  # cache not enabled
            code_out = execute_code(code_in, context)

        # Reset the context if it's not meant to be preserved
        if not save_context:
            context.clear()

        node_in = nodes.literal_block(code_in, code_in)
        node_out = nodes.literal_block(code_out, code_out)
        node_in['language'] = 'python'
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
        'version': '0.2',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
