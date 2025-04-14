import subprocess
from pathlib import Path


def fix_comment(pyfile: Path, uifile: Path):
    txt = pyfile.read_text()
    lines = txt.splitlines(keepends=True)
    lines[5] = ''#f"## Form generated from reading UI file '{uifile.name}'\n"
    lines[7] = ''#'"## Created by: Qt User Interface Compiler\n"
    pyfile.write_text(data=''.join(lines))


def compile_ui():
    ui_files = Path(__file__).parent.parent.rglob('*.ui')
    for ui_file in ui_files:
        compile_ui_file(ui_file)


def compile_ui_file(ui_file: Path) -> None:
    py_file = ui_file.with_suffix('.py')
    out = subprocess.check_output(['pyside6-uic', ui_file, '-o', py_file])
    #py_file.write_bytes(out)
    print(py_file, 'finished')
    fix_comment(pyfile=py_file, uifile=ui_file)


if __name__ == '__main__':
    compile_ui()
