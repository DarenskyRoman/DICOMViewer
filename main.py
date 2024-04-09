from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QGraphicsScene,
    QGraphicsPixmapItem,
    QTreeWidgetItem
)
from PyQt6.QtGui import QImage, QPixmap
from PyQt6 import uic
from qimage2ndarray import array2qimage

import logic
import popups


class ImagesManipulator():
    def __init__(self, view, slider, images):
        self.scene = QGraphicsScene()
        self.view = view
        self.slider = slider
        self.image_item = QGraphicsPixmapItem()
        self.images = self.setImages(images)

        self.view.setScene(self.scene)
        self.scene.addItem(self.image_item)
        self.view.centerOn(self.image_item)
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
        popups.Config.UI = self
        
        self.openFile.triggered.connect(lambda: self.fileSearch(0))
        self.openDirectory.triggered.connect(lambda: self.fileSearch(1))
        self.treeWidget.itemDoubleClicked.connect(self.seriesSelection)

    def get_indexes(self, item):        
        st = item.parent()
        if st is None:
            return None
        
        p = item.parent().parent()
        if p is None:
            return None

        patient_index = self.treeWidget.indexOfTopLevelItem(p)
        study_index = p.indexOfChild(st)
        serie_index = st.indexOfChild(item)

        return (patient_index, study_index, serie_index)

    def seriesSelection(self, item):
        indexes = self.get_indexes(item)
        if indexes is None:
            return
        
        if hasattr(self, "axialImagesShow"):
            del self.axialImagesShow

        slices = logic.getPixelsForSerie(self.dcmh, indexes)
        del indexes

        if type(slices) == popups.ErrorPop:
            slices.window.exec()
            del slices
        else:
            self.axialImagesShow = ImagesManipulator(self.axialGraphicsView, self.axialSlider, slices[1])
            del slices

    def fileSearch(self, searchType):
        if searchType == 0:
            data = QFileDialog.getOpenFileName(caption="Select file")[0]
        elif searchType == 1:
            data = QFileDialog.getExistingDirectory(caption="Select directory")

        if data != "":
            self.dcmh = logic.read(data, force=True)
        
            if type(self.dcmh) == popups.ErrorPop:
                self.dcmh.window.exec()
                del self.dcmh
            else:
                if self.treeWidget != 0:
                    self.treeWidget.clear()

                self.drawTree(self.dcmh.get_tree())

    def drawTree(self, tree_data):
        for p in tree_data:
            patient = QTreeWidgetItem()
            patient.setText(0, p["PatientInfo"])

            for st in p["Studies"]:
                study = QTreeWidgetItem(patient)
                study.setText(0, st["StudyInfo"])

                for s in st["Series"]:
                    serie = QTreeWidgetItem(study)
                    serie.setText(0, s)
                    study.addChild(serie)
                
                patient.addChild(study)

            self.treeWidget.addTopLevelItem(patient)
        

if __name__ == "__main__": 

    app = QApplication([])
    window = UI()
    window.show()
    app.exec()
