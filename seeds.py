import numpy as np
from matplotlib import pyplot as plt

seeds = np.genfromtxt("seeds.tsv", delimiter = "\t", usecols = (0,1,2,3,4,5,6))
seeds_labels = np.genfromtxt("seeds.tsv", delimiter = "\t", usecols = (-1))

for t,marker,c in zip(("Kama", "Rosa", "Canadian"), ">ox", "rgb"):
    plt.scatter(area[seeds_labels == t], compact[seeds_labels == t], marker = marker, c = c)
