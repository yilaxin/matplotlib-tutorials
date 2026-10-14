"""对比 plt.tick_params(axis='both', labelsize=14) 的效果。

左图用 matplotlib 的默认刻度字号，右图把两个坐标轴的刻度字号改成 14。
"""

import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
y = np.sin(x)

fig, axes = plt.subplots(1, 2, figsize=(9, 3.6), sharey=True)

# 左图：默认设置，刻度标签用的是 rcParams 里的默认字号（10）
axes[0].plot(x, y)
axes[0].set_title("default tick label size")

# 右图：只改刻度标签字号，其余保持默认
axes[1].plot(x, y)
axes[1].set_title("labelsize=14")
axes[1].tick_params(axis="both", labelsize=14)

fig.tight_layout()
fig.savefig("tick_params_demo.png", dpi=130)
