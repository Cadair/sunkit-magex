"""
Tracer performance
==================
A quick script to compare the performance of the python and fortran tracers.
"""
import timeit
import numpy as np
import pfsspy
import matplotlib.pyplot as plt

###############################################################################
# Create a dipole map
ntheta = 180
nphi = 360
nr = 50
rss = 2.5

phi = np.linspace(0, 2 * np.pi, nphi)
theta = np.linspace(-np.pi / 2, np.pi / 2, ntheta)
theta, phi = np.meshgrid(theta, phi)


def dipole_Br(r, theta):
    return 2 * np.sin(theta) / r**3


br = dipole_Br(1, theta).T
pfss_input = pfsspy.Input(br, nr, rss)
pfss_output = pfsspy.pfss(pfss_input)
print('Computed PFSS solution')

###############################################################################
# Trace some field lines
seed0 = np.atleast_2d(np.array([1, 1, 0]))
tracers = [pfsspy.tracing.PythonTracer(),
           pfsspy.tracing.FortranTracer()]
nseeds = 2**np.arange(6)
times = [[], []]

for nseed in nseeds:
    print(nseed)
    seeds = np.repeat(seed0, nseed, axis=0)
    for i, tracer in enumerate(tracers):
        if nseed > 100 and i == 0:
            continue
        # tracer.trace(seeds, pfss_output)
        t = timeit.timeit(lambda: tracer.trace(seeds, pfss_output), number=2)
        times[i].append(t)

###############################################################################
# Plot the results
fig, ax = plt.subplots()
ax.scatter(nseeds[1:len(times[0])], times[0][1:], label='python')
ax.scatter(nseeds[1:], times[1][1:], label='fortran')


ax.set_xscale('log')
ax.set_yscale('log')

ax.set_xlabel('Number of seeds')
ax.set_ylabel('Seconds')

ax.axvline(180 * 360, color='k', linestyle='--', label='180x360 seed points')

ax.legend()
plt.show()
