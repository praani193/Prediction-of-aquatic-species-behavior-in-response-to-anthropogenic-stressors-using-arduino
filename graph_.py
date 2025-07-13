import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from ts1 import td
from ts1 import tid
from ts1 import sd
print(td)
print(tid)
print(sd)
plt.figure(1)
plt.subplot(1, 2, 1)
plt.plot(tid,td)
plt.xlabel="Time"
plt.ylabel="Temperature"
# Plot 2:
plt.subplot(1, 2, 2)
plt.plot(sd,td)

plt.show()
