import os
from PyQt5.QtCore import QThread, pyqtSignal, QProcess


res = ""


class CodeExecutor(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, code, selected_file, current_dir, result):
        super().__init__()
        self.code = code
        self.selected_file = selected_file
        self.current_dir = current_dir
        self.result = result
        self.process = QProcess()

    def run(self):
        global res
        try:
            if self.selected_file is not None and ".tsk" in self.selected_file:
                file_name = f"{self.current_dir}/{self.selected_file.replace(' ', '')}"
            else:
                file_name = None

            if file_name:
                path = os.path.abspath(file_name)
                win_path = path.replace("/", "\\")
                lin_path = path.replace("\\", "/")
                try:
                    command = f"python ./Task/task_main.py {lin_path}"
                    self.process.start(command)
                    self.process.waitForFinished()
                    res = self.process.readAllStandardOutput().data().decode()
                    self.finished.emit(res)
                except:
                    command = f'python .\\Task\\task_main.py {win_path}'
                    print(command)
                    self.process.start(command)
                    self.process.waitForFinished()
                    res = self.process.readAllStandardOutput().data().decode()
                    self.finished.emit(res)
        except Exception as e:
            self.error.emit(f"Ошибка выполнения кода: {e}")