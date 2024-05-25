# DICOMViewer

[![ru](https://img.shields.io/badge/lang-ru-blue.svg)](https://github.com/DarenskyRoman/DICOMViewer/blob/main/README.md)
[![en](https://img.shields.io/badge/lang-en-pink.svg)](https://github.com/DarenskyRoman/DICOMViewer/blob/main/README.en.md)


Приложение для просмотра компьютерных томограмм и рентгенограмм в формате DICOM (.dcm).

## Возможности

С помощью этого приложения можно просматривать изображения медицинских исследований. 

Доступные типы исследования для просмотра:

- #### Компьютерная томография (КТ, CT)

![ct-1](/img/ct-1.png)

- #### Рентгенография (CR)

![cr-1](/img/cr-1.png)

Работа приложения для других типов исследований не проверялась.

### Взаимодействие с изображением

Для выбора различных срезов в каждой плоскости просто передвиньте ползунок расположенный под  изображением.

Имеется возможность приближения, удаления и перемещения изображения:

![ct-2](/img/ct-2.png)

![cr-2](/img/cr-2.png)

## Установка

1. Клонируйте репозиторий в любую папку на компьютере:

    ```bash
    git clone https://github.com/DarenskyRoman/DICOMViewer.git
    ```

2. Перейдите в папку с приложением:

    ```bash
    cd DICOMViewer
    ```

3. Установите необходимые зависимости:

    ```bash
    pip install -r requirements.txt
    ```

4.  Запустите приложение:

    ```bash
    python main.py
    ```