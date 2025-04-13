import ast
import os
import re
import shutil


PYQT5_TO_PYQT6_IMPORTS = [
    (r'from\s+PyQt5\s+import\s+(QtWidgets|QtGui|QtCore|QtSvg)', r'from PySide6 import \1'),
    (r'import\s+PyQt5\.(QtWidgets|QtGui|QtCore|QtSvg)', r'import PySide6.\1'),
    (r'from\s+PyQt5\.(\w+)\s+import\s+(\w+)', r'from PySide6.\1 import \2'),

]

# Adjustments for Qt6 (e.g., enums and method renames)
COMMON_REPLACEMENTS = [
    # Methods
    (r'\.exec_\(', r'.exec('),
    (r'\.translate\(', r'.tr('),
    (r'\.setSectionResizeMode\(', r'.header().setSectionResizeMode('),
    (r'\.toUtf8\(\)', r'.encode()'),
    (r'\.isSignalConnected\(', r'.signalsBlocked('),  # ggf. prüfen, nicht immer gleichwertig

    # Signal/Slot/Property
    (r'(QtCore\.)?pyqtSignal', 'QtCore.Signal'),
    (r'(QtCore\.)?pyqtSlot', 'QtCore.Slot'),
    (r'(QtCore\.)?pyqtProperty', 'QtCore.Property'),

    # Qt Enums – QtCore.Qt
    (r'(QtCore\.)?Qt\.AlignVCenter', r'QtCore.Qt.AlignmentFlag.AlignVCenter'),
    (r'(QtCore\.)?Qt\.AlignHCenter', r'QtCore.Qt.AlignmentFlag.AlignHCenter'),
    (r'(QtCore\.)?Qt\.AlignLeft', r'QtCore.Qt.AlignmentFlag.AlignLeft'),
    (r'(QtCore\.)?Qt\.AlignRight', r'QtCore.Qt.AlignmentFlag.AlignRight'),
    (r'(QtCore\.)?Qt\.AlignTop', r'QtCore.Qt.AlignmentFlag.AlignTop'),
    (r'(QtCore\.)?Qt\.AlignBottom', r'QtCore.Qt.AlignmentFlag.AlignBottom'),
    (r'(QtCore\.)?Qt\.AlignCenter', r'QtCore.Qt.AlignmentFlag.AlignCenter'),

    (r'(QtCore\.)?Qt\.Horizontal', r'QtCore.Qt.Orientation.Horizontal'),
    (r'(QtCore\.)?Qt\.Vertical', r'QtCore.Qt.Orientation.Vertical'),

    (r'(QtCore\.)?Qt\.LeftToRight', r'QtCore.Qt.LayoutDirection.LeftToRight'),
    (r'(QtCore\.)?Qt\.RightToLeft', r'QtCore.Qt.LayoutDirection.RightToLeft'),

    # QtCore.Key – Tastatur-Enums
    (r'(QtCore\.)?Qt\.Key_', r'QtCore.Qt.Key.Key_'),

    # Mouse Buttons
    (r'(QtCore\.)?Qt\.LeftButton', r'QtCore.Qt.MouseButton.LeftButton'),
    (r'(QtCore\.)?Qt\.RightButton', r'QtCore.Qt.MouseButton.RightButton'),
    (r'(QtCore\.)?Qt\.MiddleButton', r'QtCore.Qt.MouseButton.MiddleButton'),

    # ItemFlags
    (r'(QtCore\.)?Qt\.ItemIsSelectable', r'QtCore.Qt.ItemFlag.ItemIsSelectable'),
    (r'(QtCore\.)?Qt\.ItemIsEnabled', r'QtCore.Qt.ItemFlag.ItemIsEnabled'),
    (r'(QtCore\.)?Qt\.ItemIsEditable', r'QtCore.Qt.ItemFlag.ItemIsEditable'),

    # WindowFlags
    (r'(QtCore\.)?Qt\.Window', r'QtCore.Qt.WindowType.Window'),
    (r'(QtCore\.)?Qt\.Dialog', r'QtCore.Qt.WindowType.Dialog'),
    (r'(QtCore\.)?Qt\.Too', r'QtCore.Qt.WindowType.Tool'),
    (r'(QtCore\.)?Qt\.Popup', r'QtCore.Qt.WindowType.Popup'),
    (r'(QtCore\.)?Qt\.Widget', r'QtCore.Qt.WindowType.Widget'),
    (r'(QtCore\.)?Qt\.Sheet', r'QtCore.Qt.WindowType.Sheet'),
    (r'(QtCore\.)?Qt\.Drawer', r'QtCore.Qt.WindowType.Drawer'),
    (r'(QtCore\.)?Qt\.ToolTip', r'QtCore.Qt.WindowType.ToolTip'),
    (r'(QtCore\.)?Qt\.SplashScreen', r'QtCore.Qt.WindowType.SplashScreen'),
    (r'(QtCore\.)?Qt\.SubWindow', r'QtCore.Qt.WindowType.SubWindow'),
    (r'(QtCore\.)?Qt\.ForeignWindow', r'QtCore.Qt.WindowType.ForeignWindow'),
    (r'(QtCore\.)?Qt\.CoverWindow', r'QtCore.Qt.WindowType.CoverWindow'),

    # WindowStates
    (r'(QtCore\.)?Qt\.WindowNoState', r'QtCore.Qt.WindowState.WindowNoState'),
    (r'(QtCore\.)?Qt\.WindowMinimized', r'QtCore.Qt.WindowState.WindowMinimized'),
    (r'(QtCore\.)?Qt\.WindowMaximized', r'QtCore.Qt.WindowState.WindowMaximized'),
    (r'(QtCore\.)?Qt\.WindowFullScreen', r'QtCore.Qt.WindowState.WindowFullScreen'),
    (r'(QtCore\.)?Qt\.WindowActive', r'QtCore.Qt.WindowState.WindowActive'),

    # Scrollbar
    (r'(QtCore\.)?Qt\.ScrollBarAsNeeded', r'Qt.ScrollBarPolicy.ScrollBarAsNeeded'),
    (r'(QtCore\.)?Qt\.ScrollBarAlwaysOff', r'Qt.ScrollBarPolicy.ScrollBarAlwaysOff'),
    (r'(QtCore\.)?Qt\.ScrollBarAlwaysOn', r'Qt.ScrollBarPolicy.ScrollBarAlwaysOn'),

    # WindowModality
    (r'(QtCore\.)?Qt\.NonModal', r'QtCore.Qt.WindowModality.NonModal'),
    (r'(QtCore\.)?Qt\.WindowModal', r'QtCore.Qt.WindowModality.WindowModal'),
    (r'(QtCore\.)?Qt\.ApplicationModal', r'QtCore.Qt.WindowModality.ApplicationModal'),

    # WidgetAttribute
    (r'(QtCore\.)?Qt\.WA_DeleteOnClose\W', r'QtCore.Qt.WidgetAttribute.WA_DeleteOnClose'),

    #QFont
    (r'(QtGui\.)?QFont\.Monospace\W', r'QtGui.QFont.StyleHint.Monospace'),

    # TransformationMode
    (r'(QtCore\.)?Qt\.FastTransformation\W', r'QtCore.Qt.TransformationMode.FastTransformation'),
    (r'(QtCore\.)?Qt\.SmoothTransformation\W', r'QtCore.Qt.TransformationMode.SmoothTransformation'),

    # ToolButtonStyle
    (r'(QtCore\.)?Qt\.ToolButtonIconOnly\W', r'QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly'),
    (r'(QtCore\.)?Qt\.ToolButtonTextOnly\W', r'QtCore.Qt.ToolButtonStyle.ToolButtonTextOnly'),
    (r'(QtCore\.)?Qt\.ToolButtonTextBesideIcon\W', r'QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon'),
    (r'(QtCore\.)?Qt\.ToolButtonTextUnderIcon\W', r'QtCore.Qt.ToolButtonStyle.ToolButtonTextUnderIcon'),
    (r'(QtCore\.)?Qt\.ToolButtonFollowStyle\W', r'QtCore.Qt.ToolButtonStyle.ToolButtonFollowStyle'),

    # TextInteraction
    (r'(QtCore\.)?Qt\.TextSelectableByMouse', r'QtCore.Qt.TextInteractionFlag.TextSelectableByMouse'),
    (r'(QtCore\.)?Qt\.TextSelectableByKeyboard', r'QtCore.Qt.TextInteractionFlag.TextSelectableByKeyboard'),

    # Modifier Keys
    (r'(QtCore\.)?Qt\.ControlModifier', r'QtCore.Qt.KeyboardModifier.ControlModifier'),
    (r'(QtCore\.)?Qt\.ShiftModifier', r'QtCore.Qt.KeyboardModifier.ShiftModifier'),

    # Cursor
    (r'(QtCore\.)?Qt\.WaitCursor', r'QtCore.Qt.CursorShape.WaitCursor'),
    (r'(QtCore\.)?Qt\.ArrowCursor', r'QtCore.Qt.CursorShape.ArrowCursor'),
    (r'(QtCore\.)?Qt\.PointingHandCursor', r'QtCore.Qt.CursorShape.PointingHandCursor'),

    # Sort order
    (r'(QtCore\.)?Qt\.AscendingOrder', r'QtCore.Qt.SortOrder.AscendingOrder'),
    (r'(QtCore\.)?Qt\.DescendingOrder', r'QtCore.Qt.SortOrder.DescendingOrder'),

    # Data roles
    (r'(QtCore\.)?Qt\.EditRole', r'QtCore.Qt.ItemDataRole.EditRole'),
    (r'(QtCore\.)?Qt\.DisplayRole', r'QtCore.Qt.ItemDataRole.DisplayRole'),
    (r'(QtCore\.)?Qt\.DisplayRole', r'QtCore.Qt.ItemDataRole.DisplayRole'),
    (r'(QtCore\.)?Qt\.Horizontal', r'QtCore.Qt.Orientation.Horizontal'),

    # Image Formats
    (r'QImage\.Format_', r'QImage.Format.Format_'),
    (r'(QtCore\.)?Qt\.white', r'QtCore.Qt.GlobalColor.white'),
    (r'(QtCore\.)?Qt\.red', r'QtCore.Qt.GlobalColor.red'),
    (r'(QtCore\.)?Qt\.blue', r'QtCore.Qt.GlobalColor.blue'),
    (r'(QtCore\.)?Qt\.darkBlue', r'QtCore.Qt.GlobalColor.darkBlue'),
    (r'(QtCore\.)?Qt\.black', r'QtCore.Qt.GlobalColor.black'),
    (r'(QtCore\.)?Qt\.green', r'QtCore.Qt.GlobalColor.green'),
    (r'(QtCore\.)?Qt\.gray', r'QtCore.Qt.GlobalColor.gray'),
    (r'(QtCore\.)?Qt\.lightGray', r'QtCore.Qt.GlobalColor.lightGray'),
    (r'(QtCore\.)?Qt\.yellow', r'QtCore.Qt.GlobalColor.yellow'),
    (r'(QtCore\.)?Qt\.darkGray', r'QtCore.Qt.GlobalColor.darkGray'),
    (r'(QtCore\.)?Qt\.darkRed', r'QtCore.Qt.GlobalColor.darkRed'),
    (r'(QtCore\.)?Qt\.darkGreen', r'QtCore.Qt.GlobalColor.darkGreen'),
    (r'(QtCore\.)?Qt\.darkYellow', r'QtCore.Qt.GlobalColor.darkYellow'),
    (r'(QtCore\.)?Qt\.magenta', r'QtCore.Qt.GlobalColor.magenta'),
    (r'(QtCore\.)?Qt\.transparent', r'QtCore.Qt.GlobalColor.transparent'),
    (r'(QtCore\.)?Qt\.cyan', r'QtCore.Qt.GlobalColor.cyan'),
    (r'(QtCore\.)?Qt\.color0', r'QtCore.Qt.GlobalColor.color0'),
    (r'(QtCore\.)?Qt\.color1', r'QtCore.Qt.GlobalColor.color1'),

    (r'(QtCore\.)?QEvent\.WindowStateChange', r'QtCore.QEvent.Type.WindowStateChange'),

    (r'(QtCore\.)?QSettings\.IniFormat', r'QtCore.QSettings.Format.IniFormat'),

    # SQLtable
    (r'(QtSql\.)?QSqlTableModel\.OnManualSubmit', r'QSqlTableModel.EditStrategy.OnManualSubmit'),
    (r'(QtSql\.)?QSqlTableModel\.OnFieldChange', r'QSqlTableModel.EditStrategy.OnFieldChange'),
    (r'(QtSql\.)?QSqlTableModel\.OnRowChange', r'QSqlTableModel.EditStrategy.OnRowChange'),

    # Render Hints
    (r'QPainter\.Antialiasing', r'QPainter.RenderHint.Antialiasing'),
    (r'QPainter\.TextAntialiasing', r'QPainter.RenderHint.TextAntialiasing'),
    (r'QPainter\.SmoothPixmapTransform', r'QPainter.RenderHint.SmoothPixmapTransform'),
    (r'QPainter\.VerticalSubpixelPositioning', r'QPainter.RenderHint.VerticalSubpixelPositioning'),
    (r'QPainter\.LosslessImageRendering', r'QPainter.RenderHint.LosslessImageRendering'),
    (r'QPainter\.NonCosmeticBrushPatterns', r'QPainter.RenderHint.NonCosmeticBrushPatterns'),

    # ColorRoles
    (r'(QtGui\.)?QPalette\.Window', r'QtGui.QPalette.ColorRole.Window'),
    (r'(QtGui\.)?QPalette\.WindowText', r'QtGui.QPalette.ColorRole.WindowText'),
    (r'(QtGui\.)?QPalette\.Base', r'QtGui.QPalette.ColorRole.Base'),
    (r'(QtGui\.)?QPalette\.AlternateBase', r'QtGui.QPalette.ColorRole.AlternateBase'),
    (r'(QtGui\.)?QPalette\.ToolTipBase', r'QtGui.QPalette.ColorRole.ToolTipBase'),
    (r'(QtGui\.)?QPalette\.ToolTipText', r'QtGui.QPalette.ColorRole.ToolTipText'),
    (r'(QtGui\.)?QPalette\.PlaceholderText', r'QtGui.QPalette.ColorRole.PlaceholderText'),
    (r'(QtGui\.)?QPalette\.Text', r'QtGui.QPalette.ColorRole.Text'),
    (r'(QtGui\.)?QPalette\.Button', r'QtGui.QPalette.ColorRole.Button'),
    (r'(QtGui\.)?QPalette\.ButtonText', r'QtGui.QPalette.ColorRole.ButtonText'),
    (r'(QtGui\.)?QPalette\.BrightText', r'QtGui.QPalette.ColorRole.BrightText'),

    # PenStyle
    (r'Qt\.NoPen', r'Qt.PenStyle.NoPen'),
    (r'Qt\.SolidLine', r'Qt.PenStyle.SolidLine'),
    (r'Qt\.DashLine', r'Qt.PenStyle.DashLine'),
    (r'Qt\.DotLine', r'Qt.PenStyle.DotLine'),
    (r'Qt\.DashDotLine', r'Qt.PenStyle.DashDotLine'),
    (r'Qt\.DashDotDotLine', r'Qt.PenStyle.DashDotDotLine'),
    (r'Qt\.CustomDashLine', r'Qt.PenStyle.CustomDashLine'),

    # BrushStyle
    (r'Qt\.NoBrush', r'Qt.BrushStyle.NoBrush'),
    (r'Qt\.SolidPattern', r'Qt.BrushStyle.SolidPattern'),
    (r'Qt\.TexturePattern', r'Qt.BrushStyle.TexturePattern'),
    (r'Qt\.BDiagPattern', r'Qt.BrushStyle.BDiagPattern'),
    (r'Qt\.CrossPattern', r'Qt.BrushStyle.CrossPattern'),
    (r'Qt\.DiagCrossPattern', r'Qt.BrushStyle.DiagCrossPattern'),

    # QtWidgets QtWidgets.QTableView.EditTrigger.NoEditTriggers
    (r'(QtWidgets\.)?QAbstractItemView\.SelectRows', r'QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows'),
    (r'(QtWidgets\.)?QTableView\.NoEditTriggers', r'QtWidgets.QTableView.EditTrigger.NoEditTriggers'),

    # Classes
    (r'\bQRegExp\b', r'QRegularExpression'),
    (r'\bQDesktopWidget\b', r'QScreen'),  # deprecated in Qt6
]


def process_py_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    original_content = content

    for pattern, repl in PYQT5_TO_PYQT6_IMPORTS + COMMON_REPLACEMENTS:
        content = re.sub(pattern, repl, content)

    if content != original_content:
        backup_path = filepath + '.bak'
        shutil.copy(filepath, backup_path)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Ported: {filepath}")
    else:
        pass
        # print(f"No changes: {filepath}")


def process_ui_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Change XML namespaces or version-specific tags if needed
    content = re.sub(r'PyQt5', 'PyQt6', content)

    if content != original_content:
        backup_path = filepath + '.bak'
        shutil.copy(filepath, backup_path)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated UI file: {filepath}")
    else:
        pass
        # print(f"No changes in UI: {filepath}")


def port_directory(root_dir):
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if filename.endswith('.py'):
                process_py_file(filepath)
            elif filename.endswith('.ui'):
                process_ui_file(filepath)


if __name__ == '__main__':
    project_root = r'./finalcif'
    port_directory(project_root)
