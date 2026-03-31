import csv
import numpy as np
from matplotlib import pyplot as plt, cm

from BAD_UncertaintyPropogation.Distributions import FitDistribution, KDE
from BAD_UncertaintyPropogation.Kernals import Epanechnikov, Normal

file_path = "AAB_PrerequisiteData/example_trajectory_data.csv"
with open(file_path, "r") as f:
    csv_reader = csv.reader(f)
    csv_data = [row for row in csv_reader]

    mach_vals = []
    alt_vals = []
    for row in csv_data[1::]:
        mach_vals.append(float(row[3]))
        alt_vals.append(float(row[1]))
kernel = Epanechnikov()
dist_mach = FitDistribution(kernel, mach_vals)

X = np.linspace(0, 8, 1000)
Y = []

Y = dist_mach.pdf(X)

plt.hist(mach_vals, bins = 50, density = True, color ="navajowhite")
plt.plot(X, Y, color = "orange")
plt.xlabel("Mach Number")
plt.ylabel("Probability")
plt.show()


dist_alt = FitDistribution(kernel, alt_vals)
X = np.linspace(0, 30000, 1000)
Y = []

Y = dist_alt.pdf(X)

plt.hist(alt_vals, bins = 50, density = True, color ="navajowhite")
plt.plot(X, Y, color = "orange")
plt.xlabel("Altitude [ft]")
plt.ylabel("Probability")
plt.show()

with open(file_path, "r") as f:
    csv_reader = csv.reader(f)
    csv_data = [row for row in csv_reader]

data = np.array(csv_data[1::])
data = data[:, [1, 3]].astype(float) # Just keep altitude (1) and Mach Number (2)

segs = 50
alt = np.linspace(0, 30000, segs)
mach = np.linspace(3, 8, segs)
p_alt = dist_alt.pdf(alt)
p_mach = dist_mach.pdf(mach)
X, Y = np.meshgrid(alt, mach)
plt.contourf(X, Y, p_alt * p_mach.reshape([-1, 1]), levels=20, cmap="OrRd")
plt.colorbar()
plt.scatter(data[:,0], data[:,1], marker='x', s=10, c="navy")
plt.xlabel("Altitude (ft)")
plt.ylabel("Mach Number")
plt.show()


# kernel = Normal(2)
dist = KDE(kernel, data)
segs = 50
x = np.linspace(0, 30000, segs)
y = np.linspace(3, 8, segs)
alt, mach = np.meshgrid(x, y)

points = np.concatenate((alt.reshape(-1, 1), mach.reshape(-1, 1)), axis = 1)

prob = dist.pdf(points)
plt.contourf(alt, mach, prob.reshape([segs, segs]), levels=20, cmap="YlGn")
plt.colorbar()
plt.scatter(data[:,0], data[:,1], marker='x', s=10, c="navy")
plt.xlabel("Altitude (ft)")
plt.ylabel("Mach Number")
plt.show()