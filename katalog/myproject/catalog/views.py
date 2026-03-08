from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.db.models import Q, Avg
from .models import Item, Category, Review
from .forms import RegisterForm, ReviewForm

def index(request):
    """Главная страница со списком и фильтрацией"""
    items = Item.objects.all()
    query = request.GET.get('q', '')
    category_slug = request.GET.get('category', '')
    year = request.GET.get('year', '')

    if query:
        items = items.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if category_slug:
        items = items.filter(category__slug=category_slug)
    if year:
        items = items.filter(year=year)

    # Для фильтров в шаблоне
    categories = Category.objects.all()
    years = Item.objects.values_list('year', flat=True).distinct().order_by('-year')

    context = {
        'items': items,
        'categories': categories,
        'years': years,
        'selected_category': category_slug,
        'selected_year': year,
        'query': query,
    }
    return render(request, 'catalog/index.html', context)

def item_detail(request, item_id):
    """Страница элемента с отзывами и формой добавления отзыва"""
    item = get_object_or_404(Item, pk=item_id)
    reviews = item.reviews.all().order_by('-created_at')
    user_review = None
    form = None

    if request.user.is_authenticated:
        try:
            user_review = Review.objects.get(item=item, user=request.user)
        except Review.DoesNotExist:
            pass

    if request.method == 'POST' and request.user.is_authenticated and not user_review:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.item = item
            review.user = request.user
            review.save()
            return redirect('item_detail', item_id=item.id)
    else:
        form = ReviewForm()

    context = {
        'item': item,
        'reviews': reviews,
        'user_review': user_review,
        'form': form,
    }
    return render(request, 'catalog/item_detail.html', context)

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'catalog/register.html', {'form': form})

# Стандартный login и logout можно использовать из django.contrib.auth.views
# Но мы создадим простые свои (или подключим в urls.py)