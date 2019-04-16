import sys
import os
pa = sys.executable

pa_loc = sys.path[0]
with open(pa_loc + '\\py_path.ini','w') as f:
	f.write(pa)
