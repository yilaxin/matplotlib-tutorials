"""Generate ten self-contained Matplotlib practice notebooks (lessons 11-20)."""

from __future__ import annotations

import ast
import json
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent / "notebooks"


def lines(value: str) -> list[str]:
    return textwrap.dedent(value).strip("\n").splitlines(keepends=True)


def md(value: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": lines(value)}


def code(value: str, *, solution: bool = False) -> dict:
    metadata = {"tags": ["参考答案"]} if solution else {}
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": metadata,
        "outputs": [],
        "source": lines(value),
    }


def ex(prompt: str, starter: str, hint: str, answer: str) -> tuple[str, str, str, str]:
    return prompt, starter, hint, answer


def lesson(
    number: int,
    slug: str,
    title: str,
    origin: str,
    source_url: str,
    goals: str,
    concepts: str,
    setup: str,
    examples: list[tuple[str, str, str]],
    exercises: list[tuple[str, str, str, str]],
    challenge: str,
    summary: str,
) -> None:
    cells = [
        md(
            f"# 第 {number} 课：{title}｜练习\n\n"
            f"**来源：{origin}。** 本课根据 [菜鸟教程对应页面]({source_url}) 编写，"
            "示例与练习均为重新设计。\n\n"
            f"## 学习目标\n\n{goals}\n\n"
            "使用方法：按顺序运行；先修改“动手练习”的代码单元，再查看紧随其后的参考答案。"
        ),
        md(f"## 核心知识\n\n{concepts}"),
        code(setup),
    ]
    for title_text, explanation, example_code in examples:
        cells.extend(
            [
                md(f"## 示例：{title_text}\n\n{explanation}"),
                code(example_code),
            ]
        )
    for index, (prompt, starter, hint, answer) in enumerate(exercises, 1):
        cells.extend(
            [
                md(f"## 动手练习 {index}\n\n{prompt}"),
                code(starter),
                md(f"<details><summary>提示（先自己试一试）</summary>\n\n{hint}\n\n</details>"),
                md("### 参考答案\n\n完成上面的代码后，再运行下面的答案单元进行对照。"),
                code(answer, solution=True),
            ]
        )
    cells.append(md(f"## 提高练习\n\n{challenge}"))
    cells.append(md(f"## 本课小结\n\n{summary}\n\n资料：[菜鸟教程原文]({source_url})。"))
    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    for index, cell in enumerate(cells):
        cell["id"] = f"matplotlib-{number}-{index:02d}"
    path = ROOT / f"Matplotlib_{number:02d}_{slug}_练习.ipynb"
    path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{path.name}: {len(cells)} cells")


lesson(
    11,
    "imsave",
    "保存数组图像 imsave()",
    "基础教程",
    "https://www.runoob.com/matplotlib/matplotlib-imsave.html",
    "- 理解 `imsave(fname, arr, cmap=...)` 保存的是像素数组。\n"
    "- 区分二维灰度数据和三维 RGB 数据。\n"
    "- 学会指定颜色映射与检查输出路径。",
    "`plt.imsave()` 接收 `H×W` 的二维数组，或 `H×W×3/4` 的 RGB/RGBA 数组。"
    "二维数组会经过颜色映射，因此 `cmap='gray'` 和 `cmap='viridis'` 得到不同的像素颜色。"
    "RGB 图像的浮点值通常应在 `[0, 1]`，整数值通常在 `[0, 255]`。"
    "注意：`imsave` 保存数组本身；带标题、坐标轴和图例的完整图表请用 `fig.savefig()`。",
    """
    from pathlib import Path
    import numpy as np
    import matplotlib.pyplot as plt
    OUTPUT = Path.cwd() / "matplotlib_练习输出"
    OUTPUT.mkdir(exist_ok=True)
    print("文件输出目录：", OUTPUT)
    """,
    [
        (
            "保存二维渐变图",
            "`np.tile` 将一行灰度值复制成二维图像。先显示，再保存，比较颜色映射。",
            """
            gradient = np.tile(np.linspace(0, 1, 256), (80, 1))
            fig, ax = plt.subplots(figsize=(7, 2))
            ax.imshow(gradient, cmap="gray", vmin=0, vmax=1)
            ax.set_axis_off()
            plt.show()
            gray_path = OUTPUT / "11_gradient_gray.png"
            plt.imsave(gray_path, gradient, cmap="gray", vmin=0, vmax=1)
            print(gray_path.name, "已保存；大小：", gray_path.stat().st_size, "字节")
            """,
        ),
        (
            "保存 RGB 色块",
            "三维数组的最后一维依次表示红、绿、蓝。这里不需要 `cmap`。",
            """
            rgb = np.zeros((90, 180, 3), dtype=float)
            rgb[:, :60, 0] = 1
            rgb[:, 60:120, 1] = 1
            rgb[:, 120:, 2] = 1
            rgb_path = OUTPUT / "11_rgb_blocks.png"
            plt.imsave(rgb_path, rgb)
            plt.imshow(rgb)
            plt.axis("off")
            plt.show()
            print("形状：", rgb.shape, "输出：", rgb_path)
            """,
        ),
    ],
    [
        ex(
            "将上面 `gradient` 保存成 `11_gradient_viridis.png`。要求使用 `viridis` 颜色映射，并检查文件确实存在。",
            """
            viridis_path = OUTPUT / "11_gradient_viridis.png"
            # TODO: 调用 plt.imsave，传入 gradient 和 cmap
            print("存在吗？", viridis_path.exists())
            """,
            "调用形式是 `plt.imsave(文件路径, 二维数组, cmap='viridis')`。",
            """
            viridis_path = OUTPUT / "11_gradient_viridis.png"
            plt.imsave(viridis_path, gradient, cmap="viridis", vmin=0, vmax=1)
            assert viridis_path.is_file() and viridis_path.stat().st_size > 0
            print("保存成功：", viridis_path)
            """,
        ),
        ex(
            "创建一个 60×90 的 RGB 图像：左半边为黄色（红+绿），右半边为青色（绿+蓝），保存为 PNG。",
            """
            two_colors = np.zeros((60, 90, 3), dtype=float)
            # TODO: 给各区域的颜色通道赋值
            two_colors_path = OUTPUT / "11_two_colors.png"
            # TODO: 保存并显示
            """,
            "黄色是 `(1,1,0)`，青色是 `(0,1,1)`；列切片可用 `:45` 和 `45:`。",
            """
            two_colors = np.zeros((60, 90, 3), dtype=float)
            two_colors[:, :45, 0:2] = 1
            two_colors[:, 45:, 1:3] = 1
            two_colors_path = OUTPUT / "11_two_colors.png"
            plt.imsave(two_colors_path, two_colors)
            plt.imshow(two_colors)
            plt.axis("off")
            plt.show()
            assert two_colors_path.is_file()
            """,
        ),
    ],
    "将一个二维正弦波数组分别用 `gray`、`plasma` 和 `coolwarm` 保存，比较图像颜色是否相同。解释为什么数据数组保持不变。",
    "`imsave()` 是像素数组保存工具；它不会把图表标题、坐标轴或图例一起保存。\n"
    "- [ ] 我能说出二维数组与 RGB 数组的形状区别。\n"
    "- [ ] 我能为二维数据指定 `cmap`。\n"
    "- [ ] 我会用 `Path.exists()` 检查结果。",
)


