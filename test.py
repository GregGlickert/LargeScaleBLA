import h5py
import matplotlib.pyplot as plt
import numpy as np


first_col_5 = np.loadtxt("voltage_reports/voltage_report_gid_5.txt")[:, 0]
second_col_5 = np.loadtxt("voltage_reports/voltage_report_gid_5.txt")[:, 1]

first_col_0 = np.loadtxt("voltage_reports/voltage_report_gid_0.txt")[:, 0]
second_col_0 = np.loadtxt("voltage_reports/voltage_report_gid_0.txt")[:, 1]

first_col_1 = np.loadtxt("voltage_reports/voltage_report_gid_1.txt")[:, 0]
second_col_1 = np.loadtxt("voltage_reports/voltage_report_gid_1.txt")[:, 1]

first_col_2 = np.loadtxt("voltage_reports/voltage_report_gid_2.txt")[:, 0]
second_col_2 = np.loadtxt("voltage_reports/voltage_report_gid_2.txt")[:, 1]

first_col_3 = np.loadtxt("voltage_reports/voltage_report_gid_3.txt")[:, 0]
second_col_3 = np.loadtxt("voltage_reports/voltage_report_gid_3.txt")[:, 1]

first_col_4 = np.loadtxt("voltage_reports/voltage_report_gid_4.txt")[:, 0]
second_col_4 = np.loadtxt("voltage_reports/voltage_report_gid_4.txt")[:, 1]

fig, axs = plt.subplots(3,2)

axs[0, 0].plot(first_col_5, second_col_5)
axs[0, 1].plot(first_col_2, second_col_2)
axs[1, 0].plot(first_col_0, second_col_0)
axs[1, 1].plot(first_col_1, second_col_1)
axs[2, 1].plot(first_col_3, second_col_3)
axs[2, 0].plot(first_col_4, second_col_4)
plt.show()