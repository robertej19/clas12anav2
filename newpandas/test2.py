import uproot
from icecream import ic
import numpy as np
import pandas as pd
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import subprocess
import os
import time
import shutil
from shutil import copyfile

data_path = "./outfile.pkl"

df = pd.read_pickle(data_path)

print(df.head(3))
print(df.shape)