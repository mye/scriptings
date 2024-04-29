"""
https://github.com/google/atheris
"""

import atheris

with atheris.instrument_imports():
    import sys

    import some_library


def TestOneInput(data):
    some_library.parse(data)


atheris.Setup(sys.argv, TestOneInput)
atheris.Fuzz()
