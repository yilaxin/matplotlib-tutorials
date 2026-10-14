"""Generate the next five standalone Matplotlib practice notebooks."""

from __future__ import annotations

import ast
import json
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent / "notebooks"


def src(text: str) -> list[str]:
    return textwrap.dedent(text).strip("\n").splitlines(keepends=True)


def md(text: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": src(text)}


def py(text: str, answer: bool = False) -> dict:
    return {"cell_type": "code", "execution_count": None,
            "metadata": {"tags": ["参考答案"]} if answer else {},
            "outputs": [], "source": src(text)}


def lesson(n: int, slug: str, title: str, source_url: str, goals: str,
           concepts: str, setup: str, examples: list[tuple[str, str, str]],
           exercises: list[tuple[str, str, str, str]], challenge: str,
           summary: str, official_url: str | None = None) -> Path:
    refs = f"[菜鸟教程]({source_url})"
    if official_url:
        refs += f"；[Matplotlib 官方 API]({official_url})"
    cells = [
        md(f"# 第 {n} 课：{title}｜练习\n\n**资料：**{refs}。示例与练习代码为重新设计。\n\n"
           f"## 学习目标\n\n{goals}\n\n先动手完成题目，再对照参考答案。"),
        md(f"## 核心知识\n\n{concepts}"),
        py(setup),
    ]
    assert len(examples) == 2 and len(exercises) == 2
    for name, explanation, code in examples:
        cells.extend([md(f"## 示例：{name}\n\n{explanation}"), py(code)])
    for i, (prompt, starter, hint, answer) in enumerate(exercises, 1):
        cells.extend([
            md(f"## 动手练习 {i}\n\n{prompt}"),
            py(starter),
            md(f"<details><summary>提示</summary>\n\n{hint}\n\n</details>"),
            md("### 参考答案\n\n完成练习后再运行下一单元。"),
            py(answer, answer=True),
        ])
    cells.extend([md(f"## 提高练习\n\n{challenge}"),
                  md(f"## 本课小结\n\n{summary}\n\n资料：{refs}。")])
    assert len(cells) == 19
    for i, cell in enumerate(cells):
        cell["id"] = f"matplotlib-{n}-{i:02d}"
    notebook = {"cells": cells,
                "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                             "language_info": {"name": "python"}},
                "nbformat": 4, "nbformat_minor": 5}
    path = ROOT / f"Matplotlib_{n:02d}_{slug}_练习.ipynb"
    path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return path


created = []


created.append(lesson(
    26, "figure", "Figure 画布与尺寸", "https://www.runoob.com/matplotlib/matplotlib-ref-figure.html",
    "- 区分 Figure 画布、Axes 坐标图和图中元素。\n"
    "- 用 `figsize`、`dpi` 控制画布与导出尺寸。\n"
    "- 在同一画布中放置多个 Axes。",
    "Figure 是整张图，Axes 是其中的一块绘图区。`plt.figure(figsize=(w,h), dpi=...)` 的尺寸单位是英寸。"
    "通过 `fig, ax = plt.subplots()` 也能同时创建 Figure 与 Axes。位图像素大小约为英寸尺寸乘以导出 dpi；"
    "每次绘图最好显式持有 Figure 对象。",
    """
    from pathlib import Path
    import numpy as np
    import matplotlib.pyplot as plt
    OUTPUT = Path.cwd() / "matplotlib_练习输出"
    OUTPUT.mkdir(exist_ok=True)
    x = np.linspace(0, 2 * np.pi, 150)
    """,
    [
        ("观察画布尺寸", "下面创建 6×3 英寸画布，并查看对象自身记录的尺寸。",
         """
         fig, ax = plt.subplots(figsize=(6, 3), dpi=100)
         ax.plot(x, np.sin(x))
         ax.set_title("6 × 3 inch figure")
         print("Figure inches:", fig.get_size_inches(), "dpi:", fig.dpi)
         plt.show()
         """),
        ("同一 Figure 的两张图", "Axes 是 Figure 的子图，可分别控制标题与坐标范围。",
         """
         fig, axes = plt.subplots(1, 2, figsize=(9, 3), constrained_layout=True)
         axes[0].plot(x, np.sin(x)); axes[0].set_title("sin")
         axes[1].plot(x, np.cos(x), color="tomato"); axes[1].set_title("cos")
         fig.suptitle("One Figure, two Axes")
         plt.show()
         """),
    ],
    [
        ("画一张 8×4 英寸的折线图，导出为 160 dpi PNG；打印文件路径。",
         """
         output_path = OUTPUT / "26_large_figure.png"
         # TODO: 创建 8×4 英寸 Figure，绘制曲线，保存为 160 dpi
         """,
         "调用 `plt.subplots(figsize=(8,4))`，随后使用 `fig.savefig(output_path, dpi=160)`。",
         """
         output_path = OUTPUT / "26_large_figure.png"
         fig, ax = plt.subplots(figsize=(8, 4))
         ax.plot(x, np.sin(x), label="sin(x)")
         ax.set(xlabel="x", ylabel="value", title="Sine wave")
         ax.legend()
         fig.savefig(output_path, dpi=160, bbox_inches="tight")
         assert output_path.is_file()
         print(output_path)
         plt.show()
         """),
        ("创建上下排列的两个 Axes，共享 x 轴，并给 Figure 设置总标题。",
         """
         # TODO: plt.subplots(2, 1, sharex=True)，分别画正弦、余弦
         """,
         "`fig.suptitle(...)` 设置整个画布的标题。",
         """
         fig, axes = plt.subplots(2, 1, figsize=(7, 5), sharex=True,
                                  constrained_layout=True)
         axes[0].plot(x, np.sin(x)); axes[0].set_ylabel("sin")
         axes[1].plot(x, np.cos(x)); axes[1].set_ylabel("cos")
         axes[1].set_xlabel("x")
         fig.suptitle("Trigonometric functions")
         plt.show()
         """),
    ],
    "同一 Figure 分别导出 100 dpi 和 200 dpi PNG，比较文件尺寸与清晰度。",
    "Figure 管整体尺寸和导出，Axes 管具体绘图。先决定画布用途，再选择尺寸和 dpi。",
    "https://matplotlib.org/stable/api/figure_api.html",
))


created.append(lesson(
    27, "figure_axes管理", "Figure 与 Axes 管理",
    "https://www.runoob.com/matplotlib/matplotlib-ref-figure-management.html",
    "- 创建并明确操作不同的 Axes。\n"
    "- 分辨 `ax.clear()`、`fig.clear()`、`plt.close(fig)`。\n"
    "- 初步使用 `twinx()` 绘制量纲不同的两组数据。",
    "`ax.clear()` 清空单个坐标图；`fig.clear()` 清空整个画布；`plt.close(fig)` 关闭画布并释放资源。"
    "`ax.twinx()` 创建共用 x 轴但拥有另一根 y 轴的 Axes，适合量纲不同且时间轴相同的两个序列。"
    "双轴图应明确标注单位，避免让两条线看起来可以直接比较高度。",
    """
    import numpy as np
    import matplotlib.pyplot as plt
    x = np.arange(1, 7)
    sales = np.array([12, 15, 17, 16, 20, 23])
    rate = np.array([0.12, 0.15, 0.14, 0.18, 0.21, 0.19])
    """,
    [
        ("清空 Axes 后重新绘图", "同一 Figure 中只清空右图，左图继续保留。",
         """
         fig, axes = plt.subplots(1, 2, figsize=(8, 3))
         axes[0].plot(x, sales); axes[0].set_title("Retained")
         axes[1].bar(x, sales)
         axes[1].clear()
         axes[1].plot(x, rate, color="tomato"); axes[1].set_title("Replaced")
         plt.show()
         """),
        ("共用 x 轴的双 y 轴", "销售量与转化率使用不同单位，各自的 y 轴必须清楚标记。",
         """
         fig, left = plt.subplots(figsize=(7, 4))
         right = left.twinx()
         left.bar(x, sales, color="steelblue", alpha=0.5)
         right.plot(x, 100 * rate, color="tomato", marker="o")
         left.set(xlabel="month", ylabel="sales", title="Sales and conversion")
         right.set_ylabel("conversion (%)")
         plt.show()
         """),
    ],
    [
        ("创建两张子图；只清空第一张后改画散点图。观察第二张是否保持原样。",
         """
         # TODO: axes[0].clear()，再 axes[0].scatter(...)
         """,
         "先在两个 Axes 上绘图，再只对 `axes[0]` 调用 `clear()`。",
         """
         fig, axes = plt.subplots(1, 2, figsize=(8, 3))
         axes[0].plot(x, sales)
         axes[1].bar(x, sales)
         axes[0].clear()
         axes[0].scatter(x, sales, color="purple")
         axes[0].set_title("Scatter after clear")
         axes[1].set_title("Bar unchanged")
         plt.show()
         """),
        ("创建一个双轴图：左轴画 `sales` 折线，右轴画 `100*rate` 折线，明确标注两侧单位。",
         """
         # TODO: ax.twinx() 并在两侧设置 y 轴标签
         """,
         "注意左右轴可使用与各自曲线一致的颜色。",
         """
         fig, ax_left = plt.subplots()
         ax_right = ax_left.twinx()
         ax_left.plot(x, sales, color="navy", marker="o")
         ax_right.plot(x, 100 * rate, color="orange", marker="s")
         ax_left.set(xlabel="month", ylabel="sales (units)")
         ax_right.set_ylabel("conversion (%)")
         ax_left.set_title("Two y axes")
         plt.show()
         """),
    ],
    "批量生成 5 张图，在循环中使用 `plt.close(fig)`；检查图的数量是否持续增加。",
    "明确持有 fig/ax 对象可减少误操作。清空与关闭用途不同；双轴图必须突出各自单位。",
    "https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.twinx.html",
))


created.append(lesson(
    28, "频谱分析", "频谱与时频图",
    "https://www.runoob.com/matplotlib/matplotlib-ref-spectral.html",
    "- 从时域信号识别不同频率成分。\n"
    "- 使用 `psd()` 绘制功率谱密度。\n"
    "- 使用 `specgram()` 查看频率随时间的变化。",
    "对按 `Fs` 次/秒采样的一维信号，`psd()` 在频域显示各频率的功率，"
    "`specgram()` 在横轴显示时间、纵轴显示频率。`NFFT` 决定分析窗口长度，"
    "`noverlap` 决定相邻窗口重叠程度。要观察时频变化，信号长度必须覆盖多个窗口。",
    """
    import numpy as np
    import matplotlib.pyplot as plt
    Fs = 100
    t = np.arange(0, 4, 1 / Fs)
    rng = np.random.default_rng(28)
    signal = np.sin(2 * np.pi * 8 * t) + 0.55 * np.sin(2 * np.pi * 20 * t)
    signal += 0.12 * rng.normal(size=len(t))
    """,
    [
        ("时域与功率谱", "信号含 8 Hz 与 20 Hz 的成分；观察功率谱的两个峰。",
         """
         fig, axes = plt.subplots(1, 2, figsize=(10, 3))
         axes[0].plot(t[:100], signal[:100]); axes[0].set(xlabel="time (s)", title="Waveform")
         axes[1].psd(signal, NFFT=256, Fs=Fs); axes[1].set_title("Power spectrum")
         fig.tight_layout()
         plt.show()
         """),
        ("频率随时间变化", "前半段为 8 Hz，后半段为 20 Hz；频谱图应显示两个不同时间段。",
         """
         switched = np.where(t < 2, np.sin(2 * np.pi * 8 * t),
                             np.sin(2 * np.pi * 20 * t))
         fig, ax = plt.subplots(figsize=(7, 4))
         spectrum, freqs, bins, image = ax.specgram(switched, NFFT=128,
                                                     Fs=Fs, noverlap=96, cmap="viridis")
         fig.colorbar(image, ax=ax, label="power (dB)")
         ax.set(xlabel="time (s)", ylabel="frequency (Hz)", title="Spectrogram")
         plt.show()
         """),
    ],
    [
        ("把原信号的第二个频率从 20 Hz 改为 30 Hz，重新绘制功率谱；判断峰的位置是否变化。",
         """
         new_signal = np.sin(2 * np.pi * 8 * t) + 0.55 * np.sin(2 * np.pi * 30 * t)
         # TODO: 使用 ax.psd(new_signal, NFFT=256, Fs=Fs)
         """,
         "改变公式中的 20 为 30，再保持采样率不变。",
         """
         new_signal = np.sin(2 * np.pi * 8 * t) + 0.55 * np.sin(2 * np.pi * 30 * t)
         fig, ax = plt.subplots()
         ax.psd(new_signal, NFFT=256, Fs=Fs)
         ax.set_title("8 Hz and 30 Hz components")
         plt.show()
         """),
        ("制作从 5 Hz 切换到 15 Hz 的信号，切换时间为 2 秒；用 `specgram()` 显示。",
         """
         # TODO: np.where(t < 2, 第一个波形, 第二个波形)，再作时频图
         """,
         "两个分支分别是 `np.sin(2*np.pi*5*t)` 和 `np.sin(2*np.pi*15*t)`。",
         """
         changed = np.where(t < 2, np.sin(2 * np.pi * 5 * t),
                            np.sin(2 * np.pi * 15 * t))
         fig, ax = plt.subplots(figsize=(7, 4))
         _, _, _, im = ax.specgram(changed, NFFT=128, Fs=Fs, noverlap=96)
         fig.colorbar(im, ax=ax, label="power (dB)")
         ax.set(xlabel="time (s)", ylabel="frequency (Hz)", title="5 → 15 Hz")
         plt.show()
         """),
    ],
    "把 `NFFT` 分别改为 64、128、256，比较频率分辨率与时间定位之间的变化。",
    "`Fs` 必须是实际采样率；时间波形、功率谱和时频图回答的问题不同。",
    "https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.specgram.html",
))


created.append(lesson(
    29, "二维统计图", "二维直方图与六边形分箱",
    "https://www.runoob.com/matplotlib/matplotlib-ref-2d-plots.html",
    "- 用 `hist2d()` 汇总大量二维样本。\n"
    "- 用 `hexbin()` 比较六边形分箱效果。\n"
    "- 为颜色映射添加表示计数的颜色条。",
    "普通散点图在点很多时容易重叠。`hist2d(x,y,bins=...)` 将平面分成矩形网格，"
    "`hexbin(x,y,gridsize=...)` 将平面分成六边形网格；默认颜色表示每格的样本数量。"
    "调节 bins/gridsize 会改变局部细节，不能随意把颜色解释为概率密度。",
    """
    import numpy as np
    import matplotlib.pyplot as plt
    rng = np.random.default_rng(29)
    x = rng.normal(size=3500)
    y = 0.65 * x + rng.normal(scale=0.6, size=3500)
    """,
    [
        ("矩形网格的计数", "色标数值是每个矩形格子中的样本数。",
         """
         fig, ax = plt.subplots(figsize=(6, 4))
         counts, xedges, yedges, image = ax.hist2d(x, y, bins=30, cmap="Blues")
         fig.colorbar(image, ax=ax, label="count")
         ax.set(xlabel="x", ylabel="y", title="2D histogram")
         print("网格形状：", counts.shape)
         plt.show()
         """),
        ("六边形网格的计数", "在相同样本上比较六边形分箱的视觉效果。",
         """
         fig, ax = plt.subplots(figsize=(6, 4))
         bins = ax.hexbin(x, y, gridsize=30, cmap="YlOrRd")
         fig.colorbar(bins, ax=ax, label="count")
         ax.set(xlabel="x", ylabel="y", title="Hexbin")
         plt.show()
         """),
    ],
    [
        ("创建并排的二维直方图与散点图，比较 3500 个点在两种图中的可读性。",
         """
         # TODO: 两个 Axes；一侧 hist2d，另一侧 scatter(alpha=0.15, s=4)
         """,
         "小点和透明度有助于缓解散点图的遮挡。",
         """
         fig, axes = plt.subplots(1, 2, figsize=(10, 4), constrained_layout=True)
         _, _, _, im = axes[0].hist2d(x, y, bins=30, cmap="Blues")
         fig.colorbar(im, ax=axes[0], label="count")
         axes[0].set_title("Binned")
         axes[1].scatter(x, y, s=4, alpha=0.15)
         axes[1].set_title("Raw samples")
         plt.show()
         """),
        ("让 x、y 互不相关，各从标准正态分布抽样 3000 点，画六边形分箱图。",
         """
         independent_x = rng.normal(size=3000)
         independent_y = rng.normal(size=3000)
         # TODO: hexbin + colorbar
         """,
         "与本课的相关数据对比，独立样本的高密度区域通常更接近圆形。",
         """
         independent_x = rng.normal(size=3000)
         independent_y = rng.normal(size=3000)
         fig, ax = plt.subplots()
         hb = ax.hexbin(independent_x, independent_y, gridsize=25, cmap="viridis")
         fig.colorbar(hb, ax=ax, label="count")
         ax.set(xlabel="x", ylabel="y", title="Independent variables")
         plt.show()
         """),
    ],
    "把 bins 或 gridsize 改为 10、30、60，观察局部模式与噪声如何变化。",
    "当数据点大量重叠时，分箱图通常比纯散点更容易读出高密度区域。颜色条应注明表示计数还是密度。",
    "https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.hist2d.html",
))


created.append(lesson(
    30, "三角网格和极坐标", "三角网格与极坐标",
    "https://www.runoob.com/matplotlib/matplotlib-apiref.html",
    "- 在不规则点集上绘制三角网格和标量场。\n"
    "- 使用极坐标表达角度与半径。\n"
    "- 判断何时选择三角网格或极坐标。",
    "结构化矩形网格适合 `imshow()`；不规则散点可用 `triplot()` 和 `tricontourf()`。"
    "极坐标由角度 θ 和半径 r 决定，在创建 Axes 时设置 `projection='polar'`。"
    "两个绘图系统表达的是不同数据结构，本课分别练习。",
    """
    import numpy as np
    import matplotlib.pyplot as plt
    rng = np.random.default_rng(30)
    px = rng.uniform(-2, 2, 80)
    py = rng.uniform(-2, 2, 80)
    pz = np.exp(-(px**2 + py**2))
    """,
    [
        ("不规则点的三角网格", "点的位置不在规则矩阵上，三角形由 Matplotlib 自动连接。",
         """
         fig, ax = plt.subplots(figsize=(5, 5))
         ax.triplot(px, py, color="gray", linewidth=0.7)
         ax.scatter(px, py, s=9, color="tomato")
         ax.set(xlabel="x", ylabel="y", title="Triangular mesh")
         ax.set_aspect("equal")
         plt.show()
         """),
        ("极坐标曲线", "角度增长时半径也缓慢增长，形成螺旋线。",
         """
         theta = np.linspace(0, 4 * np.pi, 250)
         radius = 0.25 + theta / (4 * np.pi)
         fig, ax = plt.subplots(subplot_kw={"projection": "polar"}, figsize=(5, 5))
         ax.plot(theta, radius, color="purple")
         ax.set_title("Spiral in polar coordinates")
         plt.show()
         """),
    ],
    [
        ("使用 `tricontourf()` 给不规则点上的 `pz` 值填色，并添加颜色条。",
         """
         # TODO: ax.tricontourf(px, py, pz, levels=12) + fig.colorbar
         """,
         "`tricontourf()` 不需要先构造矩形 `meshgrid`。",
         """
         fig, ax = plt.subplots(figsize=(5, 5))
         mesh = ax.tricontourf(px, py, pz, levels=12, cmap="viridis")
         fig.colorbar(mesh, ax=ax, label="height")
         ax.set(xlabel="x", ylabel="y", title="Irregular scalar field")
         ax.set_aspect("equal")
         plt.show()
         """),
        ("以八个方向的角度为 θ、`[3,4,5,3,2,4,6,5]` 为半径，绘制闭合的极坐标折线。",
         """
         directions = np.linspace(0, 2 * np.pi, 8, endpoint=False)
         radius = np.array([3, 4, 5, 3, 2, 4, 6, 5])
         # TODO: 首尾连接后，用 polar Axes 画图
         """,
         "用 `np.r_[directions, directions[0]]` 和 `np.r_[radius, radius[0]]` 闭合。",
         """
         directions = np.linspace(0, 2 * np.pi, 8, endpoint=False)
         radius = np.array([3, 4, 5, 3, 2, 4, 6, 5])
         closed_theta = np.r_[directions, directions[0]]
         closed_radius = np.r_[radius, radius[0]]
         fig, ax = plt.subplots(subplot_kw={"projection": "polar"})
         ax.plot(closed_theta, closed_radius, marker="o")
         ax.set_title("Eight directions")
         plt.show()
         """),
    ],
    "给三角网格叠加原始采样点，比较增加或减少点数对三角形密度的影响。",
    "三角网格处理不规则二维采样，极坐标处理角度与半径。要先辨别数据结构，再选择绘图坐标系。",
    "https://matplotlib.org/stable/api/tri_api.html",
))


assert len(created) == 5
for path in created:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    assert (notebook["nbformat"], notebook["nbformat_minor"]) == (4, 5)
    assert len(notebook["cells"]) == 19
    assert len({cell["id"] for cell in notebook["cells"]}) == 19
    code_cells = [cell for cell in notebook["cells"] if cell["cell_type"] == "code"]
    assert len(code_cells) == 7
    for cell in code_cells:
        ast.parse("".join(cell["source"]), filename=path.name)
        assert cell["execution_count"] is None and cell["outputs"] == []
    print(f"PASS {path.name}: 19 cells, 7 code")

try:
    import nbformat
except ImportError:
    print("nbformat unavailable; JSON and Python syntax validated")
else:
    for path in created:
        nbformat.validate(nbformat.read(path, as_version=4))
    print("nbformat schema passed")