lesson(
    12,
    "imread",
    "读取与处理图像 imread()",
    "基础教程",
    "https://www.runoob.com/matplotlib/matplotlib-imread.html",
    "- 使用 `imread()` 读取 PNG 文件并查看形状和数据类型。\n"
    "- 用 NumPy 完成裁剪、亮度调整、通道修改。\n"
    "- 让练习在没有外部图片文件时也能运行。",
    "`plt.imread(path)` 返回 NumPy 数组。PNG 常返回 `[0,1]` 的浮点值；其他格式或后端可能不同，"
    "所以处理前应检查 `dtype`、最小值和最大值。RGB/RGBA 图像最后一维是颜色通道。"
    "裁剪用 `image[行范围, 列范围, :]`；亮度缩放之后可用 `np.clip(..., 0, 1)` 控制范围。",
    """
    from pathlib import Path
    import numpy as np
    import matplotlib.pyplot as plt
    OUTPUT = Path.cwd() / "matplotlib_练习输出"
    OUTPUT.mkdir(exist_ok=True)
    # 自己生成输入图像，避免依赖网络下载或其他课程的输出。
    yy, xx = np.mgrid[0:120, 0:180]
    sample = np.zeros((120, 180, 3), dtype=float)
    sample[..., 0] = xx / 179
    sample[..., 1] = yy / 119
    sample[..., 2] = 0.25
    sample_path = OUTPUT / "12_input.png"
    plt.imsave(sample_path, sample)
    print("练习图片：", sample_path)
    """,
    [
        (
            "读取、检查和显示",
            "读图后先看 `shape`、`dtype` 和像素范围。不同机器上的图像格式实现可能影响类型。",
            """
            image = plt.imread(sample_path)
            print("shape:", image.shape, "dtype:", image.dtype)
            print("像素范围：", float(image.min()), float(image.max()))
            plt.imshow(image)
            plt.axis("off")
            plt.show()
            """,
        ),
        (
            "裁剪和亮度对照",
            "使用子图比较原图、局部裁剪和变暗后的图像。PNG 可能包含 alpha 通道，因此只处理前三个颜色通道。",
            """
            crop = image[25:95, 40:140, :]
            darker = image.copy()
            darker[..., :3] = np.clip(darker[..., :3] * 0.5, 0, 1)
            fig, axes = plt.subplots(1, 3, figsize=(10, 3))
            for ax, data, title in zip(axes, [image, crop, darker], ["original", "crop", "darker"]):
                ax.imshow(data)
                ax.set_title(title)
                ax.axis("off")
            fig.tight_layout()
            plt.show()
            """,
        ),
    ],
    [
        ex(
            "从 `image` 中裁剪行 20:100、列 60:150，显示裁剪结果并打印其高度和宽度。",
            """
            # TODO: 从 image 裁剪出区域 crop_ex1
            # TODO: 打印前两维形状并显示
            """,
            "数组前两维分别表示高度（行）和宽度（列）。",
            """
            crop_ex1 = image[20:100, 60:150, :]
            print("高度、宽度：", crop_ex1.shape[:2])
            assert crop_ex1.shape[:2] == (80, 90)
            plt.imshow(crop_ex1)
            plt.axis("off")
            plt.show()
            """,
        ),
        ex(
            "制作一张“偏红”图像：把 G、B 通道都乘以 0.2，保持 R 和 alpha 不变；保存为 `12_red_tint.png`。",
            """
            red_tint = image.copy()
            # TODO: 修改 G、B 通道，并保存、显示
            """,
            "通道 0、1、2 对应 R、G、B；`red_tint[..., 1:3] *= 0.2`。",
            """
            red_tint = image.copy()
            red_tint[..., 1:3] *= 0.2
            red_path = OUTPUT / "12_red_tint.png"
            plt.imsave(red_path, red_tint)
            plt.imshow(red_tint)
            plt.axis("off")
            plt.show()
            assert red_path.is_file()
            """,
        ),
    ],
    "将图像上下翻转（`image[::-1]`）并保存；再尝试左右翻转。比较像素数组的形状是否改变。",
    "先检查数组的 `shape/dtype/范围`，再处理像素；裁剪用切片，亮度调整用乘法，颜色修改用通道索引。",
)


