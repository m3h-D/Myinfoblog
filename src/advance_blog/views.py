from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404, reverse

from comments.models import Comments
from posts.models import Post, Category
from posts.forms import AddPostForm
from posts.views import create_post
from accounts.models import Profile


def panel_admin(request):
    """comment haye taayd nashude ba kolle post ha va form sakhte post injast"""
    comments = get_list_or_404(Comments, approved=False)
    posts = get_list_or_404(Post)
    categories = get_list_or_404(Category)
    form = create_post(request)
    # form = AddPostForm(request.POST or None, request.FILES or None)
    # if request.method == "POST":
    #     if form.is_valid():
    #         form.instance.author = request.user
    #         form.save()
    #         return redirect(reverse("posts:post-detail", kwargs={'id': form.instance.id,
    #                                                              'slug': form.instance.slug}))

    context = {
        'comments': comments,
        'posts': posts,
        'form': form,
        'categories': categories,
    }
    return render(request, 'panelAdmin.html', context)
