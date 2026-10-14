# Matplotlib 中文学习教材

面向 Python 数据可视化入门的学习资料：30 课 Jupyter Notebook、2 份补充笔记，以及可运行的示例与练习。

每课可以独立打开；第 01–10 课讲解常见图表，第 11–30 课包含学习目标、核心知识、示例、动手练习与参考答案。建议先完成练习，再阅读参考答案。

## 快速开始

建议使用 Python 3.13（本教材已在 Python 3.13.15 下验证）。在终端中运行：

```bash
git clone https://github.com/yilaxin/matplotlib-tutorials.git
cd matplotlib-tutorials
python -m venv .venv
```

激活虚拟环境（根据系统选择）：

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

```bash
# macOS / Linux
source .venv/bin/activate
```

安装依赖并启动：

```bash
python -m pip install -r requirements.txt
python -m jupyterlab
```

在 JupyterLab 中打开 `notebooks/` 下的课程，选择 Python 内核，按顺序运行单元格。GitHub 网页可以预览 Notebook，修改和执行代码请使用本地 JupyterLab。

## 学习路线

1. **入门（01–10）**：掌握标记、线型、坐标轴和基础图表。
2. **表达与输出（11–20）**：读写图像、配置中文字体、保存图表，学习误差棒、箱线图、图例和注释。
3. **进阶（21–30）**：等高线、颜色条、向量场、画布管理、频谱、二维统计、三角网格和极坐标。

## 课程目录

| 课次 | 主题 |
| --- | --- |
| 01 | [绘图标记](notebooks/Matplotlib_01_%E7%BB%98%E5%9B%BE%E6%A0%87%E8%AE%B0.ipynb) |
| 02 | [绘图线](notebooks/Matplotlib_02_%E7%BB%98%E5%9B%BE%E7%BA%BF.ipynb) |
| 03 | [轴标签和标题](notebooks/Matplotlib_03_%E8%BD%B4%E6%A0%87%E7%AD%BE%E5%92%8C%E6%A0%87%E9%A2%98.ipynb) |
| 04 | [网格线](notebooks/Matplotlib_04_%E7%BD%91%E6%A0%BC%E7%BA%BF.ipynb) |
| 05 | [绘制多图](notebooks/Matplotlib_05_%E7%BB%98%E5%88%B6%E5%A4%9A%E5%9B%BE.ipynb) |
| 06 | [散点图](notebooks/Matplotlib_06_%E6%95%A3%E7%82%B9%E5%9B%BE.ipynb) |
| 07 | [柱形图](notebooks/Matplotlib_07_%E6%9F%B1%E5%BD%A2%E5%9B%BE.ipynb) |
| 08 | [饼图](notebooks/Matplotlib_08_%E9%A5%BC%E5%9B%BE.ipynb) |
| 09 | [直方图](notebooks/Matplotlib_09_%E7%9B%B4%E6%96%B9%E5%9B%BE.ipynb) |
| 10 | [imshow](notebooks/Matplotlib_10_imshow.ipynb) |
| 11 | [imsave](notebooks/Matplotlib_11_imsave_%E7%BB%83%E4%B9%A0.ipynb) |
| 12 | [imread](notebooks/Matplotlib_12_imread_%E7%BB%83%E4%B9%A0.ipynb) |
| 13 | [中文显示](notebooks/Matplotlib_13_%E4%B8%AD%E6%96%87%E6%98%BE%E7%A4%BA_%E7%BB%83%E4%B9%A0.ipynb) |
| 14 | [常用函数](notebooks/Matplotlib_14_%E5%B8%B8%E7%94%A8%E5%87%BD%E6%95%B0_%E7%BB%83%E4%B9%A0.ipynb) |
| 15 | [savefig](notebooks/Matplotlib_15_savefig_%E7%BB%83%E4%B9%A0.ipynb) |
| 16 | [errorbar](notebooks/Matplotlib_16_errorbar_%E7%BB%83%E4%B9%A0.ipynb) |
| 17 | [boxplot](notebooks/Matplotlib_17_boxplot_%E7%BB%83%E4%B9%A0.ipynb) |
| 18 | [fill_between](notebooks/Matplotlib_18_fill_between_%E7%BB%83%E4%B9%A0.ipynb) |
| 19 | [legend](notebooks/Matplotlib_19_legend_%E7%BB%83%E4%B9%A0.ipynb) |
| 20 | [text_annotate](notebooks/Matplotlib_20_text_annotate_%E7%BB%83%E4%B9%A0.ipynb) |
| 21 | [contour](notebooks/Matplotlib_21_contour_%E7%BB%83%E4%B9%A0.ipynb) |
| 22 | [colorbar](notebooks/Matplotlib_22_colorbar_%E7%BB%83%E4%B9%A0.ipynb) |
| 23 | [step](notebooks/Matplotlib_23_step_%E7%BB%83%E4%B9%A0.ipynb) |
| 24 | [stackplot](notebooks/Matplotlib_24_stackplot_%E7%BB%83%E4%B9%A0.ipynb) |
| 25 | [quiver](notebooks/Matplotlib_25_quiver_%E7%BB%83%E4%B9%A0.ipynb) |
| 26 | [figure](notebooks/Matplotlib_26_figure_%E7%BB%83%E4%B9%A0.ipynb) |
| 27 | [figure_axes管理](notebooks/Matplotlib_27_figure_axes%E7%AE%A1%E7%90%86_%E7%BB%83%E4%B9%A0.ipynb) |
| 28 | [频谱分析](notebooks/Matplotlib_28_%E9%A2%91%E8%B0%B1%E5%88%86%E6%9E%90_%E7%BB%83%E4%B9%A0.ipynb) |
| 29 | [二维统计图](notebooks/Matplotlib_29_%E4%BA%8C%E7%BB%B4%E7%BB%9F%E8%AE%A1%E5%9B%BE_%E7%BB%83%E4%B9%A0.ipynb) |
| 30 | [三角网格和极坐标](notebooks/Matplotlib_30_%E4%B8%89%E8%A7%92%E7%BD%91%E6%A0%BC%E5%92%8C%E6%9E%81%E5%9D%90%E6%A0%87_%E7%BB%83%E4%B9%A0.ipynb) |