lesson(
    13,
    "中文显示",
    "中文字体与负号显示",
    "基础教程",
    "https://www.runoob.com/matplotlib/matplotlib-zh.html",
    "- 查看当前环境中可用的中文字体。\n"
    "- 使用 `rcParams` 设置图表字体。\n"
    "- 解决负号显示成方框的问题。",
    "Matplotlib 的默认字体未必包含汉字字形。先从字体列表中找到机器上实际存在的字体，再设置"
    "`plt.rcParams['font.sans-serif']`。负号异常时可设置 `axes.unicode_minus=False`。"
    "本课代码会按系统已有字体挑选；如果一个都没有，会打印提醒。",
    """
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    candidates = ["Microsoft YaHei", "SimHei", "PingFang SC", "Heiti TC",
                  "Noto Sans CJK SC", "WenQuanYi Micro Hei"]
    installed = {item.name for item in font_manager.fontManager.ttflist}
    chinese_font = next((name for name in candidates if name in installed), None)
    if chinese_font:
        plt.rcParams["font.sans-serif"] = [chinese_font, "DejaVu Sans"]
        print("当前使用中文字体：", chinese_font)
    else:
        print("未发现预设的中文字体；如出现缺字方框，请安装中文字体后重启内核。")
    plt.rcParams["axes.unicode_minus"] = False
    """,
    [
        (
            "中文标题与坐标轴",
            "折线图的标题、轴标签、图例都使用中文。检查文字是否能正常显示。",
            """
            days = np.arange(1, 8)
            temperature = np.array([-3, -1, 2, 5, 3, 0, -2])
            fig, ax = plt.subplots(figsize=(7, 4))
            ax.plot(days, temperature, marker="o", label="气温")
            ax.set(title="一周气温变化", xlabel="日期（天）", ylabel="温度（℃）")
            ax.axhline(0, color="gray", linewidth=0.8)
            ax.legend()
            ax.grid(alpha=0.25)
            plt.show()
            """,
        ),
        (
            "局部字体设置",
            "如果不想修改全局配置，也可以只给单个标题指定 `FontProperties`。",
            """
            fig, ax = plt.subplots(figsize=(5, 3))
            ax.bar(["A", "B", "C"], [4, 7, 5])
            if chinese_font:
                prop = font_manager.FontProperties(family=chinese_font, size=14)
                ax.set_title("单图字体示例", fontproperties=prop)
            else:
                ax.set_title("Font demo")
            plt.show()
            """,
        ),
    ],
    [
        ex(
            "画出每月降水量 `[20, 35, 28, 41]` 的柱形图，设置中文标题、x/y 轴标签和中文图例。",
            """
            rain = [20, 35, 28, 41]
            months = ["一月", "二月", "三月", "四月"]
            # TODO: 绘图并设置标题、标签、图例
            """,
            "在 `ax.bar(..., label='降水量')` 后调用 `ax.legend()`。",
            """
            rain = [20, 35, 28, 41]
            months = ["一月", "二月", "三月", "四月"]
            fig, ax = plt.subplots()
            ax.bar(months, rain, label="降水量", color="skyblue")
            ax.set(title="前四个月降水量", xlabel="月份", ylabel="毫米")
            ax.legend()
            plt.show()
            """,
        ),
        ex(
            "画出 `y = x - 2`，其中 x 为 0 到 4。确认负数刻度的减号显示正常。",
            """
            x = np.arange(5)
            # TODO: 绘制 y = x - 2，并设置负号显示参数
            """,
            "设置 `plt.rcParams['axes.unicode_minus'] = False`；y 最小值为 -2。",
            """
            plt.rcParams["axes.unicode_minus"] = False
            x = np.arange(5)
            fig, ax = plt.subplots()
            ax.plot(x, x - 2, marker="o")
            ax.set(title="负数刻度检查", xlabel="x", ylabel="y")
            ax.grid(alpha=0.3)
            plt.show()
            """,
        ),
    ],
    "在已安装字体中寻找另一款中文字体，分别画两张图比较字形；使用 `plt.rc_context(...)` 临时设置字体，观察设置是否在退出上下文后恢复。",
    "先查询已安装字体，再设置字体名称；字体不可用时应安装字体或调整候选列表，不要假定每个平台都装有 `SimHei`。",
)


