# превращает функцию в задачу для celery
from celery import shared_task
from django.core.mail import send_mail
import logging
logger = logging.getLogger(__name__)
from eoscan_app.settings import BASE_DIR, WEIGHT_ROOT
from .processing.preparers import Preparer
from .models import Order, Tool

# стадартные библиотеки
from datetime import datetime
import os
import time
# import glob
# import random

# библиотеки для работы с изображениями
import cv2
# from matplotlib import pyplot as plt

# библиотеки для работы с матрицами и мат.методами
import numpy as np
# from scipy import ndimage

# библиотеки для работы с геоданными
# from pyproj import Proj, transform
# import rasterio as rio
# from osgeo import gdal


@shared_task
def save_orders(user_id):
    logger.info(f"Вызван метод save_orders")
    logger.info(f"par {user_id}")
    orders = Order.objects.select_related('tool', 'tool__tool_type').\
        filter(user__pk=user_id)
    filename = f'media/reports/orders_user_{user_id}.txt'
    with open(filename, 'w', encoding='utf-8') as f:
        for item in orders:
            f.write('Order #' + str(item.pk) + '|' + str(item.tool) + '\n')


@shared_task
def send_mail_task(subject, text_message, email_to):
    time.sleep(5)
    logger.info(f"Вызван метод send_mail_task с "
                f"параметрами:{subject}, {text_message}")
    send_mail(subject=subject,
              message=text_message,
              from_email='some@some.com',
              recipient_list=[email_to],
              fail_silently=False)


@shared_task
def tool_1_task(order_id):
    order = Order.objects.get(pk=order_id)
    tool_id = order.tool.id
    raw_file_path = order.source_path
    extension = order.extension
    datetime_ = datetime.now()
    fn_datetime = datetime_.timestamp()
    order.start_datetime = datetime_
    order.save()

    logger.info(f"fn_datetime:{fn_datetime}")
    user_id = order.user.id
    if not order.result_path:
        fn = '%s.%s.%s.%s' % (fn_datetime, order_id, user_id, extension)
        # текущий таймстемп вида 1593602121.340265 + .номер заказа +
        # .номер пользователя + .расширение вида png
        fn_full = os.path.join(order.result_folder_path, fn)
        order.result_path = fn_full
        order.save()

    # далее сделать условие для выбора размера ядра
    kernel_size = (256, 256)
    prep = Preparer(kernel_size)
    image = cv2.imread(raw_file_path)
    # разрежем изображение на страйды
    img_stride_list = prep.image_cutter([image, image])[0]
    # фиксируем время разрезания изображения
    order.cutter_datetime = datetime.now()
    # получим массив с изначальной (до трансформации по размерам ядра) формой
    form_array = prep.get_form_array([image, image])[0]
    # получим список страйдов с одинаковыми размерами
    # (стандартизованы до размера ядра)
    standart_img_stride_list = prep.standartizator(img_stride_list)
    # сформируем название для файла .npy со стандартизованными страйдами
    # (многомерный массив)
    filename_for_img_rsl = 'img_rsl_' + fn + '.npy'
    # определим путь до папки с распознанными изображениями
    path_for_img_strides = os.path.join(BASE_DIR, 'media', 'strided_images')
    logger.info(f"path_for_img_strides: {path_for_img_strides}")
    # сохраним файл .npy со стандартизованными страйдами (многомерный массив)
    prep.stride_saver(standart_img_stride_list, filename_for_img_rsl,
                      path_for_img_strides)

    from .processing.tools import model_1 as model_
    model = model_(kernel_size)
    model.load_weights(os.path.join(WEIGHT_ROOT, '1.hdf5'))

    # нужно будет передавать third_size
    def test_img_generator(test_imgs, kernel_size, third_size=3):
        """Вспомогательная функция для метода
        predict_generator из tensorflow"""
        for img in range(test_imgs.shape[0]):
            yield test_imgs[img].reshape(1, kernel_size[0],
                                         kernel_size[1], third_size)

    # загружаем наш многомерный массив со страйдами размера ядра
    test_imgs = np.load(
        os.path.join(path_for_img_strides, filename_for_img_rsl)
    )
    # делаем распознавание
    pred = model.predict_generator(test_img_generator(test_imgs, kernel_size),
                                   test_imgs.shape[0])
    # фиксируем время, когда распознавание выполнено
    order.recognizer_datetime = datetime.now()
    # метод img_builder собирает страйды в изображение,
    # находу приводя размер страйдов к оригинальному
    result = prep.img_builder((order.img.height, order.img.width),
                              form_array, pred) * 255.
    # фиксируем время, когда страйды собраны в новое изображение
    order.merger_datetime = datetime.now()
    result = np.atleast_3d(result.reshape((result.shape[0], result.shape[1])))
    # записываем изображение в папку с распознанными изображениями
    try:
        os.mkdir(order.result_folder_path)
    except:
        pass

    try:
        cv2.imwrite(os.path.join(fn_full), result)
        order.finish_datetime = datetime.now()
        order.save()
    except:
        raise Exception
