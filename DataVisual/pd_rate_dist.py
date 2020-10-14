import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import csv
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


def public_freq_labeling(view_rate):
    if view_rate < 2.5:
        return 0
    elif view_rate < 5:
        return 1
    elif view_rate < 7.5:
        return 2
    elif view_rate < 10:
        return 3
    elif view_rate < 12.5:
        return 4
    elif view_rate < 15:
        return 5
    elif view_rate < 17.5:
        return 6
    elif view_rate < 20:
        return 7
    elif view_rate < 22.5:
        return 8
    elif view_rate < 25:
        return 9
    elif view_rate < 27.5:
        return 10
    elif view_rate < 30:
        return 11
    elif view_rate < 32.5:
        return 12
    elif view_rate < 35:
        return 13
    elif view_rate < 37.5:
        return 14
    elif view_rate < 40:
        return 15
    elif view_rate < 42.5:
        return 16
    elif view_rate < 45:
        return 17
    elif view_rate < 47.5:
        return 18
    elif view_rate < 50:
        return 19
    else:
        return 20


pd_file = open('../kbs_pd.csv', 'r', encoding='utf-8')
pd_rdr = csv.reader(pd_file)
public_drama = {}
cable_drama = {}
publicTV = ('kbs1', 'kbs2', 'mbc', 'sbs')

for line in pd_rdr:
    sp_line = line
    pd_idx = 1
    drama_name = sp_line[pd_idx]

    while (drama_name != ''):
        if (sp_line[pd_idx+3] != ''):
            if (sp_line[pd_idx+1] in publicTV):
                public_drama[drama_name] = float(sp_line[pd_idx+3])
            else:
                cable_drama[drama_name] = float(sp_line[pd_idx+3])

        pd_idx = pd_idx+4
        if (pd_idx >  84):
            break
        drama_name = sp_line[pd_idx]


pd_file.close()

public_rates= list(public_drama.values())
cable_rates = list(cable_drama.values())
public_x = [0 for i in range(len(public_rates))]
cable_x = [1 for i in range(len(cable_rates))]
public_freq_label = [public_freq_labeling(x) for x in public_rates]
cable_freq_label = [public_freq_labeling(x) for x in cable_rates]

public_freq = [0 for i in range(21)]
cable_freq = [0 for i in range(21)]

for label in public_freq_label:
    public_freq[label] += 1
for label in cable_freq_label:
    cable_freq[label] += 1

# print(public_freq)
# print(cable_freq)
# print(public_drama)
# print(cable_drama)
# for key, value in sorted(public_drama.items()):
#     print(key, ":", value)
# for key, value in sorted(cable_drama.items()):
#     print(key, ":", value)
# print(public_rates, cable_rates)
# print(max(public_rates), min(public_rates))
# print(max(cable_rates), min(cable_rates))

# plt.scatter(public_rates, public_rates)
# plt.scatter(cable_rates, cable_rates)
# # plt.xlabel()
# plt.ylabel('view rate')
# # plt.title()
# plt.legend(['public', 'cable'])
# plt.show()

fig, axs = plt.subplots(1, 2)
axs[0].hist(public_rates, range=(0, 70), bins=40)
axs[1].hist(cable_rates, range=(0, 30), bins=25, color='orange')

axs[0].set_title('public')
axs[1].set_title('cable')
for ax in axs.flat:
    ax.set(xlabel='view rate', ylabel='frequency')

plt.show()