lesson(
    14,
    "常用函数",
    "常用函数与 Axes 接口",
    "基础教程的常用函数速查页",
    "https://www.runoob.com/matplotlib/matplotlib-func.html",
    "- 理解 Figure（整张画布）和 Axes（单张坐标图）的分工。\n"
    "- 用 `fig, ax = plt.subplots()` 组合多个绘图函数。\n"
    "- 根据数据类型选择折线、柱形、散点或直方图。",
    "`pyplot` 会操作当前图表；Axes 接口明确指出目标图，例如 `ax.plot()`、`ax.set_title()`。"
    "多子图练习推荐使用 `fig, axes = plt.subplots(...)`。常用函数按任务分为：创建图、绘制数据、"
    "标注/坐标、布局、导出。需要时用 `help(ax.plot)` 或官方文档查具体参数。",
    """
    import numpy as np
    import matplotlib.pyplot as plt
    rng = np.random.default_rng(14)
    x = np.arange(1, 7)
    sales = np.array([12, 15, 14, 18, 20, 23])
    """,
    [
        (
            "同一数据的两种调用方式",
            "`plt.plot()` 和 `ax.plot()` 都可以作图。后者在多子图中更容易区分目标。",
            """
            fig, ax = plt.subplots()
            ax.plot(x, sales, marker="o", label="sales")
            ax.set(title="Sales trend", xlabel="Month", ylabel="Units")
            ax.legend()
            plt.show()
            """,
        ),
        (
            "一个 Figure 上的两个 Axes",
            "两个子图可分别使用不同的图表类型，而不相互覆盖。",
            """
            fig, axes = plt.subplots(1, 2, figsize=(10, 4))
            axes[0].plot(x, sales, marker="o")
            axes[0].set_title("Trend")
            axes[1].bar(x, sales, color="teal")
            axes[1].set_title("Comparison")
            fig.tight_layout()
            plt.show()
            """,
        ),
    ],
    [
        ex(
            "创建一个 2×2 子图：依次画折线、柱形、散点图和一组随机数据的直方图；为每个子图加英文标题。",
            """
            fig, axes = plt.subplots(2, 2, figsize=(9, 7))
            # TODO: 在 axes[0,0]、axes[0,1]、axes[1,0]、axes[1,1] 中绘图
            plt.show()
            """,
            "`axes[1, 1].hist(rng.normal(size=100), bins=10)` 是直方图的例子。",
            """
            fig, axes = plt.subplots(2, 2, figsize=(9, 7))
            axes[0, 0].plot(x, sales, marker="o")
            axes[0, 0].set_title("Line")
            axes[0, 1].bar(x, sales)
            axes[0, 1].set_title("Bar")
            axes[1, 0].scatter(x, sales)
            axes[1, 0].set_title("Scatter")
            axes[1, 1].hist(rng.normal(size=100), bins=10)
            axes[1, 1].set_title("Histogram")
            fig.tight_layout()
            plt.show()
            """,
        ),
        ex(
            "用 `ax` 对象绘制销量增长，并在同一张图上添加 y=0 参考线、网格和图例。",
            """
            growth = np.diff(sales, prepend=sales[0])
            # TODO: 创建 fig, ax 并绘图
            """,
            "参考线用 `ax.axhline(0, ...)`，网格用 `ax.grid()`。",
            """
            growth = np.diff(sales, prepend=sales[0])
            fig, ax = plt.subplots()
            ax.plot(x, growth, marker="s", label="monthly change")
            ax.axhline(0, color="gray", linewidth=0.8)
            ax.set(xlabel="Month", ylabel="Change", title="Sales change")
            ax.grid(alpha=0.3)
            ax.legend()
            plt.show()
            """,
        ),
    ],
    "把练习 1 的 2×2 图表加上 Figure 总标题，统一坐标轴标签，并解释每个子图适合回答的不同问题。",
    "Figure 管画布，Axes 管单个坐标图。图表类型应服务于分析问题：趋势用折线，类别比较用柱形，变量关系用散点，分布用直方图。",
)


lesson(
    15,
    "savefig",
    "导出完整图表 savefig()",
    "参考文档延伸练习",
    "https://www.runoob.com/matplotlib/matplotlib-ref-savefig.html",
    "- 区分 `imsave()` 的像素保存和 `fig.savefig()` 的整张图表导出。\n"
    "- 使用 `dpi`、`bbox_inches` 和文件后缀控制输出。\n"
    "- 学会使用 PNG、SVG 等格式。",
    "`fig.savefig(path)` 会导出 Figure 上的所有 Axes、标题、标签和图例。`dpi` 决定位图的像素密度；"
    "`bbox_inches='tight'` 有助于减少裁剪。PNG 是位图，SVG 是矢量图。"
    "推荐通过 `fig.savefig` 指定具体 Figure，保存后再 `plt.show()`。",
    """
    from pathlib import Path
    import numpy as np
    import matplotlib.pyplot as plt
    OUTPUT = Path.cwd() / "matplotlib_练习输出"
    OUTPUT.mkdir(exist_ok=True)
    x = np.linspace(0, 2 * np.pi, 160)
    """,
    [
        (
            "保存完整曲线图",
            "先建图和配置标签，再保存。图例与坐标轴应出现在输出文件中。",
            """
            curve_fig, ax = plt.subplots(figsize=(6, 4))
            ax.plot(x, np.sin(x), label="sin(x)")
            ax.plot(x, np.cos(x), label="cos(x)")
            ax.set(title="Trigonometric curves", xlabel="x", ylabel="value")
            ax.legend()
            png_path = OUTPUT / "15_curves.png"
            curve_fig.savefig(png_path, dpi=150, bbox_inches="tight")
            print("输出：", png_path, "字节：", png_path.stat().st_size)
            plt.show()
            """,
        ),
        (
            "导出 SVG",
            "相同 Figure 可以保存为多种格式；SVG 适合需要继续编辑的线图。",
            """
            fig, ax = plt.subplots(figsize=(5, 3))
            ax.bar(["A", "B", "C"], [8, 12, 10], color="cornflowerblue")
            ax.set(title="Category comparison", ylabel="count")
            svg_path = OUTPUT / "15_bars.svg"
            fig.savefig(svg_path, bbox_inches="tight")
            print("输出：", svg_path.name, "字节：", svg_path.stat().st_size)
            plt.show()
            """,
        ),
    ],
    [
        ex(
            "把前面的曲线图保存为 `15_curves_high_res.png`，设置 `dpi=300`、`bbox_inches='tight'`，检查文件大小。",
            """
            high_path = OUTPUT / "15_curves_high_res.png"
            # TODO: 使用 curve_fig.savefig 保存第一个示例的曲线图
            print("存在吗？", high_path.exists())
            """,
            "`curve_fig.savefig(high_path, dpi=300, bbox_inches='tight')`。",
            """
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.plot(x, np.sin(x), label="sin(x)")
            ax.plot(x, np.cos(x), label="cos(x)")
            ax.set(title="Trigonometric curves", xlabel="x", ylabel="value")
            ax.legend()
            high_path = OUTPUT / "15_curves_high_res.png"
            fig.savefig(high_path, dpi=300, bbox_inches="tight")
            assert high_path.is_file() and high_path.stat().st_size > 0
            print("文件字节数：", high_path.stat().st_size)
            plt.show()
            """,
        ),
        ex(
            "创建带两个子图的 Figure，并保存为 `15_two_axes.svg`。一张子图为折线图，另一张为散点图。",
            """
            # TODO: plt.subplots(1, 2)，分别绘图并使用 fig.savefig
            """,
            "使用 `axes[0].plot(...)`、`axes[1].scatter(...)` 和 `fig.savefig(...)`。",
            """
            fig2, axes2 = plt.subplots(1, 2, figsize=(8, 3), constrained_layout=True)
            axes2[0].plot(x, np.sin(x))
            axes2[0].set_title("Line")
            axes2[1].scatter(x[::8], np.cos(x[::8]), s=20)
            axes2[1].set_title("Scatter")
            two_axes_path = OUTPUT / "15_two_axes.svg"
            fig2.savefig(two_axes_path)
            assert two_axes_path.is_file()
            plt.show()
            """,
        ),
    ],
    "把同一张图分别保存为 72 dpi 和 300 dpi 的 PNG，比较文件字节数；然后保存为 SVG，思考为何 SVG 没有按同样方式依赖像素密度。",
    "`savefig()` 导出完整 Figure，`imsave()` 保存像素数组。位图清晰度受 dpi 和画布尺寸影响；导出前确认标签与图例没有被截断。",
)


