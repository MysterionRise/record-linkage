import numpy as np
from matplotlib import pyplot as plt

seeds = np.genfromtxt("seeds.tsv", delimiter="\t", usecols=(0, 1, 2, 3, 4, 5, 6))
seeds_labels = np.genfromtxt("seeds.tsv", delimiter="\t", usecols=(-1), dtype=str)

# z-score normalisation
seeds -= seeds.mean(axis=0)
seeds /= seeds.std(axis=0)

area = seeds[:, 0]
compact = seeds[:, 2]
asymmetry = seeds[:, 5]

for t, marker, c in zip(("Kama", "Rosa", "Canadian"), ">ox", "rgb"):
    plt.scatter(area[seeds_labels == t], compact[seeds_labels == t], marker=marker, c=c)

plt.savefig("seeds_area_compact.png")

plt.clf()

for t, marker, c in zip(("Kama", "Rosa", "Canadian"), ">ox", "rgb"):
    plt.scatter(area[seeds_labels == t], asymmetry[seeds_labels == t], marker=marker, c=c)

plt.savefig("seeds_area_asymmetry.png")

plt.clf()

for t, marker, c in zip(("Kama", "Rosa", "Canadian"), ">ox", "rgb"):
    plt.scatter(compact[seeds_labels == t], asymmetry[seeds_labels == t], marker=marker, c=c)

plt.savefig("seeds_compact_asymmetry.png")
