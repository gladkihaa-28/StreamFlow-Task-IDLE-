from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
from SQLiteLib import SQLiteModule


class CommandsWindow(QDialog):
    def __init__(self, commands):
        super().__init__()
        try:
            uic.loadUi("./Task/QTs/GeneratedCommands.ui", self)
        except:
            uic.loadUi(".\\Task\\QTs\\GeneratedCommands.ui", self)
        self.commands.setPlainText("\n".join(commands))
        self.close_button.clicked.connect(self.close)

    def close(self):
        self.hide()


class PushWindow(QDialog):
    def __init__(self):
        super().__init__()
        try:
            uic.loadUi("./Task/QTs/PushWindow.ui", self)
        except:
            uic.loadUi(".\\Task\\QTs\\PushWindow.ui", self)
        self.pushButton.clicked.connect(self.push)

    def push(self):
        try:
            commands = []
            commit = self.commit_input.toPlainText().replace(" ", "")
            name = self.name_input.toPlainText().replace(" ", "")
            email = self.email_input.toPlainText().replace(" ", "")
            url = self.url_input.toPlainText().replace(" ", "")
            self.AddToBase([name, email, url])
            commands.append("git init")
            commands.append(f'git config --global user.name "{name}"')
            commands.append(f'git config --global user.email "{email}"')
            commands.append("git reset")
            commands.append("git add *")
            commands.append(f'git commit -m "{commit}"')
            commands.append("git branch -M main.exe")
            commands.append(f"git remote add origin {url}")
            commands.append("git push -u origin main.exe")
            self.commands_window = CommandsWindow(commands)
            self.commands_window.show()
        except:
            pass
        self.hide()

    def AddToBase(self, values):
        try:
            lib = SQLiteModule("./Task/users.db")
        except:
            lib = SQLiteModule(".\\Task\\users.db")
        lib.add(values)