lesson(
    16,
    "errorbar",
    "误差棒 errorbar()",
    "参考文档延伸练习",
    "https://www.runoob.com/matplotlib/matplotlib-ref-errorbar.html",
    "- 用误差棒表示测量值的不确定性。\n"
    "- 区分标量误差、逐点误差和非对称误差。\n"
    "- 设置 `fmt`、`capsize` 和 `ecolor`。",
    "`ax.errorbar(x, y, yerr=..., fmt='o-')` 绘制数据点和误差棒。`yerr=0.5` 表示每个点使用相同"
    "的上下误差；一维数组可为每点设不同误差；形状为 `2×N` 的数组可表示下、上误差不相等。"
    "误差棒表达的是给定的不确定性，不会自动计算置信区间。",
    """
    import numpy as np
    import matplotlib.pyplot as plt
    x = np.arange(1, 6)
    means = np.array([5.2, 6.1, 5.8, 7.0, 7.4])
    """,
    [
        (
            "相同误差与逐点误差",
            "下面的两组线表示相同均值，但误差范围不同。比较图中的横帽长度。",
            """
            fig, ax = plt.subplots(figsize=(7, 4))
            ax.errorbar(x, means, yerr=0.4, fmt="o-", capsize=4, label="fixed ±0.4")
            ax.errorbar(x, means + 1, yerr=[0.2, 0.5, 0.3, 0.6, 0.4],
                        fmt="s--", capsize=4, label="varying")
            ax.set(xlabel="sample", ylabel="measurement", title="Error bars")
            ax.legend()
            ax.grid(alpha=0.25)
            plt.show()
            """,
        ),
        (
            "非对称误差",
            "`yerr` 的第一行是向下的误差，第二行是向上的误差。",
            """
            lower = np.array([0.2, 0.3, 0.5, 0.2, 0.4])
            upper = np.array([0.6, 0.4, 0.2, 0.8, 0.5])
            fig, ax = plt.subplots()
            ax.errorbar(x, means, yerr=np.vstack([lower, upper]), fmt="o",
                        color="navy", ecolor="orange", capsize=5)
            ax.set_title("Asymmetric uncertainty")
            plt.show()
            """,
        ),
    ],
    [
        ex(
            "绘制 `[10, 11, 13, 12]` 四个观测值，误差分别为 `[1, 0.5, 1.5, 0.8]`。要求绿色圆点、端帽长度为 5。",
            """
            measured = np.array([10, 11, 13, 12])
            errors = np.array([1, 0.5, 1.5, 0.8])
            # TODO: 绘制误差棒
            """,
            "传 `fmt='go-'`、`yerr=errors`、`capsize=5`。",
            """
            measured = np.array([10, 11, 13, 12])
            errors = np.array([1, 0.5, 1.5, 0.8])
            fig, ax = plt.subplots()
            ax.errorbar(np.arange(1, 5), measured, yerr=errors,
                        fmt="go-", capsize=5)
            ax.set(xlabel="trial", ylabel="value", title="Measurements with uncertainty")
            plt.show()
            """,
        ),
        ex(
            "用 `lower=[0.2, 0.4, 0.3]` 和 `upper=[0.5, 0.2, 0.6]` 绘制三个非对称误差棒。",
            """
            values = np.array([2.0, 2.4, 2.1])
            lower = np.array([0.2, 0.4, 0.3])
            upper = np.array([0.5, 0.2, 0.6])
            # TODO: 组成 2×3 的误差数组并绘图
            """,
            "`np.vstack([lower, upper])` 可以得到正确的形状。",
            """
            values = np.array([2.0, 2.4, 2.1])
            lower = np.array([0.2, 0.4, 0.3])
            upper = np.array([0.5, 0.2, 0.6])
            asymmetric = np.vstack([lower, upper])
            assert asymmetric.shape == (2, 3)
            fig, ax = plt.subplots()
            ax.errorbar([1, 2, 3], values, yerr=asymmetric,
                        fmt="s", ecolor="tab:red", capsize=4)
            ax.set_title("Asymmetric errors")
            plt.show()
            """,
        ),
    ],
    "给每个点额外添加 x 方向误差 `xerr`。思考什么时候横向误差也有实际意义。",
    "误差数组必须与点数匹配；`yerr` 可以是标量、逐点数组或 `2×N` 数组。误差棒的来源应在真实分析中说明。",
)


