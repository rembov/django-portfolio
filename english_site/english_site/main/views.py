import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import Word, Achievement, UserAchievement
from .forms import RegisterForm

def index(request):
    return render(request, 'main/index.html')

@login_required
def words_view(request):
    words = Word.objects.all()
    words_list = list(words.values('id', 'category', 'word', 'translation'))
    context = {'words_json': json.dumps(words_list, ensure_ascii=False)}
    return render(request, 'main/words.html', context)

@login_required
def game_view(request):
    words = Word.objects.all()
    words_list = list(words.values('id', 'category', 'word', 'translation'))
    context = {'words_json': json.dumps(words_list, ensure_ascii=False)}
    return render(request, 'main/game.html', context)

@login_required
def grammar_view(request):
    return render(request, 'main/grammar.html')

@login_required
def speaking_view(request):
    return render(request, 'main/speaking.html')

@login_required
def awards_view(request):
    user_achievements = UserAchievement.objects.filter(user=request.user).values_list('achievement__code', flat=True)
    all_achievements = Achievement.objects.all()
    context = {
        'user_achievements': list(user_achievements),
        'all_achievements': all_achievements,
    }
    return render(request, 'main/awards.html', context)

@login_required
def check_answer(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        test_type = data.get('test_type')
        correct = data.get('correct')
        if correct:
            try:
                ach = Achievement.objects.get(code=test_type)
                obj, created = UserAchievement.objects.get_or_create(user=request.user, achievement=ach)
                if created:
                    return JsonResponse({'success': True, 'new_achievement': ach.name})
            except Achievement.DoesNotExist:
                pass
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'main/register.html', {'form': form})