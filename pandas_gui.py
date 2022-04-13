import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandasgui import show

df = pd.read_csv('connection table.csv')
gui = show(df)


