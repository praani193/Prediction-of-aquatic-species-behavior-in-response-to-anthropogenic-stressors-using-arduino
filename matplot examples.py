import matplotlib.pyplot as plt
import numpy as np
td=[25,23,47]
tid=[1,2,3]
sd=[23,44.5,54.2]

plt.subplot(1, 2, 1)
plt.plot(td,tid)

#plot 2:
x1 = np.array(sd)
y2 = np.array(tid)

plt.subplot(1, 2, 2)
plt.plot(x1,y2)

plt.show()
