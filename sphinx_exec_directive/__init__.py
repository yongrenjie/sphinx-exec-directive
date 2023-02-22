import os
from hashlib import md5
from pathlib import Path
from typing import Optional

from docutils import nodes
from docutils.parsers.rst import Directive, Parser
from docutils.utils import new_document

from .parse_options import *
from .run import Runner
from .version import __version__


class _global:
    context = dict()
    previous_rst : Optional[Path] = None


class Exec(Directive):
    has_content = True
    required_arguments = 0
    optional_arguments = 1
    option_spec = {
        'context':     option_boolean,
        'cache':       option_boolean,
        'language':    option_language,
        'intertext':   option_str,
        'project_dir': option_str,
        'with':        option_str,
        'args':        option_str
    }

    def run(self):
        # Get the source file and if it has changed, then reset the context.
        current_rst = Path(self.state_machine.document.attributes['source'])
        if _global.previous_rst is None or _global.previous_rst != current_rst:
            _global.previous_rst = current_rst
            _global.context.clear()

        # Parse options
        save_context = self.options.get('context', False)
        language = self.options.get('language', 'python')
        project_dir = self.options.get('project_dir', '')
        opt_with = self.options.get('with', '')
        args = self.options.get ('args','').split()
        intertext = self.options.get('intertext', None)

        use_cache = (not save_context
                     and len(_global.context) == 0
                     and self.options.get('cache', True))
        from_file = len(self.arguments) > 0

        # Get some important paths. NOTE ABOUT PATHS:
        # Any variable ending in _pAD is an absolute path to a directory.
        #                        _pRD is a  relative path to a directory.
        #                        _pAF is an absolute path to a file.
        #                        _pRF is a  relative path to a file.
        top_level_sphinx_pAD = Path(setup.confdir)
        # Determine where to get source code from.
        if from_file:
            # File was specified; read in its contents.
            source_pAF = top_level_sphinx_pAD.joinpath(Path(self.arguments[0]))
            code_in = source_pAF.read_text()
        else:
            # Set the 'source file' to be the rst file which the code is in.
            # This path is already absolute.
            source_pAF = current_rst
            code_in = "\n".join(self.content)
        # If we are using a build system then the user file is actually a
        # project directory.

        # If caching was enabled, search for the cached result first.
        if use_cache:
            source_pRF = source_pAF.relative_to(top_level_sphinx_pAD)

            # Determine the file to store the cached output in (or read from)
            if from_file:
                source_identifier = source_pRF.with_suffix('')
                source_identifier = str(source_identifier).replace('/', '-')
                identifier = f"{source_identifier}-{language}-file.out"
                # e.g. ^ folder-yymmdd-filename-python-file.out
            else:
                source_identifier = source_pRF.with_suffix('')
                source_identifier = str(source_identifier).replace('/', '-')
                md5_hash = md5(code_in.encode('utf-8')).hexdigest()
                identifier = (f"{source_identifier}-{language}-"
                              f"inline-{md5_hash}.out")
                # e.g. ^ folder-yymmdd-python-inline-<HASH>.out
            build_pAD = Path(setup.app.doctreedir).parent
            output_pAF = build_pAD / "exec_directive" / identifier

            cache_found = (output_pAF.exists()
                           and (source_pAF.stat().st_mtime
                                < output_pAF.stat().st_mtime))
            if cache_found:
                # If the cached output was found and was modified more recently
                # than the source file, just read the output directly.
                with open(output_pAF, "r") as out_f:
                    code_out = out_f.read()
            else:
                # Caching requested but not found. Run the code again and cache
                # it. The context must be empty because otherwise caching would
                # have been disabled.
                runner = Runner(code_in=code_in,
                                language=language,
                                executable=opt_with,
                                args=args,
                                project_dir=project_dir,
                                context=None)
                runner.execute_code()
                code_out = runner.code_out
                if not output_pAF.parent.exists():
                    output_pAF.parent.mkdir()
                with open(output_pAF, "w") as out_f:
                    print(code_out, file=out_f, end="")
        else:
            # Caching was disabled, just run the code
            runner = Runner(code_in=code_in,
                            language=language,
                            executable=opt_with,
                            args=args,
                            project_dir=project_dir,
                            context=_global.context)
            runner.execute_code()
            code_out = runner.code_out

            # Update or reset the context if necessary
            if language == 'python':
                if save_context:
                    _global.context = runner.context
                else:
                    _global.context.clear()

        # Generate Sphinx output
        node_in = nodes.literal_block(code_in, code_in)
        node_out = nodes.literal_block(code_out, code_out)
        node_in['language'] = language
        node_out['language'] = 'none'

        if code_out.strip() == "":
            return [node_in]
        else:
            if intertext:
                internodes = new_document('intertext', self.state.document.settings)
                Parser().parse(intertext, internodes)
                return [node_in, *internodes.document.children, node_out]
            else:
                return [node_in, node_out]


def setup(app):
    setup.app = app
    setup.confdir = app.confdir
    app.add_directive("exec", Exec)

    return {
        'version': __version__,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
