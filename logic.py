from hierarchy import read_files
from popups import ErrorPop


def read(dir, force):
    try:
        return read_files(dir, force=force)
    except Exception:
        return ErrorPop(msg="Can't read this data")


def getPixelsForSerie(data, indexes):
    try:
        return data.get_pixels_data(indexes)
    except Exception:
        return ErrorPop(msg="Can't get images data")