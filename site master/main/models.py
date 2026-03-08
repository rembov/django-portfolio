from django.db import models

class Service(models.Model):
    """Услуга мастера"""
    name = models.CharField('Название', max_length=200)
    description = models.TextField('Описание', blank=True)
    price = models.DecimalField('Цена', max_digits=8, decimal_places=2)
    image = models.ImageField('Фото', upload_to='services/', blank=True, null=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return self.name

class ContactRequest(models.Model):
    """Заявка с формы обратной связи"""
    name = models.CharField('Имя', max_length=100)
    phone = models.CharField('Телефон', max_length=20)
    message = models.TextField('Сообщение', blank=True)
    created_at = models.DateTimeField('Дата', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return f'{self.name} - {self.phone}'

class SiteSettings(models.Model):
    """Настройки сайта (контакты)"""
    phone = models.CharField('Телефон', max_length=20)
    email = models.EmailField('Email')
    address = models.CharField('Адрес', max_length=300, blank=True)
    vk = models.URLField('ВКонтакте', blank=True)
    telegram = models.URLField('Telegram', blank=True)

    class Meta:
        verbose_name = 'Настройки сайта'
        verbose_name_plural = 'Настройки сайта'

    def save(self, *args, **kwargs):
        # гарантируем, что будет только одна запись с настройками
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj