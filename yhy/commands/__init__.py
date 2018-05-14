from importlib import import_module
from pkgutil import iter_modules


def build(cli,
          path=__path__,
          package=__package__):
    """Build CLI dynamically based on submodules."""
    for _, name, ispkg in iter_modules(path):
        module = import_module(f'.{name}', package)
        if ispkg:
            build(cli.group(name)(module.group),
                  module.__path__,
                  module.__package__)
        else:
            cli.command(name)(module.command)
