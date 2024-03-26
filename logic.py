from pydicom import dcmread
from pathlib import Path
import numpy as np

def read(dir):
    dir = Path(dir)
    volumes = {}
    bodyParts = set()
    for patient_dir in dir.iterdir():
        if patient_dir.is_dir():
            for file in patient_dir.iterdir():
                try:
                    dicom_file = dcmread(file, force=True)
                    body_part = dicom_file.get('BodyPartExamined')
                    if body_part not in bodyParts:
                        bodyParts.add(body_part)
                        volumes[f"{body_part}"] = []

                    pixel_data = dicom_file.get('PixelData')

                    if pixel_data is None:
                        print("Секция Pixel Data отсутствует в файле:", file)
                        continue

                    pixel_array = np.frombuffer(pixel_data, dtype=np.uint16)

                    volumes[f"{body_part}"].append(pixel_array.reshape(int(dicom_file.Rows), int(dicom_file.Columns)))

                except Exception as e:
                    print(f"Ошибка при обработке файла {file}: {e}")
    return volumes
