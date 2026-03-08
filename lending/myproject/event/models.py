from django.db import models
from django.utils import timezone  # для установки даты по умолчанию


class EventSettings(models.Model):
    """Настройки мероприятия (синглтон)"""
    title = models.CharField('Название события', max_length=200)
    description = models.TextField('Описание')
    date_start = models.DateTimeField('Дата и время начала')
    venue = models.CharField('Место проведения', max_length=300)
    organizer_contact = models.CharField('Контакты организатора', max_length=200, blank=True)
    logo = models.ImageField('Логотип', upload_to='event/', blank=True, null=True)

    class Meta:
        verbose_name = 'Настройки события'
        verbose_name_plural = 'Настройки события'

    def save(self, *args, **kwargs):
        # гарантируем единственную запись
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        """
        Загружает настройки. Если записи нет – создаёт с временными значениями.
        """
        obj, created = cls.objects.get_or_create(
            pk=1,
            defaults={
                'title': 'Новое событие',
                'description': 'Добавьте описание в админке',
                'date_start': timezone.now() + timezone.timedelta(days=30),  # через месяц
                'venue': 'Место не указано',
                'organizer_contact': 'Контакт не указан',
            }
        )
        return obj

    def __str__(self):
        return self.title


class Speaker(models.Model):
    """Спикер мероприятия"""
    name = models.CharField('Имя', max_length=100)
    title = models.CharField('Должность / компания', max_length=200)
    photo = models.ImageField('Фото', upload_to='speakers/', blank=True, null=True)
    bio = models.TextField('Биография', blank=True)
    social_link = models.URLField('Ссылка на соцсети', blank=True)

    class Meta:
        verbose_name = 'Спикер'
        verbose_name_plural = 'Спикеры'

    def __str__(self):
        return self.name


class Schedule(models.Model):
    """Пункт программы"""
    start_time = models.DateTimeField('Начало')
    end_time = models.DateTimeField('Конец')
    title = models.CharField('Название', max_length=200)
    description = models.TextField('Описание', blank=True)
    speaker = models.ForeignKey(
        Speaker,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Спикер'
    )

    class Meta:
        verbose_name = 'Программа'
        verbose_name_plural = 'Программа'
        ordering = ['start_time']

    def __str__(self):
        return f'{self.start_time.strftime("%d.%m %H:%M")} – {self.title}'


class Registration(models.Model):
    """Заявка на участие"""
    name = models.CharField('Имя', max_length=100)
    email = models.EmailField('Email')
    phone = models.CharField('Телефон', max_length=20)
    registered_at = models.DateTimeField('Дата регистрации', auto_now_add=True)

    class Meta:
        verbose_name = 'Регистрация'
        verbose_name_plural = 'Регистрации'
        ordering = ['-registered_at']

    def __str__(self):
        return f'{self.name} – {self.email}'