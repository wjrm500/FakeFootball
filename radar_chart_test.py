import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
labels=np.array(['Offence', 'Defence', 'Control', 'Spark'])
stats=[1.5, 0.75, 0.9, 1.2]
angles=np.linspace(0, 2*np.pi, len(labels), endpoint=False)
stats=np.concatenate((stats,[stats[0]]))
angles=np.concatenate((angles,[angles[0]]))
fig=plt.figure()
ax = fig.add_subplot(111, polar=True)
ax.plot(angles, stats, 'o-', linewidth=2)
ax.fill(angles, stats, alpha=0.25)
ax.set_thetagrids(angles * 180/np.pi, labels)
ax.set_title('Hello')
ax.grid(True)
plt.show()