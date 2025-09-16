import pandas as pd
import numpy as np

from plotnine import *
from plotnine.data import *




p = ggplot(aes(x='displ', y='cty'), mpg)
p = p + geom_point(aes(color='factor(cyl)'))

p.save(filename = 'test3.png', height=5, width=5, units = 'in', dpi=1000)