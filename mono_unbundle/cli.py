"""
Extract DLLs from a Xamarin ELF bundle.

https://github.com/tjg1/mono_unbundle

Usage:
    mono_unbundle [options] [--] FILE PATH
    mono_unbundle --version

Arguments:
    FILE             mono_mkbundle ELF library (libmonodroid_bundle_app.so)
    PATH             Output directory for extracted DLL files.

Options:
    --help, -h       Print this help messsage.
    -v, --verbose    Output verbose messages.
    --version        Display version information.
"""
from docopt import docopt
from . import MonoBundle
from . import __version__


def cli():
    arguments = docopt(__doc__)
    if arguments["--version"]:
        print("mono_unbundle %s" % __version__)
    file = arguments['FILE']
    path = arguments['PATH']
    verbose = arguments['--verbose']

    MonoBundle(file, path, verbose).extract_all()


if __name__ == "__main__":
    cli()