## 补充笔记

- [Matplotlib_Pyplot_菜鸟教程](supplements/Matplotlib_Pyplot_%E8%8F%9C%E9%B8%9F%E6%95%99%E7%A8%8B.ipynb)
- [Matplotlib_后续10节_菜鸟教程](supplements/Matplotlib_%E5%90%8E%E7%BB%AD10%E8%8A%82_%E8%8F%9C%E9%B8%9F%E6%95%99%E7%A8%8B.ipynb)

## 文件说明

```text
notebooks/      01–30 课，按编号顺序学习
supplements/    Pyplot 入门和基础图表合辑，与部分课程内容重叠
demos/          独立运行的演示脚本
scripts/        第 11–30 课的 Notebook 生成脚本、课程验证工具
requirements.txt  运行和学习环境依赖
```

在仓库根目录运行 `python demos/tick_params_demo.py` 可生成刻度字号对比图。
生成脚本会覆盖 `notebooks/` 中对应课程，修改前请先保存自己的笔记。例如：

```bash
python scripts/generate_matplotlib_11_20.py
```

## 常见问题

- **中文显示为方框**：参考第 13 课选择本机可用中文字体。也可以在导入 `matplotlib.pyplot` 后设置 `plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Noto Sans CJK SC', 'DejaVu Sans']`，并设置 `plt.rcParams['axes.unicode_minus'] = False`。只会使用本机已安装的字体。
- **图片保存在哪里**：部分课程在当前工作目录创建 `matplotlib_练习输出/`；文件路径会在课程中打印。自动生成的图片和运行输出已加入 Git 忽略规则。
- **练习单元看起来没有画图**：练习代码可能只包含注释或待完成部分，这是留给学习者修改的区域。
- **参数兼容性**：绘图库依赖固定为已验证的 Matplotlib 3.11.2 和 NumPy 2.5.3；升级后建议重新运行验证工具。

## 验证课程

```bash
python scripts/validate_notebooks.py
```

验证工具逐个读取 Notebook，在独立临时目录、独立 Python 进程中顺序执行代码单元，并强制渲染所有图形；不会覆盖学习文件或提交运行输出。它检查代码运行与图形渲染，不评判习题答案是否正确。验证结果见 [VALIDATION.md](VALIDATION.md)。

## 参考来源

课程中的原有来源链接与说明已保留。这些文件为本地学习笔记与练习整理；引用资料的权利归原作者所有。

- [Matplotlib 官方文档](https://matplotlib.org/stable/)
- [NumPy 官方文档](https://numpy.org/doc/stable/)
- [菜鸟教程 Matplotlib 教程](https://www.runoob.com/matplotlib/matplotlib-tutorial.html)
