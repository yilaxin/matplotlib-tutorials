"""Build and validate five self-contained Matplotlib practice notebooks."""

from __future__ import annotations

import ast
import json
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent / "notebooks"


def source(value: str) -> list[str]:
    return textwrap.dedent(value).strip("\n").splitlines(keepends=True)


def markdown(value: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": source(value)}


def python(value: str, answer: bool = False) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {"tags": ["参考答案"]} if answer else {},
        "outputs": [],
        "source": source(value),
    }


def exercise(prompt: str, starter: str, hint: str, solution: str) -> tuple[str, str, str, str]:
    return prompt, starter, hint, solution


def build(
    number: int,
    slug: str,
    title: str,
    url: str,
    goals: str,
    concepts: str,
    setup: str,
    examples: list[tuple[str, str, str]],
    exercises: list[tuple[str, str, str, str]],
    challenge: str,
    summary: str,
    extra_url: str | None = None,
) -> Path:
    origin = f"[菜鸟教程参考文档]({url})"
    if extra_url:
        origin += f"；API 参数参考 [Matplotlib 官方文档]({extra_url})"
    cells = [
        markdown(
            f"# 第 {number} 课：{title}｜练习\n\n"
            f"**学习资料：**{origin}。本练习的代码和数据均为重新设计。\n\n"
            f"## 学习目标\n\n{goals}\n\n"
            "按顺序运行代码单元。先完成每道动手题，再查看参考答案。"
        ),
        markdown(f"## 核心知识\n\n{concepts}"),
        python(setup),
    ]
    assert len(examples) == 2 and len(exercises) == 2
    for name, explanation, snippet in examples:
        cells.extend([markdown(f"## 示例：{name}\n\n{explanation}"), python(snippet)])
    for i, (prompt, starter, hint, solution) in enumerate(exercises, 1):
        cells.extend(
            [
                markdown(f"## 动手练习 {i}\n\n{prompt}"),
                python(starter),
                markdown(f"<details><summary>提示</summary>\n\n{hint}\n\n</details>"),
                markdown("### 参考答案\n\n完成题目后再运行下面的代码。"),
                python(solution, answer=True),
            ]
        )
    cells.extend(
        [
            markdown(f"## 提高练习\n\n{challenge}"),
            markdown(f"## 本课小结\n\n{summary}\n\n资料：{origin}。"),
        ]
    )
    assert len(cells) == 19
    for i, cell in enumerate(cells):
        cell["id"] = f"matplotlib-{number}-{i:02d}"
    document = {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    path = ROOT / f"Matplotlib_{number:02d}_{slug}_练习.ipynb"
    path.write_text(json.dumps(document, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return path


created: list[Path] = []


created.append(build(
    21,
    "contour",
    "等高线与填充等高线",
    "https://www.runoob.com/matplotlib/matplotlib-ref-contour.html",
    "- 把二维标量场转换成等值线图。\n"
    "- 用 `contour()`、`contourf()` 和 `clabel()` 展示层级与数值。\n"
    "- 理解 `X`、`Y`、`Z` 的形状关系。",
    "`np.meshgrid(x, y)` 生成二维坐标矩阵。`Z` 必须和它们具有相同的二维形状。"
    "`contour()` 画等值线，`contourf()` 填满层级之间的区域；`levels` 指定层级的个数或具体数值。"
    "`clabel()` 为等高线标注数值，`fig.colorbar()` 解释填充颜色。",
    """
    import numpy as np
    import matplotlib.pyplot as plt
    x = np.linspace(-3, 3, 120)
    y = np.linspace(-3, 3, 100)
    X, Y = np.meshgrid(x, y)
    Z = np.exp(-((X - 1)**2 + Y**2)) + 0.7 * np.exp(-((X + 1)**2 + (Y - 1)**2) / 1.5)
    print("X/Y/Z 形状：", X.shape, Y.shape, Z.shape)
    """,
    [
        (
            "只用线表达高度",
            "选择固定的等值层级，并在曲线上显示数值。",
            """
            levels = np.linspace(0.1, 1.1, 6)
            fig, ax = plt.subplots(figsize=(6, 5))
            lines = ax.contour(X, Y, Z, levels=levels, colors="navy")
            ax.clabel(lines, inline=True, fontsize=8)
            ax.set(xlabel="x", ylabel="y", title="Contour lines")
            ax.set_aspect("equal")
            plt.show()
            """,
        ),
        (
            "填充等高线与色标",
            "用颜色表示连续变化，同时用较淡的线标出层级边界。",
            """
            fig, ax = plt.subplots(figsize=(6, 5))
            filled = ax.contourf(X, Y, Z, levels=15, cmap="viridis")
            ax.contour(X, Y, Z, levels=15, colors="black", linewidths=0.3, alpha=0.5)
            fig.colorbar(filled, ax=ax, label="height")
            ax.set(xlabel="x", ylabel="y", title="Filled contours")
            ax.set_aspect("equal")
            plt.show()
            """,
        ),
    ],
    [
        exercise(
            "对 `Z` 绘制 0.2、0.4、0.6、0.8、1.0 五条等值线，在每条线上显示数值。",
            """
            chosen_levels = [0.2, 0.4, 0.6, 0.8, 1.0]
            # TODO: 使用 ax.contour 与 ax.clabel
            """,
            "`ax.contour(...)` 的返回对象可以传给 `ax.clabel(...)`。",
            """
            chosen_levels = [0.2, 0.4, 0.6, 0.8, 1.0]
            fig, ax = plt.subplots(figsize=(6, 5))
            contour_set = ax.contour(X, Y, Z, levels=chosen_levels, cmap="plasma")
            ax.clabel(contour_set, inline=True, fmt="%.1f")
            ax.set_aspect("equal")
            ax.set_title("Specified levels")
            plt.show()
            """,
        ),
        exercise(
            "生成 `W = sin(X) * cos(Y)`，用 `coolwarm` 颜色映射绘制填充等高线，并加颜色条。",
            """
            W = np.sin(X) * np.cos(Y)
            # TODO: contourf + fig.colorbar
            """,
            "`W` 的范围大致在 -1 到 1；可以设置 `levels=np.linspace(-1, 1, 13)`。",
            """
            W = np.sin(X) * np.cos(Y)
            fig, ax = plt.subplots(figsize=(6, 5))
            fill = ax.contourf(X, Y, W, levels=np.linspace(-1, 1, 13), cmap="coolwarm")
            fig.colorbar(fill, ax=ax, label="sin(x) cos(y)")
            ax.set(xlabel="x", ylabel="y", title="Signed field")
            plt.show()
            """,
        ),
    ],
    "改变 `levels` 的数量（5、10、20），比较细节和可读性的变化；再用 `imshow()` 显示同一数据。",
    "等高线强调特定数值边界，填充等高线强调区域变化。绘图前先检查网格与数据形状是否一致。",
    "https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.contour.html",
))


created.append(build(
    22,
    "colorbar",
    "颜色条 colorbar()",
    "https://www.runoob.com/matplotlib/matplotlib-ref-colorbar.html",
    "- 把图像或散点图的颜色对应到数值。\n"
    "- 调整色标方向、刻度和标签。\n"
    "- 在多个子图之间共享一个颜色条。",
    "先通过 `imshow()`、`scatter()` 或 `contourf()` 获取可映射颜色的对象 `mappable`，"
    "然后调用 `fig.colorbar(mappable, ax=ax)`。`vmin/vmax` 或 `norm` 控制颜色与数据的关系。"
    "比较多张图时应固定相同的颜色范围，防止相同颜色代表不同数值。",
    """
    import numpy as np
    import matplotlib.pyplot as plt
    rng = np.random.default_rng(22)
    base = np.arange(100, dtype=float).reshape(10, 10)
    """,
    [
        (
            "热力图的颜色条",
            "固定颜色范围，让 0 和 100 的含义稳定。",
            """
            fig, ax = plt.subplots(figsize=(5, 4))
            image = ax.imshow(base, cmap="viridis", vmin=0, vmax=100)
            fig.colorbar(image, ax=ax, label="value")
            ax.set_title("Matrix and colorbar")
            plt.show()
            """,
        ),
        (
            "散点图的颜色条",
            "这里颜色来自第三个变量 `scores`，不是 x 或 y 坐标。",
            """
            xs = rng.uniform(0, 10, 80)
            ys = rng.uniform(0, 10, 80)
            scores = rng.uniform(0, 100, 80)
            fig, ax = plt.subplots(figsize=(6, 4))
            dots = ax.scatter(xs, ys, c=scores, cmap="plasma", vmin=0, vmax=100)
            fig.colorbar(dots, ax=ax, label="score")
            ax.set(xlabel="x", ylabel="y", title="Scatter with third variable")
            plt.show()
            """,
        ),
    ],
    [
        exercise(
            "给 `base` 画一张热力图，添加位于下方的水平颜色条，并让刻度显示 0、25、50、75、100。",
            """
            # TODO: 创建 fig, ax，imshow 后使用 fig.colorbar(..., orientation='horizontal')
            """,
            "`ticks=[0, 25, 50, 75, 100]` 可以直接传给 `fig.colorbar`。",
            """
            fig, ax = plt.subplots(figsize=(6, 4))
            image = ax.imshow(base, cmap="magma", vmin=0, vmax=100)
            fig.colorbar(image, ax=ax, orientation="horizontal",
                         ticks=[0, 25, 50, 75, 100], label="value", pad=0.12)
            ax.set_title("Horizontal colorbar")
            plt.show()
            """,
        ),
        exercise(
            "在两个并排子图中显示 `base` 和 `base / 2`，共用一个 0–100 的颜色条。观察第二张图为何整体更暗。",
            """
            # TODO: 两次 imshow 都指定 vmin=0、vmax=100，然后用 fig.colorbar(..., ax=axes)
            """,
            "共同色标的 `ax` 参数可以接收 `axes` 数组；两张图必须使用同一个 `cmap` 和数值范围。",
            """
            fig, axes = plt.subplots(1, 2, figsize=(8, 3), constrained_layout=True)
            im1 = axes[0].imshow(base, cmap="viridis", vmin=0, vmax=100)
            axes[0].set_title("Full scale")
            axes[1].imshow(base / 2, cmap="viridis", vmin=0, vmax=100)
            axes[1].set_title("Half values")
            fig.colorbar(im1, ax=axes, label="value")
            plt.show()
            """,
        ),
    ],
    "尝试把颜色映射换成 `coolwarm`，让负值与正值分别对应冷、暖两色，并在颜色条上明确标出零点。",
    "颜色条必须关联到绘图函数返回的可映射对象；跨图比较要固定色标范围。",
    "https://matplotlib.org/stable/api/_as_gen/matplotlib.figure.Figure.colorbar.html",
))


created.append(build(
    23,
    "step",
    "阶梯图 step()",
    "https://www.runoob.com/matplotlib/matplotlib-apiref.html",
    "- 用阶梯图表现分段保持不变的数据。\n"
    "- 比较 `where='pre'`、`'post'`、`'mid'`。\n"
    "- 知道阶梯图与折线图适用的数据含义不同。",
    "`ax.step(x, y, where=...)` 的 `where` 决定阶梯跳变发生在采样点之前、之后还是中间。"
    "`post` 表示一个值从当前 x 保持到下一个 x；它不会在最后一个 x 之后自动延伸。"
    "对已经知道每个区间边界的数据，`stairs()` 也是可选方法。",
    """
    import numpy as np
    import matplotlib.pyplot as plt
    hours = np.arange(0, 7)
    level = np.array([1, 1, 2, 2, 4, 3, 3])
    """,
    [
        (
            "三种跳变位置对比",
            "用同一组数据比较 pre、post、mid 的含义。",
            """
            fig, axes = plt.subplots(1, 3, figsize=(11, 3), sharey=True)
            for ax, place in zip(axes, ["pre", "post", "mid"]):
                ax.step(hours, level, where=place, marker="o")
                ax.set_title(f"where={place}")
                ax.set_xticks(hours)
                ax.grid(alpha=0.25)
            fig.tight_layout()
            plt.show()
            """,
        ),
        (
            "与普通折线比较",
            "库存或状态在两次记录之间保持不变，阶梯图比斜线更贴切。",
            """
            fig, ax = plt.subplots(figsize=(7, 4))
            ax.plot(hours, level, "--", alpha=0.5, label="linear interpolation")
            ax.step(hours, level, where="post", label="held value")
            ax.set(xlabel="hour", ylabel="level", title="Two interpretations")
            ax.legend()
            plt.show()
            """,
        ),
    ],
    [
        exercise(
            "给定时刻 `[0,2,4,6,8]` 与状态 `[0,1,1,0,1]`，画 `where='post'` 的阶梯图，并设置 y 轴刻度为 0/1。",
            """
            t = np.array([0, 2, 4, 6, 8])
            state = np.array([0, 1, 1, 0, 1])
            # TODO: 绘制阶梯图；y 轴仅显示 0、1
            """,
            "使用 `ax.step(t, state, where='post')` 和 `ax.set_yticks([0, 1])`。",
            """
            t = np.array([0, 2, 4, 6, 8])
            state = np.array([0, 1, 1, 0, 1])
            fig, ax = plt.subplots()
            ax.step(t, state, where="post", marker="o")
            ax.set_yticks([0, 1])
            ax.set(xlabel="time", ylabel="state", title="On/off state")
            plt.show()
            """,
        ),
        exercise(
            "对 `hours/level` 分别画 `pre` 与 `post` 两个子图，突出它们在 x=2 附近的跳变差异。",
            """
            # TODO: 用 plt.subplots(1,2) 分别作图，并用 ax.axvline(2, ...) 标位置
            """,
            "两张图共用 y 轴；标上垂直参考线更容易看到跳变位置。",
            """
            fig, axes = plt.subplots(1, 2, figsize=(9, 3), sharey=True)
            for ax, place in zip(axes, ["pre", "post"]):
                ax.step(hours, level, where=place, marker="o")
                ax.axvline(2, color="tomato", linestyle="--", alpha=0.7)
                ax.set(title=f"{place} at x=2", xlabel="hour")
                ax.grid(alpha=0.2)
            fig.tight_layout()
            plt.show()
            """,
        ),
    ],
    "用 `stairs(values, edges)` 表示已知区间边界的计数，比较它与 `step()` 的输入方式。",
    "阶梯图适合分段常量，如开关状态、库存和计数更新。选择 `where` 前先定义每个值在哪段区间有效。",
    "https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.step.html",
))


created.append(build(
    24,
    "stackplot",
    "堆叠面积图 stackplot()",
    "https://www.runoob.com/matplotlib/matplotlib-apiref.html",
    "- 显示多组正值数据的总量与组成。\n"
    "- 给每层添加图例并核对累计总量。\n"
    "- 制作百分比堆叠面积图。",
    "`ax.stackplot(x, y1, y2, ..., labels=...)` 将各序列在每个 x 上累加成面积层。"
    "最上方的轮廓代表总量。`baseline='zero'` 从零轴开始，适合读数；"
    "`baseline='sym'` 会把图形居中，强调形状。输入序列应为非负值，且长度都与 x 一致。",
    """
    import numpy as np
    import matplotlib.pyplot as plt
    months = np.arange(1, 7)
    desktop = np.array([18, 20, 23, 25, 24, 28])
    mobile = np.array([12, 15, 16, 19, 22, 24])
    tablet = np.array([5, 6, 5, 7, 8, 9])
    total = desktop + mobile + tablet
    """,
    [
        (
            "总量与组成",
            "关注最上方边界是否等于三组数据的逐月总和。",
            """
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.stackplot(months, desktop, mobile, tablet,
                         labels=["desktop", "mobile", "tablet"], alpha=0.85)
            ax.plot(months, total, color="black", linewidth=1, label="total")
            ax.set(xlabel="month", ylabel="users", title="Users by device")
            ax.legend(loc="upper left")
            plt.show()
            """,
        ),
        (
            "零基线与对称基线",
            "两张图包含同样的数据，但对称基线改变了视觉中心。",
            """
            fig, axes = plt.subplots(1, 2, figsize=(10, 3), sharex=True)
            for ax, baseline in zip(axes, ["zero", "sym"]):
                ax.stackplot(months, desktop, mobile, tablet, baseline=baseline)
                ax.set_title(f"baseline={baseline}")
                ax.set_xticks(months)
            fig.tight_layout()
            plt.show()
            """,
        ),
    ],
    [
        exercise(
            "画三组设备数据的堆叠面积图，在上方叠加总量折线，并标出第 6 个月总量。",
            """
            # TODO: stackplot + plot(total) + annotate 最后一个点
            """,
            "`ax.annotate(str(total[-1]), xy=(months[-1], total[-1]), xytext=(-25, 15), textcoords='offset points')`。",
            """
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.stackplot(months, desktop, mobile, tablet,
                         labels=["desktop", "mobile", "tablet"])
            ax.plot(months, total, color="black", label="total")
            ax.annotate(str(total[-1]), xy=(months[-1], total[-1]),
                        xytext=(-25, 15), textcoords="offset points",
                        arrowprops={"arrowstyle": "->"})
            ax.set(title="Monthly total", xlabel="month", ylabel="users")
            ax.legend()
            plt.show()
            """,
        ),
        exercise(
            "把三组数据转换为每月百分比，再绘制 100% 堆叠面积图；y 轴固定在 0–100。",
            """
            # TODO: 每个序列除以 total 并乘 100，再 stackplot
            """,
            "例如 `desktop_pct = 100 * desktop / total`；三组百分比之和应接近 100。",
            """
            desktop_pct = 100 * desktop / total
            mobile_pct = 100 * mobile / total
            tablet_pct = 100 * tablet / total
            assert np.allclose(desktop_pct + mobile_pct + tablet_pct, 100)
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.stackplot(months, desktop_pct, mobile_pct, tablet_pct,
                         labels=["desktop", "mobile", "tablet"])
            ax.set_ylim(0, 100)
            ax.set(xlabel="month", ylabel="share (%)", title="Device share")
            ax.legend(loc="upper left")
            plt.show()
            """,
        ),
    ],
    "添加第四组数据，观察总量和各层厚度怎样变化；思考何时分组折线图更方便比较单组趋势。",
    "堆叠面积图能同时表达总量和组成。百分比版本表达占比变化，应明确 y 轴单位并检查每期之和为 100%。",
    "https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.stackplot.html",
))


created.append(build(
    25,
    "quiver",
    "矢量场箭头图 quiver()",
    "https://www.runoob.com/matplotlib/matplotlib-ref-spans-vectors.html",
    "- 使用 `X/Y` 指定箭头位置，使用 `U/V` 指定方向。\n"
    "- 让颜色表示速度大小。\n"
    "- 比较箭头图与流线图的视觉表达。",
    "`ax.quiver(X, Y, U, V)` 在网格位置 `(X, Y)` 画出分量为 `(U, V)` 的箭头。"
    "`np.hypot(U, V)` 计算长度，可作为第 5 个参数映射颜色。"
    "`streamplot(x, y, U, V)` 连接相邻方向形成流线。用 `set_aspect('equal')` 避免方向视觉失真。",
    """
    import numpy as np
    import matplotlib.pyplot as plt
    x = np.linspace(-2, 2, 11)
    y = np.linspace(-2, 2, 11)
    X, Y = np.meshgrid(x, y)
    U, V = -Y, X
    speed = np.hypot(U, V)
    print("网格与分量形状：", X.shape, U.shape, V.shape)
    """,
    [
        (
            "旋转方向的箭头图",
            "在位置 `(x,y)` 使用向量 `(-y,x)`，箭头围绕原点旋转。",
            """
            fig, ax = plt.subplots(figsize=(5, 5))
            arrows = ax.quiver(X, Y, U, V, speed, cmap="viridis")
            fig.colorbar(arrows, ax=ax, label="speed")
            ax.set(xlabel="x", ylabel="y", title="Rotational field")
            ax.set_aspect("equal")
            plt.show()
            """,
        ),
        (
            "与流线图比较",
            "同一个向量场可用连续流线显示方向变化；这里的 `x/y` 是一维规则网格。",
            """
            fig, ax = plt.subplots(figsize=(5, 5))
            flow = ax.streamplot(x, y, U, V, color=speed, cmap="plasma", density=1.2)
            fig.colorbar(flow.lines, ax=ax, label="speed")
            ax.set(xlabel="x", ylabel="y", title="Streamlines")
            ax.set_aspect("equal")
            plt.show()
            """,
        ),
    ],
    [
        exercise(
            "制作一个所有箭头都向右的均匀场：`U=1`、`V=0`，并将坐标轴设为等比例。",
            """
            right_u = np.ones_like(X)
            right_v = np.zeros_like(Y)
            # TODO: 用 ax.quiver 绘图，设置 equal aspect
            """,
            "箭头分量是 (1,0)，因此没有竖直方向分量。",
            """
            right_u = np.ones_like(X)
            right_v = np.zeros_like(Y)
            fig, ax = plt.subplots(figsize=(5, 5))
            ax.quiver(X, Y, right_u, right_v)
            ax.set_aspect("equal")
            ax.set_title("Uniform rightward flow")
            plt.show()
            """,
        ),
        exercise(
            "把矢量改为从原点向外扩散：`U=X`、`V=Y`。用颜色表示向量长度，并添加颜色条。",
            """
            radial_u, radial_v = X, Y
            # TODO: 计算长度；quiver 的第 5 个参数传长度；添加 colorbar
            """,
            "长度由 `np.hypot(radial_u, radial_v)` 计算。",
            """
            radial_u, radial_v = X, Y
            radial_speed = np.hypot(radial_u, radial_v)
            fig, ax = plt.subplots(figsize=(5, 5))
            arrows = ax.quiver(X, Y, radial_u, radial_v, radial_speed, cmap="magma")
            fig.colorbar(arrows, ax=ax, label="magnitude")
            ax.set_aspect("equal")
            ax.set_title("Radial field")
            plt.show()
            """,
        ),
    ],
    "尝试 `ax.quiverkey()` 为箭头长度设置标尺，再把网格点数从 11×11 提高到 21×21，观察密度变化。",
    "箭头的位置由 X/Y 决定，方向由 U/V 决定。颜色条可进一步表达强度；密度过高会影响读图。",
    "https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.quiver.html",
))


assert len(created) == 5
for path in created:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    assert notebook["nbformat"] == 4 and notebook["nbformat_minor"] == 5
    assert len(notebook["cells"]) == 19
    assert len({cell["id"] for cell in notebook["cells"]}) == 19
    code_cells = [cell for cell in notebook["cells"] if cell["cell_type"] == "code"]
    assert len(code_cells) == 7
    for cell in code_cells:
        ast.parse("".join(cell["source"]), filename=path.name)
        assert cell["outputs"] == [] and cell["execution_count"] is None
    print(f"PASS {path.name}: {len(notebook['cells'])} cells, {len(code_cells)} code")

try:
    import nbformat
except ImportError:
    print("nbformat unavailable; JSON and AST checks completed")
else:
    for path in created:
        nbformat.validate(nbformat.read(path, as_version=4))
    print("nbformat schema validation passed")
