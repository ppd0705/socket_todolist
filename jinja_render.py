import os

from jinja2 import Environment, FileSystemLoader


path = '{}/templates/'.format(os.path.dirname(__file__))
loader = FileSystemLoader(path)
env = Environment(loader=loader)


def render_template(path, **kwargs):
    t = env.get_template(path)
    return t.render(**kwargs)
