# -*- coding: utf-8 -*-
"""
Этот код представляет собой определение пользовательского поля
модели Django под названием WEBPField, которое используется
для хранения изображений в формате WEBP.
 Данный код также использует библиотеку Pillow для конвертации
 изображений в формат WEBP.
"""
import io

from PIL import Image
from django.core.files.base import ContentFile
from django.db import models
from django.db.models.fields.files import ImageFieldFile


class WEBPFieldFile(ImageFieldFile): #Pillow - переформатирует изображения в формат вебп для оптимизации загрузки изображений
    """
    Класс-наследник ImageFieldFile для обработки полей изображений в
    формате WEBP.
    """
    def save(self, name, content, save=True):
        """
        Переопределенный метод save для сохранения изображения в формате WEBP.
        """
        content.file.seek(0)
        image = Image.open(content.file)
        image_bytes = io.BytesIO()
        image.save(fp=image_bytes, format="WEBP")
        image_content_file = ContentFile(content=image_bytes.getvalue())
        super().save(name, image_content_file, save)


class WEBPField(models.ImageField):
    """
    Пользовательское поле модели Django для хранения изображений в формате WEBP.
    """
    attr_class = WEBPFieldFile