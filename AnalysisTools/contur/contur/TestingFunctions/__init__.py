from .TesterFunctions import *

import os
if os.getenv('CONTURTEST') == 'old':
	print "Using old hand-coded data. *_HF_EW and *_HF_MU will be missing."
	from .StaticData import *
else:
	from .StaticDB import *
	init_dbs()
del os
