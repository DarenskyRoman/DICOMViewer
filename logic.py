from pydicom import dcmread

def read(file):
    try:
        return dcmread(file)
    except Exception:
        return