lesson(
    17,
    "boxplot",
    "箱线图 boxplot()",
    "参考文档延伸练习",
    "https://www.runoob.com/matplotlib/matplotlib-ref-boxplot.html",
    "- 识别中位数、四分位数、须线和离群点。\n"
    "- 比较多组数据的分布。\n"
    "- 使用 `patch_artist`、`showmeans` 与 `whis`。",
    "箱体上下边缘通常对应第 1、3 四分位数，中线是中位数。默认须线延伸到仍位于 "
    "1.5 倍四分位距内的最远数据点；须线外的点会作为离群值显示。"
    "箱线图展示分布概要，不能代替原始样本。",
    """
    import numpy as np
    import matplotlib.pyplot as plt
    rng = np.random.default_rng(17)
    group_a = rng.normal(70, 8, 80)
    group_b = rng.normal(76, 12, 80)
    group_c = np.concatenate([rng.normal(72, 6, 77), [100, 104, 109]])
    groups = [group_a, group_b, group_c]
    """,
    [
        (
            "比较三组成绩",
            "观察中位数、箱体宽度和离群点。箱体高度越大，四分位距越大。",
            """
            fig, ax = plt.subplots(figsize=(7, 4))
            ax.boxplot(groups, showmeans=True, patch_artist=True)
            ax.set_xticks([1, 2, 3])
            ax.set_xticklabels(["A", "B", "C"])
            ax.set(title="Score distributions", xlabel="group", ylabel="score")
            ax.grid(axis="y", alpha=0.25)
            plt.show()
            """,
        ),
        (
            "箱线图与数据点并排",
            "如果样本量较少，可以把点也画出来，避免只看摘要而忽略数据。",
            """
            small = [np.array([3, 4, 4, 5, 7, 9]), np.array([2, 3, 6, 6, 8, 10])]
            fig, ax = plt.subplots()
            ax.boxplot(small)
            ax.set_xticks([1, 2])
            ax.set_xticklabels(["X", "Y"])
            for pos, data in enumerate(small, 1):
                ax.scatter(np.full(len(data), pos) + rng.normal(0, 0.03, len(data)),
                           data, color="tab:orange", zorder=3)
            ax.set_title("Boxplot plus samples")
            plt.show()
            """,
        ),
    ],
    [
        ex(
            "绘制 `groups` 的水平箱线图，显示均值点，并使用 A/B/C 标签。",
            """
            # TODO: 创建图，使用 ax.boxplot(groups, vert=False, ...)
            """,
            "使用 `vert=False` 绘制水平箱线图；标签可由 `set_yticklabels()` 设置。",
            """
            fig, ax = plt.subplots(figsize=(7, 4))
            ax.boxplot(groups, vert=False, showmeans=True)
            ax.set_yticks([1, 2, 3])
            ax.set_yticklabels(["A", "B", "C"])
            ax.set(xlabel="score", title="Horizontal boxplots")
            ax.grid(axis="x", alpha=0.25)
            plt.show()
            """,
        ),
        ex(
            "比较 `whis=1.5` 和 `whis=(5,95)` 两种须线定义；用两个子图展示同一数据。",
            """
            # TODO: 创建两个子图并分别调用 boxplot
            """,
            "`whis=(5, 95)` 表示以第 5 与第 95 百分位作为须线目标。",
            """
            fig, axes = plt.subplots(1, 2, figsize=(10, 4), sharey=True)
            axes[0].boxplot(group_c, whis=1.5)
            axes[0].set_title("1.5 × IQR")
            axes[1].boxplot(group_c, whis=(5, 95))
            axes[1].set_title("5th–95th percentile")
            fig.tight_layout()
            plt.show()
            """,
        ),
    ],
    "把 `group_c` 中三个极端值去掉重新画图，比较中位数、四分位数和须线的变化。",
    "箱线图适合比较组间分布。须线的含义受 `whis` 参数影响，阅读图表时应说明其定义。",
)


