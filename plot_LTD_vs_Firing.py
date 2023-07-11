from bmtk.utils.reports.compartment import CompartmentReport
import numpy as np
from tqdm import tqdm
import h5py
import pandas as pd
import matplotlib.pyplot as plt

def get_data(path):
    report = CompartmentReport(path)
    cells = report.node_ids()
    nodes = []
    zero_count = []
    for i in tqdm(range(len(report.node_ids()))):
        data = report.data(node_id=i)
        



