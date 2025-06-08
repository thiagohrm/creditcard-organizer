import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import pytest

def test_import_tkinter():
    import tkinter
    assert tkinter is not None