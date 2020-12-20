import os
from django.db import models
from django.contrib.auth.models import User
from eoscan_app.settings import MEDIA_ROOT


class AdvUser(User):
    company = models.ForeignKey("Company", on_delete=models.SET_NULL,
                                null=True, blank=True,
                                verbose_name='Компания')
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Дата регистрации')
    updated = models.DateTimeField(auto_now=True,
                                   null=True, blank=True,
                                   verbose_name='Дата обновления данных')
    count = models.FloatField(default=0.0, verbose_name='Состояние счета')
    memory_limit = models.FloatField(null=True, blank=True,
                                     verbose_name='Лимит хранилища')
    tools_list = models.ManyToManyField("Tool", blank=True,
                                        verbose_name='Список доступных '
                                                     'моделей')

    def __str__(self):
        return f"{self.username}"


class Company(models.Model):
    name = models.CharField(max_length=128, verbose_name='Название')
    inn = models.BigIntegerField(blank=True, null=True,
                                 verbose_name='ИНН')

    def __str__(self):
        return self.name


class Order(models.Model):

    img = models.ImageField(null=True, blank=True, upload_to='upload_images/',
                            verbose_name='Изображение', width_field='width',
                            height_field="height")
    tool = models.ForeignKey("Tool", on_delete=models.SET_NULL,
                             null=True, blank=True,
                             verbose_name='Модель')
    size = models.FloatField(null=True, blank=True,
                             verbose_name='Размер файла')
    height = models.IntegerField(null=True, blank=True,
                                 verbose_name='Высота')
    width = models.IntegerField(null=True, blank=True,
                                verbose_name='Ширина')
    extension = models.CharField(max_length=32, null=True, blank=True,
                                 verbose_name='Расширение')
    # в методе save написать проверку на geodata
    string_geodata = models.TextField(null=True, blank=True,
                                      verbose_name='Геоданные файла')
    # rename
    inputed_geodata = models.TextField(null=True, blank=True,
                                      verbose_name='Ввести геоданные '
                                                   'файла вручную')
    user = models.ForeignKey(AdvUser, on_delete=models.SET_NULL,
                             null=True, blank=True,
                             verbose_name='Пользователь')
    process_inputed_geodata = models.BooleanField(default=False,
                                         verbose_name='Обработать '
                                                      'введенные геоданные')
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Дата создания')
    discount = models.FloatField(default=0.0, verbose_name='% скидки')
    source_path = models.CharField(max_length=526, null=True, blank=True,
                                       verbose_name='Путь до сырья')
    result_folder_path = models.CharField(max_length=526, null=True,
                                          blank=True, verbose_name=
                                          'Путь до папки для сохранения '
                                          'результата')
    result_path = models.CharField(max_length=526, null=True, blank=True,
                                       verbose_name='Путь до результата')
    start_datetime = models.DateTimeField(null=True, blank=True,
                                          verbose_name='Дата начала обработки')
    finish_datetime = models.DateTimeField(null=True, blank=True,
                                           verbose_name='Дата окончания '
                                                        'обработки')
    task_id = models.CharField(max_length=64, blank=True,
                               null=True, verbose_name='Задача')
    task_status = models.CharField(max_length=64, blank=True,
                                   null=True, verbose_name='Статус выполнения')
    priority = models.SmallIntegerField(default=0, verbose_name='Приоритет')
    description = models.TextField(null=True, blank=True,
                                      verbose_name='Описание изображения')

    def __str__(self):
        return f"Order #{self.id} ({self.created})"

    def save(self):
        super(Order, self).save()
        raw_file_path = os.path.join(MEDIA_ROOT, self.img.name)
        self.source_path = raw_file_path
        self.size = os.path.getsize(raw_file_path)
        self.extension = self.img.name.split('.')[-1]
        self.result_folder_path = os.path.join(MEDIA_ROOT, 'recognized_images',
                                               str(self.id))
        super(Order, self).save()


class Tool(models.Model):
    name = models.CharField(max_length=256, default='No-name tool',
                            verbose_name='Название')
    description = models.TextField(null=True, blank=True,
                                   verbose_name='Описание')
    avatar = models.ImageField(null=True, blank=True, upload_to='media/',
                               verbose_name='Аватар')
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, null=True, blank=True,
                                   verbose_name='Дата изменения')
    tool_type = models.ForeignKey("ToolType", on_delete=models.SET_NULL,
                                  null=True, blank=True,
                                  verbose_name='Тип модели')
    weights = models.FileField(null=True, blank=True, upload_to='',
                               verbose_name='Файл весов')
    price = models.FloatField(default=0.0, verbose_name='Стоимость')
    origin_path = models.CharField(max_length=526, null=True, blank=True,
                                       verbose_name='Директория из')
    result_path = models.CharField(max_length=526, null=True, blank=True,
                                       verbose_name='Директория в')

    def __str__(self):
        return self.name


class ToolType(models.Model):
    name = models.CharField(max_length=256, default='No-name tool type',
                            verbose_name='Название')
    proc_geodata = models.BooleanField(default=False,
                                       verbose_name='Работа с геоданными')

    def __str__(self):
        return self.name
