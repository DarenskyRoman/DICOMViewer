from pydicom import dcmread
from pathlib import Path
import numpy as np

def read(dir):
    dir = Path(dir)
    volumes = {}
    for patient_dir in dir.iterdir():
        if patient_dir.is_dir():
            for file in patient_dir.iterdir():
                try:
                    dc = dcmread(file, force=True)
                    body_part = dc.get('BodyPartExamined')
                    if body_part not in volumes.keys():
                        volumes[f"{body_part}"] = []

                    pixel_data = dc.get('PixelData')

                    if pixel_data is None:
                        print("Pixel Data not found:", file)
                        continue

                    pixel_array = np.frombuffer(pixel_data, dtype=np.uint16)
                    volumes[f"{body_part}"].append(pixel_array.reshape(int(dc.Rows), int(dc.Columns)))

                except Exception as e:
                    print(f"Error with file {file}: {e}")
    return volumes
