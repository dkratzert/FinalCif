import subprocess
from pathlib import Path


def fix_comment(pyfile: Path) -> str:
    txt = pyfile.read_text()
    lines = txt.splitlines(keepends=True)
    for num, line in enumerate(lines):
        lines[num] = line.replace('PySide6', 'qtpy')
    lines[5] = ''  # f"## Form generated from reading UI file '{uifile.name}'\n"
    lines[7] = ''  # '"## Created by: Qt User Interface Compiler\n"
    txt = ''.join(lines)
    return txt


def compile_ui(uic_path: Path | None = None) -> None:
    ui_files = (Path(__file__).parent.parent / 'finalcif').rglob('*.ui')
    for ui_file in ui_files:
        compile_ui_file(ui_file, uic_path)


def compile_ui_file(ui_file: Path, uic_path: Path | None = None) -> None:
    py_file = ui_file.with_suffix('.py')
    if uic_path:
        uic_cmd = uic_path / 'pyside6-uic'
    else:
        uic_cmd = 'pyside6-uic'
    print(f"Compiling using {uic_cmd}...")
    subprocess.check_output([uic_cmd, '-a', ui_file, '-o', py_file])
    print(py_file, 'finished')
    txt = fix_comment(pyfile=py_file)
    py_file.write_text(data=txt)


if __name__ == '__main__':
    compile_ui()