lesson(
    18,
    "fill_between",
    "曲线之间填充 fill_between()",
    "参考文档延伸练习",
    "https://www.runoob.com/matplotlib/matplotlib-ref-fill_between.html",
    "- 用 `fill_between()` 标出曲线和基线之间的面积。\n"
    "- 表示上下界形成的区间。\n"
    "- 使用 `where` 和 `interpolate` 标出条件区域。",
    "`fill_between(x, y1, y2=0)` 在两条曲线之间填色。`where` 是与 x 同长度的布尔数组，"
    "决定填充哪些区间。两条曲线交叉时，`interpolate=True` 能在交点附近改善边界。"
    "`alpha` 让线条仍然可见。",
    """
    import numpy as np
    import matplotlib.pyplot as plt
    x = np.linspace(0, 2 * np.pi, 300)
    y = np.sin(x)
    """,
    [
        (
            "曲线与零线之间的面积",
            "使用两种颜色区分正值和负值区域。",
            """
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.plot(x, y, color="black", linewidth=1.5)
            ax.fill_between(x, y, 0, where=(y >= 0), color="seagreen",
                            alpha=0.3, interpolate=True, label="positive")
            ax.fill_between(x, y, 0, where=(y < 0), color="tomato",
                            alpha=0.3, interpolate=True, label="negative")
            ax.axhline(0, color="gray", linewidth=0.7)
            ax.legend()
            plt.show()
            """,
        ),
        (
            "用阴影表示区间",
            "上、下界可以各是一条曲线；阴影表示给定范围。",
            """
            center = np.cos(x)
            margin = 0.15 + 0.08 * np.abs(np.sin(x))
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.plot(x, center, color="navy", label="estimate")
            ax.fill_between(x, center - margin, center + margin,
                            color="cornflowerblue", alpha=0.25, label="range")
            ax.legend()
            ax.set_title("Estimate and interval")
            plt.show()
            """,
        ),
    ],
    [
        ex(
            "绘制 `y = sin(x)`，只填充 `y > 0.5` 的部分（与水平线 y=0.5 之间）。",
            """
            # TODO: 画线，并调用 fill_between(x, y, 0.5, where=...)
            """,
            "布尔条件为 `y > 0.5`；可添加 `interpolate=True`。",
            """
            fig, ax = plt.subplots()
            ax.plot(x, y, color="navy")
            ax.axhline(0.5, color="gray", linestyle="--")
            ax.fill_between(x, y, 0.5, where=(y > 0.5),
                            interpolate=True, alpha=0.35, color="orange")
            ax.set_title("Above threshold")
            plt.show()
            """,
        ),
        ex(
            "令上下界为 `cos(x) ± 0.25`，在同一图中绘制中心线、上下界与阴影。",
            """
            center = np.cos(x)
            # TODO: 定义上下界并绘制
            """,
            "上界为 `center + 0.25`，下界为 `center - 0.25`。",
            """
            center = np.cos(x)
            lower, upper = center - 0.25, center + 0.25
            fig, ax = plt.subplots()
            ax.plot(x, center, label="center")
            ax.plot(x, lower, color="gray", linewidth=0.8)
            ax.plot(x, upper, color="gray", linewidth=0.8)
            ax.fill_between(x, lower, upper, color="tab:blue", alpha=0.2,
                            label="±0.25")
            ax.legend()
            plt.show()
            """,
        ),
    ],
    "尝试 `fill_betweenx(y, x1, x2)` 绘制水平方向的带状区域，并解释它与 `fill_between()` 的区别。",
    "区域填充应有明确含义：基线以上、两条曲线差异、上下界范围等。不要把任意带状区误称为统计置信区间。",
)


lesson(
    19,
    "legend",
    "图例 legend()",
    "参考文档延伸练习",
    "https://www.runoob.com/matplotlib/matplotlib-ref-legend.html",
    "- 使用 `label` 和 `legend()` 解释多条曲线。\n"
    "- 调整 `loc`、`ncol`、`title` 和边框。\n"
    "- 把图例放到坐标轴外侧并避免裁切。",
    "设置了 `label` 的绘图对象可自动加入图例。`loc` 控制图例相对位置，"
    "`bbox_to_anchor` 用于精确锚定，`ncol` 决定列数。若图例位于绘图区之外，"
    "配合 `constrained_layout` 或 `bbox_inches='tight'` 可减少裁切。",
    """
    import numpy as np
    import matplotlib.pyplot as plt
    x = np.linspace(0, 2 * np.pi, 160)
    """,
    [
        (
            "三条曲线的图例",
            "每条曲线设置不同的 `label`，再统一调用 `ax.legend()`。",
            """
            fig, ax = plt.subplots(figsize=(7, 4))
            for k in (1, 2, 3):
                ax.plot(x, np.sin(k * x), label=f"sin({k}x)")
            ax.legend(loc="upper right", title="Functions", frameon=True)
            ax.set_title("Multiple curves")
            plt.show()
            """,
        ),
        (
            "图例放到右侧",
            "右侧留出位置，可减少线条与图例重叠。",
            """
            fig, ax = plt.subplots(figsize=(7, 4))
            ax.plot(x, np.sin(x), label="sine")
            ax.plot(x, np.cos(x), label="cosine")
            ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1), borderaxespad=0)
            ax.set_title("Legend outside axes")
            fig.tight_layout()
            plt.show()
            """,
        ),
    ],
    [
        ex(
            "绘制四条频率不同的余弦曲线，并让图例位于图底部，分两列显示。",
            """
            # TODO: 绘制四条曲线；legend(loc=..., ncol=2)
            """,
            "试试 `loc='upper center', bbox_to_anchor=(0.5, -0.12)`。",
            """
            fig, ax = plt.subplots(figsize=(7, 4))
            for k in range(1, 5):
                ax.plot(x, np.cos(k * x), label=f"cos({k}x)")
            ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12),
                      ncol=2, title="Frequencies")
            fig.subplots_adjust(bottom=0.28)
            plt.show()
            """,
        ),
        ex(
            "对一个分组柱形图添加图例。两组数据为 A=[4,6,8]、B=[5,7,6]，类别为 Q1/Q2/Q3。",
            """
            categories = ["Q1", "Q2", "Q3"]
            a = np.array([4, 6, 8])
            b = np.array([5, 7, 6])
            # TODO: 分组柱形图，调用 legend
            """,
            "先定义 `pos=np.arange(3)` 和 `width=0.35`，两组柱子的 x 位置分别为 `pos±width/2`。",
            """
            categories = ["Q1", "Q2", "Q3"]
            a = np.array([4, 6, 8])
            b = np.array([5, 7, 6])
            pos = np.arange(3)
            width = 0.35
            fig, ax = plt.subplots()
            ax.bar(pos - width / 2, a, width, label="A")
            ax.bar(pos + width / 2, b, width, label="B")
            ax.set_xticks(pos, categories)
            ax.legend(title="Series")
            plt.show()
            """,
        ),
    ],
    "给图例添加标题并切换 `frameon`；观察何时应该把图例放到图外，以及什么情况下直接在线条末端标注更易读。",
    "图例需要准确对应数据对象。`label` 通常写在绘图函数中，布局完成后检查图例是否遮挡数据或被裁切。",
)


