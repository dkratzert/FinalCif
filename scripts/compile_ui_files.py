from pathlib import Path

from qtpy import uic

def fix_comment(pyfile: Path, uifile: Path):
    txt = pyfile.read_text()
    lines = txt.splitlines(keepends=True)
    lines[2] = f"# Form implementation generated from reading ui file '{uifile.name}'\n"
    lines[4] = "# Created by: PyQt5 UI code generator"
    pyfile.write_text(data=''.join(lines))


def compile_ui():
    ui_files = Path(__file__).parent.parent.rglob('*.ui')
    for ui_file in ui_files:
        compile_ui_file(ui_file)


def compile_ui_file(ui_file: Path) -> None:
    py_file = ui_file.with_suffix('.py')
    with open(py_file, 'w', encoding='utf-8') as pyf, open(ui_file, 'r', encoding='utf-8') as uif:
        uic.compileUi(uifile=uif, pyfile=pyf, execute=True)
        print(f'Compiling {ui_file.name}')
    fix_comment(pyfile=py_file, uifile=ui_file)


if __name__ == '__main__':
    compile_ui()
