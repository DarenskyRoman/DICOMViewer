import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt6 import uic
from logic import read


class UI(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi("silly.ui", self)
        
        self.figure = plt.figure()
  
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
          
        self.imageLayout.addWidget(self.toolbar)
        self.imageLayout.addWidget(self.canvas)

        self.openFile.triggered.connect(self.fileSearch)


    def fileSearch(self):
        file = QFileDialog.getOpenFileName(caption = "Open file", filter="DICOM files (*.dcm)")
        filedata = read(file[0])

        try:
            self.figure.clear()
    
            ax = self.figure.add_subplot()
            ax.imshow(filedata.pixel_array, cmap=plt.cm.bone)
            
            self.canvas.draw()

        except Exception:
            self.errorWindow("Cannot open this file")

    def errorWindow(self, text):
        QMessageBox.critical(self, "Error", text)


app = QApplication([])
window = UI()
window.show()
app.exec()
