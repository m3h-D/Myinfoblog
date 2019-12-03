from .models import Post, Category
from comments.models import Comments
from django.db.models import Count


def post_sidebar(request):
    """include kardane sidebar to list o detail e post"""
    late_post = Post.objects.filter(published=True).order_by('-created')[:3]
    category = Category.objects.all().order_by('title')
    context = {
        'category_title_sidebar': category,
        'late_post_sidebar': late_post,
    }
    return context


def comments_counter(request):
    comment_counter = Comments.objects.filter(approved=False).count()
    return {'comment_counter': comment_counter}
