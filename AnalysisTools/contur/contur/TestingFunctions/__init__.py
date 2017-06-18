from .TesterFunctions import *

import os

if os.getenv('CONTURTEST') != 'new':
	print "Using hand-coded data"
	from .StaticData import *
else:
	print "Using DB"
	from .StaticDB import *
	init_dbs()

del os
