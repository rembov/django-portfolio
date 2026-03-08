from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Post, Comment
from .forms import CommentForm

def index(request):
    posts = Post.objects.filter(published=True).order_by('-created_at')
    paginator = Paginator(posts, 5)  # по 5 постов на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/index.html', {'page_obj': page_obj})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, published=True)
    comments = post.comments.filter(moderated=True).order_by('-created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            # После сохранения редиректим на эту же страницу (чтобы избежать повторной отправки)
            return redirect('post_detail', slug=post.slug)
    else:
        form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'form': form,
    }
    return render(request, 'blog/post_detail.html', context)