import io
from contextlib import redirect_stdout

from docutils import nodes
from docutils.parsers.rst import Directive


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
    optional_arguments = 1
    option_spec = {
        'context': _option_boolean,
    }

    def run(self):
        save_context = self.options.get('context', False)

        code_in = "\n".join(self.content)
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
    app.add_directive("exec", Exec)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
