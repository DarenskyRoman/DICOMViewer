import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt6 import uic
import logic
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, width, height):
        self.fig = Figure(figsize=(width, height))
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)

    def addSlider(self, valmax):
        ax = self.fig.add_axes([0.25, 0.1, 0.65, 0.03])
        self.slider = Slider(ax=ax,
                            label="Slice",
                            valmin=0,
                            valinit=0,
                            valstep=1,
                            valmax=valmax)


class UI(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi("silly.ui", self)
        
        self.axialCanvas = MplCanvas(1, 1)
        axialToolbar = NavigationToolbar2QT(self.axialCanvas, self)
        self.axialLayout.addWidget(self.axialCanvas)
        self.axialLayout.addWidget(axialToolbar)

        self.sagittalCanvas = MplCanvas(1, 1)
        sagittalToolbar = NavigationToolbar2QT(self.sagittalCanvas, self)
        self.sagittalLayout.addWidget(self.sagittalCanvas)
        self.sagittalLayout.addWidget(sagittalToolbar)

        self.coronalCanvas = MplCanvas(1, 1)
        coronalToolbar = NavigationToolbar2QT(self.coronalCanvas, self)
        self.coronalLayout.addWidget(self.coronalCanvas)
        self.coronalLayout.addWidget(coronalToolbar)

        
        self.openFile.triggered.connect(self.fileSearch)
        self.bodyPartsList.itemDoubleClicked.connect(self.bodyPartSelection)


    def bodyPartSelection(self, bodyPart):
        self.axialCanvas.axes.cla()
        #self.sagittalCanvas.clear()
        #self.coronalCanvas.clear()

        slices = self.volumes[f"{bodyPart.text()}"]
        
        self.axialCanvas.addSlider(len(slices)-1)
        self.axialCanvas.slider.on_changed(lambda val: self.plotAxialSLice(val, slices))
        self.plotAxialSLice(0, slices)
        #self.axialLayout.addWidget(slider)

    def plotAxialSLice(self, val, slices):
        self.axialCanvas.axes.imshow(slices[val], cmap=plt.cm.bone)
        self.axialCanvas.draw()

    def fileSearch(self):
        dir = QFileDialog.getExistingDirectory(caption="Select directory")
        self.volumes = logic.read(dir)
        for bodyPart in self.volumes.keys():
            self.bodyPartsList.addItem(f"{bodyPart}")

if __name__ == "__main__": 

    app = QApplication([])
    window = UI()
    window.show()
    app.exec()
