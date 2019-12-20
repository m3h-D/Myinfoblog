from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404, reverse
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.admin.views.decorators import staff_member_required

from accounts.models import Profile
# from posts.views import create_post
from posts.forms import AddPostForm
from comments.models import Comments
# Create your views here.
from posts.models import Post, Category

User = get_user_model()


def home_page(request, recommended=None):
    special_posts = Post.objects.filter(special=True)
    posts = Post.objects.filter(published=True)
    slide_category = Category.objects.all()
    post_authors = Post.objects.values_list('author__id', flat=True)
    authors = User.objects.filter(id__in=post_authors)
    # 'author__first_name', 'author__profile__bio', 'author__profile__image')
    # print(authors)
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


@staff_member_required
def panel_admin(request):
    """comment haye taayd nashude ba kolle post ha va form sakhte post injast"""
    comments = get_list_or_404(Comments, approved=False)
    posts = get_list_or_404(Post)
    categories = get_list_or_404(Category)
    # form = create_post(request)

    form = AddPostForm(request.POST or None, request.FILES or None, initial={
                       'author': request.user})
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return redirect(reverse("posts:post-detail", kwargs={'post_id': form.instance.id,
                                                                 'post_slug': form.instance.slug}))

    context = {
        'comments': comments,
        'posts': posts,
        'form': form,
        'categories': categories,
    }
    return render(request, 'pages/panelAdmin.html', context)
