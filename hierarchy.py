import os
import gc

import pydicom
from pydicom.uid import UID
import numpy as np

from dicom_model.patient import Patient


# file = "DICOM/19061421/00000447"

# ds = pydicom.dcmread(file, force=True)
# ds.file_meta.TransferSyntaxUID = UID("1.2.840.10008.1.2.1")

def __files_walk(start_path):
    list = []
    for root, dirs, files in os.walk(start_path):
        for file in files:
            if file == "DICOMDIR":
                continue
            list.append(os.path.join(root, file))
    return list


def __validate(file):
    if not hasattr(file, "Modality"):
        return False
    if not hasattr(file, "SOPClassUID"):
        return False
    if not hasattr(file, "StudyInstanceUID"):
        return False
    if not hasattr(file, "SeriesInstanceUID"):
        return False
    if not hasattr(file, "SOPInstanceUID"):
        return False
    
    return True


def __tsUID_standart(file):
    if not hasattr(file.file_meta, "TransferSyntaxUID"):
        file.file_meta.TransferSyntaxUID = UID("1.2.840.10008.1.2")
    return file


def _getPixelDataFromDataset(ds):
    # Get original element
    el = ds['PixelData']

    # Get data
    data = ds.pixel_array

    # Remove data (mark as deferred)
    ds['PixelData'] = el
    del ds._pixel_array

    # Obtain slope and offset
    slope = 1
    offset = 0
    needFloats = False
    needApplySlopeOffset = False
    if 'RescaleSlope' in ds:
        needApplySlopeOffset = True
        slope = ds.RescaleSlope
    if 'RescaleIntercept' in ds:
        needApplySlopeOffset = True
        offset = ds.RescaleIntercept
    if int(slope) != slope or int(offset) != offset:
        needFloats = True
    if not needFloats:
        slope, offset = int(slope), int(offset)

    # Apply slope and offset
    if needApplySlopeOffset:

        # Maybe we need to change the datatype?
        if data.dtype in [np.float32, np.float64]:
            pass
        elif needFloats:
            data = data.astype(np.float32)
        else:
            # Determine required range
            minReq, maxReq = data.min(), data.max()
            minReq = min(
                [minReq, minReq * slope + offset, maxReq * slope + offset])
            maxReq = max(
                [maxReq, minReq * slope + offset, maxReq * slope + offset])

            # Determine required datatype from that
            dtype = None
            if minReq < 0:
                # Signed integer type
                maxReq = max([-minReq, maxReq])
                if maxReq < 2 ** 7:
                    dtype = np.int8
                elif maxReq < 2 ** 15:
                    dtype = np.int16
                elif maxReq < 2 ** 31:
                    dtype = np.int32
                else:
                    dtype = np.float32
            else:
                # Unsigned integer type
                if maxReq < 2 ** 8:
                    dtype = np.uint8
                elif maxReq < 2 ** 16:
                    dtype = np.uint16
                elif maxReq < 2 ** 32:
                    dtype = np.uint32
                else:
                    dtype = np.float32

            # Change datatype
            if dtype != data.dtype:
                data = data.astype(dtype)

        # Apply slope and offset
        try:
            data *= slope
            data += offset
        except:
            data = data * slope
            data = data + offset

    # Done
    return data


def __sorting(files):
    return

def read_files(path, force=False):
    files = [pydicom.dcmread(file, force=force) for file in __files_walk(path)]
    files = [__tsUID_standart(file) for file in files if __validate(file)]

    dcmh = DicomHierarchy()
    for f in files:
        dcmh.add_patient(f)

    del files

    return dcmh

class DicomHierarchy:
    def __init__(self):
        self.patients = []

    def add_patient(self, data):
        for p in self.patients:
            try:
                p.add_dataset(data)
            except Exception as e:
                pass
            else:
                break
        else:
            self.patients.append(Patient(dicom_dataset=data))

    def get_tree(self):
        tree = []
        i = 0
        for p in self.patients:
            birthdate = getattr(p, "PatientBirthDate")
            birthdate = birthdate[6:8] + '.' + birthdate[4:6] + '.' + birthdate[:4]
            tree.append({"PatientInfo": f"Name: {getattr(p, 'PatientName')}, Birthdate: {birthdate}, Sex: {getattr(p, 'PatientSex')}", "Studies": []})
            
            j = 0
            for st in p.studies:
                studyInfo = f"Study Date: {getattr(st, 'StudyDate')}, Reffering Physician: {getattr(st, 'RefferingPhysician')}"
                tree[i]["Studies"].append({"StudyInfo": studyInfo, "Series": []})

                for s in st.series:
                    _ = s.images[0]
                    serieInfo = f"Modality: {getattr(_, 'Modality')}, Body Part: {getattr(_, 'BodyPartExamined')}, Description: {getattr(_, 'SeriesDescription')}"
                    tree[i]["Studies"][j]["Series"].append(serieInfo)
                
                j += 1

            i += 1
        return tree

    def get_pixels_data(self, indexes):
        p = self.patients[indexes[0]]
        st = p.studies[indexes[1]]
        s = st.series[indexes[2]]
        
        singlePlane = False
        if getattr(s.images[0], "Modality") != "CT":
            singlePlane = True
        return (singlePlane, s.get_pixel_array())

if __name__=="__main__":

    read_files("DICOM", force=True)