#!npython

# ./run.py function_name parameter1 parameter2

import sys

from test import *
from images import *

if __name__ == "__main__":
    function = sys.argv[1]
    arguments = sys.argv[2:]
    function_call = "%s(%s)" % (function, ",".join(arguments))
    eval(function_call)
