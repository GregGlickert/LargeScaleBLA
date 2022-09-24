import matplotlib.pyplot as plt
import numpy as np

data = np.array([56.9, 23.1, 9.3, 10.7])
mylabels = ["PyrA", "PyrC", "FSI", "LTS"]

def func(pct, allvalues):
    absolute = int(pct / 100.*np.sum(allvalues))
    return "{:.1f}%\n".format(pct)

fig, ax = plt.subplots(figsize=(10, 7))

wedges, texts, autotexts = ax.pie(data,
                                  autopct = lambda pct: func(pct, data),
                                  labels = mylabels)

ax.set_title("proportion of cell types")
plt.show()
