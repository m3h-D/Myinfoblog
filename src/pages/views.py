from django.shortcuts import render
from django.contrib.auth import get_user_model
# Create your views here.
from posts.models import Post, Category

User = get_user_model()


def home_page(request, recommended=None):
    special_posts = Post.objects.filter(special=True)
    posts = Post.objects.filter(published=True)
    slide_category = Category.objects.all()
    authors = User.objects.filter(is_staff=True)
    for item in posts:
        recommended = item.recommended_posts(
            request=request)
    context = {
        'special_posts': special_posts,
        'slide_category': slide_category,
        'authors': authors,
        'recommended': recommended,
    }
    return render(request, 'pages/home.html', context)
