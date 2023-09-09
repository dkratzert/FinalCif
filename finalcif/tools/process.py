import sys, os
import time
import threading
from pathlib import Path

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import QProcess, QIODevice, QTimer, QTime


class ProcessWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.text_widget = QTextEdit()
        layout.addWidget(self.text_widget)

        self.button = QPushButton("Run QProcess")
        layout.addWidget(self.button)

        self.time_label = QLabel()
        layout.addWidget(self.time_label)

        self.setLayout(layout)

        self.button.clicked.connect(self.run_process)
        self.process = None
        self.stop_monitor = False

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

    def update_time(self):
        current_time = QTime.currentTime()
        time_text = current_time.toString("hh:mm:ss")
        self.time_label.setText(f"Current Time: {time_text}")

    def run_process(self):
        self.text_widget.clear()
        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.on_ready_read)
        Path("tests/examples/work/cu_BruecknerJK_153F40_0m.chk").unlink(missing_ok=True)
        self.process.start("platon", ["-U",
                                      "tests/examples/work/cu_BruecknerJK_153F40_0m.cif"])
        threading.Thread(target=self.monitor_output_log).start()

    def on_ready_read(self):
        output = self.process.readAllStandardOutput().data().decode()
        self.text_widget.append(output)

    def monitor_output_log(self):
        while not self.stop_monitor:
            try:
                with open("tests/examples/work/cu_BruecknerJK_153F40_0m.chk", "r") as log_file:
                    content = log_file.read()
                    if '#                                                                              *' in content:
                        self.stop_program()
            except FileNotFoundError:
                pass
            time.sleep(1)

    def stop_program(self):
        print('# Stopping Platon!')
        self.stop_monitor = True
        if self.process and self.process.state() == QProcess.Running:
            self.process.terminate()
        #app.quit()


app = QApplication(sys.argv)
window = QMainWindow()
window.setWindowTitle("QProcess Example")

process_widget = ProcessWidget()
window.setCentralWidget(process_widget)

window.show()

sys.exit(app.exec_())
