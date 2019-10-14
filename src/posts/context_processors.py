from .models import Post, Category
from django.db.models import Count


def post_sidebar(request):
    """include kardane sidebar to list o detail e post"""
    posts = Post.objects.filter(published=True)
    category = Category.objects.all().order_by('title')

    late_post = posts.order_by('-created')[:3]
    context = {
        'category_title_sidebar': category,
        'late_post_sidebar': late_post,
    }
    return context
