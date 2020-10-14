import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import csv
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


pd_file = pd.read_csv('../kbs_each_ep.csv', encoding='utf-8')
rate_list = np.array(pd_file['view_rate'])


plt.hist(rate_list, range=(0,50), bins=50)
plt.title('kbs mini series')
plt.xlabel('view rate')
plt.ylabel('frequency')
plt.show()