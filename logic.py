from pydicom_series import read_files


def read(dir):
    
    try:
        return read_files(dir, showProgress=False, readPixelData=False, force=True)
    
    except Exception as e:
        print(f"Can't read data properly: {e}")


def getPixelsForSerie(data):

    try:
        return data.get_pixel_array()
    except Exception as e:
        print(f"Can't get images data: {e}")