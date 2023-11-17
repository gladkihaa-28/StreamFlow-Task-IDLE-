from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QListWidgetItem
from PyQt5 import uic
from CodeRunner import CodeExecutor
from Push import PushWindow
import sys
import os


class TaskIDE(QMainWindow, QWidget):
    def __init__(self):
        super().__init__()
        try:
            try:
                uic.loadUi("./Task/QTs/window.ui", self)
            except:
                uic.loadUi(".\\Task\\QTs\\window.ui", self)
        except:
            try:
                uic.loadUi("./QTs/window.ui", self)
            except:
                uic.loadUi(".\\QTs\\window.ui", self)
        self.current_dir = ""
        self.populate_file_list()
        self.file_list.itemClicked.connect(self.load_file_content)
        self.run_button.clicked.connect(self.run_code)
        self.remove_button.clicked.connect(self.remove_file)
        self.push_button.clicked.connect(self.push_code)
        self.create_button.clicked.connect(self.create_file)
        self.selected_file = None
        self.active_executors = []


    def populate_file_list(self):
        self.file_list.clear()
        self.file_list.addItem("\n")
        try:
            self.current_dir = "./"
            filenames = os.listdir(self.current_dir)
        except:
            self.current_dir = ".\\"
            filenames = os.listdir(self.current_dir)
        for filename in filenames:
            if "." in str(filename) and ".git" not in str(filename) and "output" not in str(filename) and "idea" not in str(filename):
                item = QListWidgetItem(filename)
                self.file_list.addItem(" " * (15 - len(item.text())) + item.text())
        self.file_list.addItem("\n")

    def load_file_content(self, item):
        code = self.code_editor.toPlainText().strip()
        if code != "" and self.selected_file is not None and "." in str(self.selected_file):
            try:
                with open(f"{self.current_dir}/{self.selected_file}".replace(" ", ""), 'w') as file:
                    file.write(code)
            except:
                with open(f"{self.current_dir}\\{self.selected_file}".replace(" ", ""), 'w') as file:
                    file.write(code)
        selected_file = item.text()
        self.selected_file = selected_file
        try:
            if self.selected_file is not None and "." in str(self.selected_file):
                try:
                    with open(f"{self.current_dir}/{selected_file}".replace(" ", ""), 'r') as file:
                        file_code = file.read()
                except:
                    with open(f"{self.current_dir}\\{selected_file}".replace(" ", ""), 'r') as file:
                        file_code = file.read()
                code = "\n"
                for line in file_code.split("\n"):
                    code += line + "\n"
                self.code_editor.setPlainText("\n" + code)
            else:
                self.code_editor.setPlainText("\n")

        except Exception as e:
            print(f"Ошибка загрузки файла: {e}")

    def run_code(self):
        code = self.code_editor.toPlainText()
        inputs = self.inputs.toPlainText().split("\n")
        lines = code.split("\n")
        new_lines = []
        i = 0
        for line in lines:
            if not line.startswith("#"):
                if "input()" in line:
                    new_lines.append(line.replace("input()", inputs[i]))
                    i += 1
                elif line != "":
                    new_lines.append(line)

        code = "\n" + "\n".join(new_lines) + "\n"
        self.code_editor.setPlainText(code)
        code = self.code_editor.toPlainText()

        self.result.setPlainText("")
        selected_file = self.selected_file

        code_executor = CodeExecutor(code, selected_file, self.current_dir, self.result)
        code_executor.finished.connect(self.handle_result)
        code_executor.error.connect(self.handle_error)
        self.active_executors.append(code_executor)
        code_executor.start()

    def handle_result(self, result):
        self.result.setPlainText("    " + result)

    def handle_error(self, error):
        self.result.setPlainText(error)

    def closeEvent(self, event):
        for code_executor in self.active_executors:
            code_executor.quit()
            code_executor.wait()
        event.accept()


    def push_code(self):
        self.push_window = PushWindow()
        self.push_window.show()

    def create_file(self):
        names = self.file_edit.toPlainText().replace(" ", "").split("\n")
        names = [el for el in names if el]
        self.file_edit.setPlainText("      \n      ")
        for name in names:
            try:
                open(f"{name}", "w")
            except:
                open(f"{name}", "w")
        self.populate_file_list()

    def remove_file(self):
        path = self.selected_file.replace(" ", "")
        if "/" in path:
            os.remove(path)
        else:
            os.remove(path)
        self.selected_file = None
        self.populate_file_list()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TaskIDE()
    ex.show()
    sys.exit(app.exec_())