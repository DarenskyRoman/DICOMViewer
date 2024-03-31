from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QGraphicsScene,
    QGraphicsPixmapItem
)
from PyQt6.QtGui import QImage, QPixmap
from PyQt6 import uic
from qimage2ndarray import array2qimage

import logic

class ImagesManipulator():
    def __init__(self, view, slider, images):
        self.scene = QGraphicsScene()
        self.view = view
        self.slider = slider
        self.image_item = QGraphicsPixmapItem()
        self.images = self.setImages(images)

        self.view.setScene(self.scene)
        self.scene.addItem(self.image_item)
        #self.view.centerOn(self.image_item)
        self.slider.setMinimum(0)
        self.slider.setMaximum(len(self.images) - 1)

        self.slider.valueChanged.connect(self.update_image)
        self.update_image(0)

    def setImages(self, images):
        return [array2qimage(image, normalize=True) for image in images]

    def update_image(self, value):
        try:
            self.image_item.setPixmap(QPixmap.fromImage(self.images[value]))

        except IndexError:
            print("Error: No image at index", value)
    

class UI(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi("silly.ui", self)
        
        self.openFile.triggered.connect(self.fileSearch)
        self.seriesList.itemDoubleClicked.connect(self.seriesSelection)

    def seriesSelection(self):

        if hasattr(self, "axialImagesShow"):
            del self.axialImagesShow

        index = self.seriesList.currentRow()
        slices = logic.getPixelsForSerie(self.series[index])
        del index

        self.axialImagesShow = ImagesManipulator(self.axialGraphicsView, self.axialSlider, slices)

    def fileSearch(self):
        dir = QFileDialog.getExistingDirectory(caption="Select directory")

        if self.seriesList != 0:
            self.seriesList.clear()

        self.series = logic.read(dir)

        i = 1

        for serieDescription in self.series:
            self.seriesList.addItem(f"{i} {serieDescription.description}")
            i += 1

        del i

if __name__ == "__main__": 

    app = QApplication([])
    window = UI()
    window.show()
    app.exec()
