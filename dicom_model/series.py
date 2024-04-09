import gc

import numpy as np
from pydicom.config import logger

from dicom_model.image import Image


class Series(object):
    def __init__(self, dicom_dataset=None):
        self.images = list()
        self.dicom_dataset = dicom_dataset
        self.images.append(Image(dicom_dataset=dicom_dataset))
        self.sorted = False
        self.shape = None

    def __repr__(self):
        try:
            output = f"\t\tSeriesIUID = {self.dicom_dataset.SeriesInstanceUID}:\n"
            for x in self.images:
                output += repr(x)
            return output
        except Exception as e:
            logger.debug("trouble getting Series data", exc_info=e)
            return "\t\tSeriesIUID = None\n"

    def __str__(self):
        try:
            return self.dicom_dataset.SeriesInstanceUID
        except Exception as e:
            logger.debug("trouble getting image SeriesInstanceUID", exc_info=e)
            return "None"

    def __eq__(self, other):
        try:
            return self.dicom_dataset.SeriesInstanceUID == other.dicom_dataset.SeriesInstanceUID
        except Exception as e:
            logger.debug("trouble comparing two Series", exc_info=e)
            return False

    def __ne__(self, other):
        try:
            return self.dicom_dataset.SeriesInstanceUID != other.dicom_dataset.SeriesInstanceUID
        except Exception as e:
            logger.debug("trouble comparing two Series", exc_info=e)
            return True

    def __getattr__(self, name):
        return getattr(self.dicom_dataset, name, None)

    def add_dataset(self, dataset):
        try:
            if self.dicom_dataset.SeriesInstanceUID == dataset.SeriesInstanceUID:
                for x in self.images:
                    if x.SOPInstanceUID == dataset.SOPInstanceUID:
                        logger.debug("Image is already part of this series")
                        break
                else:
                    self.images.append(Image(dicom_dataset=dataset))

            else:
                raise KeyError("Not the same SeriesInstanceUIDs")
        except Exception as e:
            logger.debug("trouble adding image to series", exc_info=e)
            raise KeyError("Not the same SeriesInstanceUIDs")

    #?
    def __sort(self):
        self.images.sort(key=lambda k: getattr(k, "InstanceNumber"))
        self.sorted = True

    def get_pixel_array(self):
        # It's easy if no file or if just a single file
        if len(self.images) == 0:
            return None
        elif len(self.images) == 1:
            ds = self.images[0]
            slice = self.__getPixelDataFromDataset(ds)
            return slice

        # Init data (using what the dicom packaged produces as a reference)
        ds = self.images[0]
        if hasattr(ds, "InstanceNumber") and not self.sorted:
            self.__sort()

        slice = self.__getPixelDataFromDataset(ds)
        if slice is None:
            return slice

        if self.shape is None:
            self.shape = self.find_shape()

        vol = np.zeros(self.shape, dtype=slice.dtype)
        vol[0] = slice

        # Fill volume
        ll = self.shape[0]
        for z in range(1, ll):
            ds = self.images[z]
            pixels = self.__getPixelDataFromDataset(ds)
            if pixels is None:
                continue
            vol[z] = pixels

        # Done
        gc.collect()
        return vol
    
    def __getPixelDataFromDataset(self, ds):
        # Get data
        try:
            data = ds.pixel_array
        except Exception:
            return None

        # Obtain slope and offset
        slope = 1
        offset = 0
        needFloats = False
        needApplySlopeOffset = False
        
        if getattr(ds, "RescaleSlope") != None:
            slope = getattr(ds, "RescaleSlope")
            needApplySlopeOffset = True
        if getattr(ds, "RescaleIntercept") != None:
            offset = getattr(ds, "RescaleIntercept")
            needApplySlopeOffset = True
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
    
    def find_shape(self):
        """Find the expected shape of `dataset.pixel_array` without reading the pixel data.
        The returned shape is a tuple"""
        img = self.images[0]
        shape = getattr(img, "Rows"), getattr(img, "Columns")
        frames = len(self.images) or 1
        if frames > 1:
            shape = (frames,) + shape
        samples = getattr(img, "SamplesPerPixel")
        if samples > 1:
            conf = getattr("PlanarConfiguration")
            if conf == 0:
                shape += (samples,)
            elif conf == 1:
                shape = (samples,) + shape
            else:
                raise ValueError(f"Invalid Planar Configuration: '{conf}'")
        return shape
    