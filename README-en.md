# DICOMViewer

An application for viewing computer tomograms and radiographs in the  DICOM format (.dcm).

## Features

With this application you can view images of medical researches.

Available types of researches to view:

- #### Computed tomography (CT)

![ct-1](/img/ct-1.png)

- #### Radiography (CR)

![cr-1](/img/cr-1.png)

The application hasn't been tested for other types of researches.

### Interaction with the image

To select different slices in each plane simply move the slider located under the image.

It's possible to zoom in/out and move the image:

![ct-2](/img/ct-2.png)

![cr-2](/img/cr-2.png)

## Installation

1. Clone the repository to any folder on your computer:

    ```bash
    git clone https://github.com/DarenskyRoman/DICOMViewer.git
    ```

2. Go to the application folder:

    ```bash
    cd DICOMViewer
    ```

3. Install the necessary dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4.  Launch the application:

    ```bash
    python main.py
    ```