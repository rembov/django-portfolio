from django.shortcuts import render, redirect
from .models import EventSettings, Speaker, Schedule, Registration

def index(request):
    settings = EventSettings.load()
    speakers = Speaker.objects.all()
    schedule = Schedule.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        if name and email and phone:
            Registration.objects.create(
                name=name,
                email=email,
                phone=phone
            )
            # можно добавить сообщение об успехе через messages
            return redirect('index')  # редирект на ту же страницу (чтобы избежать повторной отправки)

    context = {
        'settings': settings,
        'speakers': speakers,
        'schedule': schedule,
    }
    return render(request, 'event/index.html', context)