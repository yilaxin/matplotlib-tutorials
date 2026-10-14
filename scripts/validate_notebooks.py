"""Validate and render each notebook's Python cells in an isolated process."""
from __future__ import annotations

import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import traceback
import warnings

ROOT = Path(__file__).resolve().parent.parent


def worker(path: Path) -> int:
    os.environ['MPLBACKEND'] = 'Agg'
    import matplotlib.pyplot as plt
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    warnings.filterwarnings('ignore', message='.*non-interactive.*')
    nb = json.loads(path.read_text(encoding='utf-8'))
    if nb.get('nbformat') != 4:
        raise ValueError('Expected Notebook format 4')
    scope = {'__name__': '__main__'}

    def render_and_close(*args, **kwargs):
        for n in plt.get_fignums():
            plt.figure(n).canvas.draw()
        plt.close('all')

    plt.show = render_and_close
    work_root = ROOT / '.tmp'
    work_root.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='lesson-', dir=work_root) as temp:
        for index, cell in enumerate(nb['cells']):
            if cell['cell_type'] != 'code':
                continue
            try:
                code = compile(''.join(cell['source']), f'{path.name}:cell-{index + 1}', 'exec')
                previous = Path.cwd()
                try:
                    os.chdir(temp)
                    with contextlib.redirect_stdout(io.StringIO()):
                        exec(code, scope)
                    render_and_close()
                finally:
                    os.chdir(previous)
            except Exception:
                traceback.print_exc()
                return 1
    return 0


def main() -> int:
    paths = sorted((ROOT / 'notebooks').glob('*.ipynb')) + sorted((ROOT / 'supplements').glob('*.ipynb'))
    if len(paths) != 32:
        raise ValueError(f'Expected 32 notebooks; found {len(paths)}')
    failures = []
    start = time.monotonic()
    for path in paths:
        try:
            result = subprocess.run([sys.executable, str(Path(__file__).resolve()), '--worker', str(path)],
                                    capture_output=True, text=True, encoding='utf-8', errors='replace',
                                    timeout=120, env={**os.environ, 'PYTHONUTF8': '1'})
        except subprocess.TimeoutExpired:
            print(f'FAIL {path.name}: execution timed out', flush=True)
            failures.append(path)
            continue
        print(f'{"PASS" if result.returncode == 0 else "FAIL"} {path.name}', flush=True)
        if result.returncode:
            failures.append(path)
            print(result.stderr)
    print(f'{len(paths) - len(failures)}/{len(paths)} passed in {time.monotonic() - start:.1f}s')
    return bool(failures)


if __name__ == '__main__':
    if '--worker' in sys.argv:
        raise SystemExit(worker(Path(sys.argv[-1])))
    raise SystemExit(main())
