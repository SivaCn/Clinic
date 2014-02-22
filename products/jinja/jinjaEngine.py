
import os
from jinja2 import Environment, FileSystemLoader

# Capture our current directory
THIS_DIR = os.path.dirname(os.path.abspath(__file__))

class Jinja(object):
    """
    """
    def __init__(self):
        """
        """
        pass

    def renderTemplate(self, _templateLoc=r'/templates', _template='login.html', **kwargs):
        """
        """
        # Create the jinja2 environment.
        # Notice the use of trim_blocks, which greatly helps control whitespace.

        j2_env = Environment(loader=FileSystemLoader(os.path.join(THIS_DIR, _templateLoc)),
                             trim_blocks=True)

        template = j2_env.get_template(_template)

        return template.render(title='Hellow Gist from GutHub', **kwargs)
