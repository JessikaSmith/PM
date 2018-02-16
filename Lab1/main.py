
from Tools import *
import numpy as np
import asciitable

data = asciitable.read('ringwaydata.txt',fill_values=('---',None))
data = data.filled()
data.dtype.names = ('year','mm','tmax_deg','tmin_deg','af_days','rain_mm','sun_hours')
max_deg = list(data['tmax_deg'])
max_deg = [float(x) for x in max_deg if x != 'N/A']
m = Distribution(max_deg)
#m.show_histogram()
#m.kernel_density(1)

est = Estimator(max_deg)
est.estimate_params(3)