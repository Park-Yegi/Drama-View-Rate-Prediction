import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import csv
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


pd_file = pd.read_csv('../kbs_mini.csv', encoding='utf-8')
rate_list = np.array(pd_file['first_rate'])

plt.hist(rate_list, range=(0,25), bins=20)
plt.title('the first episode')
plt.xlabel('first view rate')
plt.ylabel('frequency')
plt.show()