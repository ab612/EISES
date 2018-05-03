### csv_to_JSON converts a data stream CSV to A standardized JSON file format for
### fact factories to process
__author__="Madison.Soden"
__date__="Thu May  3 13:54:50 2018"
__license__="NA?"
__version__="csv_to_JSON"
__email__="madison.soden@gmail.com"
__status__="Production"

import pandas as pd

with open('file.dat', 'r') as fin:
    data = fin.read().splitlines(True)
header= data[:1]
with open('file.dat', 'w') as fout:
    fout.writelines(data[1:])
foo = pd.read_csv("file.dat")
foo.drop(foo.index[1])

