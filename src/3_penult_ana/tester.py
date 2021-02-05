from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
import random 
import sys
import os, subprocess
from pdf2image import convert_from_path
import math
from icecream import ic
import shutil
from PIL import Image, ImageDraw, ImageFont

#This project
from utils import data_getter
from picture_tools import prelimplot


prelimplot.stitch_pics("pics/",save_dir="./")