lesson(
    20,
    "text_annotate",
    "文本与箭头标注 text() / annotate()",
    "参考文档延伸练习",
    "https://www.runoob.com/matplotlib/matplotlib-ref-text.html",
    "- 使用 `text()` 标出具体数值。\n"
    "- 使用 `annotate()` 指向峰值或异常点。\n"
    "- 区分 `xy`、`xytext` 与坐标系。",
    "`ax.text(x, y, s)` 在指定位置写文本。`ax.annotate(text, xy=..., xytext=..., "
    "arrowprops=...)` 中，`xy` 是指向的数据点，`xytext` 是文字放置位置。"
    "可以设置 `textcoords='offset points'`，让 `xytext` 成为相对数据点的像素级偏移。",
    """
    import numpy as np
    import matplotlib.pyplot as plt
    months = np.arange(1, 7)
    values = np.array([12, 16, 15, 22, 19, 25])
    """,
    [
        (
            "为柱形图添加数值",
            "`text()` 可以放在每根柱子的顶部。",
            """
            fig, ax = plt.subplots(figsize=(7, 4))
            bars = ax.bar(months, values, color="steelblue")
            for bar, value in zip(bars, values):
                ax.text(bar.get_x() + bar.get_width() / 2, value + 0.3,
                        str(value), ha="center", va="bottom")
            ax.set_ylim(0, 30)
            ax.set_title("Value labels")
            plt.show()
            """,
        ),
        (
            "用箭头指出峰值",
            "根据数据计算峰值索引，避免手工写死坐标。",
            """
            peak = int(np.argmax(values))
            fig, ax = plt.subplots(figsize=(7, 4))
            ax.plot(months, values, marker="o")
            ax.annotate("peak", xy=(months[peak], values[peak]),
                        xytext=(-45, -35), textcoords="offset points",
                        arrowprops={"arrowstyle": "->", "color": "tomato"})
            ax.set(xlabel="month", ylabel="value", title="Peak annotation")
            plt.show()
            """,
        ),
    ],
    [
        ex(
            "在折线图中自动找到最低值，并用箭头标注 `minimum`。文字放在该点右上方。",
            """
            # TODO: 用 np.argmin(values) 找位置，调用 ax.annotate
            """,
            "`xy=(months[idx], values[idx])`；`xytext=(25, 25)` 配合 `textcoords='offset points'`。",
            """
            idx = int(np.argmin(values))
            fig, ax = plt.subplots()
            ax.plot(months, values, marker="o")
            ax.annotate("minimum", xy=(months[idx], values[idx]),
                        xytext=(25, 25), textcoords="offset points",
                        arrowprops={"arrowstyle": "->"})
            ax.set_title("Minimum point")
            plt.show()
            """,
        ),
        ex(
            "画一条 60 点的正弦曲线，只在第 0、15、30、45 个点添加数值文本，不要给每个点都写标签。",
            """
            xs = np.linspace(0, 2 * np.pi, 60)
            ys = np.sin(xs)
            # TODO: 画线并为指定四个点调用 text
            """,
            "在 `for idx in (0, 15, 30, 45)` 中调用 `ax.text(xs[idx], ys[idx], ...)`。",
            """
            xs = np.linspace(0, 2 * np.pi, 60)
            ys = np.sin(xs)
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.plot(xs, ys)
            for idx in (0, 15, 30, 45):
                ax.scatter(xs[idx], ys[idx], color="tomato")
                ax.text(xs[idx], ys[idx] + 0.08, f"{ys[idx]:.2f}", ha="center")
            ax.set_ylim(-1.25, 1.25)
            ax.set_title("Selective labels")
            plt.show()
            """,
        ),
    ],
    "将第 15 课的双曲线图与本课标注结合：加图例，标出最高点，并导出完整 Figure；确认注释没有被裁切。",
    "`text()` 适合静态文字标签，`annotate()` 适合强调具体数据点。标签数量应控制在读者能快速辨认的范围。",
)


def validate_generated_notebooks() -> None:
    paths = sorted(ROOT.glob("Matplotlib_1[1-9]*_练习.ipynb"))
    paths += sorted(ROOT.glob("Matplotlib_20*_练习.ipynb"))
    assert len(paths) == 10, f"Expected 10 notebooks; got {len(paths)}"
    for path in paths:
        document = json.loads(path.read_text(encoding="utf-8"))
        assert document["nbformat"] == 4
        assert len(document["cells"]) == 19, path.name
        assert len({cell["id"] for cell in document["cells"]}) == len(document["cells"])
        code_cells = [cell for cell in document["cells"] if cell["cell_type"] == "code"]
        assert len(code_cells) == 7, path.name
        for cell in code_cells:
            ast.parse("".join(cell["source"]), filename=path.name)
            assert cell["execution_count"] is None and cell["outputs"] == []
        print(f"PASS {path.name}: {len(document['cells'])} cells, {len(code_cells)} code")
    try:
        import nbformat
    except ImportError:
        print("nbformat is unavailable; JSON and AST checks completed")
    else:
        for path in paths:
            nbformat.validate(nbformat.read(path, as_version=4))
        print("nbformat schema validation passed")


validate_generated_notebooks()
