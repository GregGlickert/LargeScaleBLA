import numpy as np
import pandas as pd
import h5py
import shutil
import random
import matplotlib.pyplot as plt
from scipy.stats import ttest_rel # for paired t-test
from scipy.stats import ttest_ind

"""
losers = []
winners = []
for i in range(64):
    losers.append(0)
for i in range(120):
    losers.append(1)
for i in range(173):
    losers.append(2)
for i in range(138):
    losers.append(3)
for i in range(87):
    losers.append(4)
for i in range(46):
    losers.append(5)
for i in range(19):
    losers.append(6)
for i in range(6):
    losers.append(7)
for i in range(4):
    losers.append(8)

for i in range(2):
    winners.append(0)
for i in range(13):
    winners.append(1)
for i in range(26):
    winners.append(2)
for i in range(42):
    winners.append(3)
for i in range(28):
    winners.append(4)
for i in range(16):
    winners.append(5)
for i in range(7):
    winners.append(6)
for i in range(6):
    winners.append(7)
for i in range(1):
    winners.append(8)
for i in range(1):
    winners.append(9)

z_score, p_value = ttest_ind(losers,winners)
print('z-score is', z_score)
print('p-value from zscore is', p_value)

plt.hist(losers,density=True)
plt.title("losers")
plt.figure(2)
plt.title("Winners")
plt.hist(winners,density=True)
plt.show()
"""

df = pd.read_csv('connection table.csv')
data = df[df['cell id']<800]
data = data[data['cell id']>1]
winners = data[data['is winner?']=="Winner"]
losers = data[data['is winner?']=="Loser"]

z_score, p_value = ttest_ind(losers['disynapses'],winners['disynapses'])
print('z-score is', z_score)
print('p-value from zscore is', p_value)

print(losers['disynapses'].describe())
print(winners['disynapses'].describe())

plt.hist(losers['disynapses'], density=True,color='r',label='Losers')
plt.xlabel('Disynaptic Connections')
plt.ylabel("Probability")
plt.hist(winners['disynapses'], density=True,color='b',label='Winners')
plt.legend()
plt.savefig("winners.svg")