from PyQt6.QtWidgets import QMessageBox 
from main import UI
from dataclasses import dataclass



@dataclass
class Config:
    UI: UI

class ErrorPop():
    def __init__(self, ok_btn=False, msg="Ooh!"):
        self.window = QMessageBox(Config.UI)
        self.window.setIcon(QMessageBox.Icon.Warning)
        self.window.setWindowTitle("Oops!")
        self.window.setText(msg)
        if ok_btn:
            self.window.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.window.setStandardButtons(QMessageBox.StandardButton.Cancel)
