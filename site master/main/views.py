from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings as django_settings  # импортируем настройки Django
from .models import Service, ContactRequest, SiteSettings
import requests

def index(request):
    """Главная страница-портал (короткая информация и ссылки)"""
    services = Service.objects.all()[:3]  # покажем первые 3 услуги
    context = {
        'services': services,
        'settings': SiteSettings.load(),
    }
    return render(request, 'main/index.html', context)

def services(request):
    """Список всех услуг"""
    services = Service.objects.all()
    context = {
        'services': services,
        'settings': SiteSettings.load(),
    }
    return render(request, 'main/services.html', context)

def contacts(request):
    """Страница контактов с формой обратной связи"""
    settings = SiteSettings.load()
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message', '')

        # Сохраняем заявку в БД
        ContactRequest.objects.create(
            name=name,
            phone=phone,
            message=message
        )

        # Отправляем уведомление на email (если настроено)
        if settings.email:
            send_mail(
                subject=f'Новая заявка от {name}',
                message=f'Имя: {name}\nТелефон: {phone}\nСообщение: {message}',
                from_email=settings.email,
                recipient_list=[settings.email],
                fail_silently=True,
            )

        # Отправляем уведомление в Telegram (берём токен из настроек Django)
        bot_token = django_settings.TELEGRAM_BOT_TOKEN
        chat_id = django_settings.TELEGRAM_CHAT_ID
        if bot_token and chat_id:
            text = f'Новая заявка:\nИмя: {name}\nТелефон: {phone}\nСообщение: {message}'
            try:
                requests.post(
                    f'https://api.telegram.org/bot{bot_token}/sendMessage',
                    data={'chat_id': chat_id, 'text': text},
                    timeout=5
                )
            except requests.RequestException:
                pass  # игнорируем ошибки сети/телеграма

        return redirect('contacts')  # после отправки редиректим на ту же страницу

    context = {
        'settings': settings,
    }
    return render(request, 'main/contacts.html', context)