from sys import argv, stderr
from sys import exit

import pandas as pd

from pandasviewer import show_dataframe

if len(argv) < 2:
    print("Usage: %s <sas7bdat file>" % (argv[0]), file=stderr)

    exit(1)

try:
    df = pd.read_sas(argv[1])
    show_dataframe(df)
except Exception as e:
    print("Error: %s" % (str(e)), file=stderr)
