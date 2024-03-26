import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QListWidgetItem
from PyQt6 import uic
import numpy as np
import logic


class UI(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi("silly.ui", self)
        
        self.axialFigure = plt.figure()  
        self.axialCanvas = FigureCanvas(self.axialFigure)
        self.axialToolbar = NavigationToolbar(self.axialCanvas, self)
        self.axialLayout.addWidget(self.axialCanvas)
        self.axialLayout.addWidget(self.axialToolbar)

        self.sagittalFigure = plt.figure()
        self.sagittalCanvas = FigureCanvas(self.sagittalFigure)
        self.sagittalToolbar = NavigationToolbar(self.sagittalCanvas, self)
        self.sagittalLayout.addWidget(self.sagittalCanvas)
        self.sagittalLayout.addWidget(self.sagittalToolbar)

        self.coronalFigure = plt.figure()
        self.coronalCanvas = FigureCanvas(self.coronalFigure)
        self.coronalToolbar = NavigationToolbar(self.coronalCanvas, self)
        self.coronalLayout.addWidget(self.coronalCanvas)
        self.coronalLayout.addWidget(self.coronalToolbar)

        
        self.openFile.triggered.connect(self.fileSearch)
        self.bodyPartsList.itemDoubleClicked.connect(self.bodyPartSelection)


    def bodyPartSelection(self, bodyPart):
        self.axialFigure.clear()
        #self.sagittalFigure.clear()
        #self.coronalFigure.clear()
        slices = self.volumes[f"{bodyPart.text()}"]
        
        self.axAxial = self.axialFigure.add_subplot(111)
        self.axAxial.imshow(slices[0], cmap=plt.cm.bone)
        self.axialCanvas.draw()
        #self.axSagitall = self.sagittalFigure.add_subplot()
        #axCoronal = self.coronalFigure.add_subplot()
        
        self.axialSlider = Slider(ax=self.axialFigure.add_subplot(111),
                                  label="Slice",
                                  valmin=0,
                                  valinit=0,
                                  valstep=1,
                                  valmax=len(slices)-1)
        self.axialSlider.on_changed(lambda val: self.plotAxialSLice(val, slices))

    def plotAxialSLice(self, val, slices):
        self.axAxial.imshow(slices[val], cmap=plt.cm.bone)
        self.axialCanvas.draw()

    def fileSearch(self):
        dir = QFileDialog.getExistingDirectory(caption="Select directory")
        self.volumes = logic.read(dir)
        for bodyPart in self.volumes.keys():
            self.bodyPartsList.addItem(f"{bodyPart}")

        # try:
        #     self.figure.clear()
    
        #     ax = self.figure.add_subplot()
        #     ax.imshow(filedata.pixel_array, cmap=plt.cm.bone)
            
        #     self.canvas.draw()

        # except Exception:
        #     self.errorWindow("Cannot open this file")

    def errorWindow(self, text):
        QMessageBox.critical(self, "Error", text)


app = QApplication([])
window = UI()
window.show()
app.exec()
