from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import Count
from django.urls import reverse
from tinymce import HTMLField
from comments.models import Comments
from likes.models import LikeDislike
from rates.models import Rate
from usertrackers.models import UserTracker
from bookmarks.models import BookMark
import json


User = get_user_model()

# Create your models here.


class Category(models.Model):
    """ daste bandi e post ha"""
    title = models.CharField(
        max_length=120, db_index=True, verbose_name='عنوان دسته')
    slug = models.SlugField(max_length=120, blank=True, null=True,
                            unique=True, verbose_name="اسلاگ")
    description = models.TextField(
        blank=True, null=True, verbose_name='توضیحات')
    image = models.ImageField(
        blank=True, null=True, verbose_name='تصویر')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:category-list', args=[self.slug])


class Post(models.Model):
    """model e post """
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='نویسنده')
    title = models.CharField(max_length=120, verbose_name='عنوان')
    slug = models.SlugField(blank=True, max_length=100,
                            unique=True, verbose_name='اسلاگ')
    image = models.ImageField(verbose_name='تصویر عنوان')
    category = models.ManyToManyField(
        Category, related_name='post', verbose_name='دسته')
    content = HTMLField()
    read_time = models.TimeField(
        null=True, blank=True, verbose_name='زمان لازم برای خواندن پست')
    commetns = GenericRelation(Comments, related_name='post')
    rating = GenericRelation(Rate)
    likes = GenericRelation(LikeDislike, related_name='postlikes')
    published = models.BooleanField(default=True, verbose_name='پست شده')
    special = models.BooleanField(default=False, verbose_name='ویژه')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        """order barasase zamane sakht"""
        ordering = ('-created',)
        index_together = (('id', 'slug'),)
        verbose_name = 'پست'
        verbose_name_plural = 'پست ها'

    def __str__(self):
        """return kardane name nevisande va post"""
        return "پست {} توسط {}".format(self.title, self.author)

    # @property
    # def latest_posts(self):
    #     """3 ta post akhar"""
    #     posts = Post.objects.filter(
    #         published=True).order_by('-created')[:3]
    #     return posts

    @property
    def comments(self):
        """
        behtare vase har modeli ke mikhaym comment dashte bashe injuri ye property
        barash taarif konim.
        tu inja manzoor az self hamoon object haye Post e.
        age decorator e property o nazarim to view bayad joloye comments() bezarim
        """
        comments = Comments.objects.filter_by_model(instance=self)
        return comments

    # @property
    # def get_content_type(self):
    #     """
    #     baraye sakhtane form to Post bayad ContentType o begirim ta befahmim
    #     commenti ke dare neveshte mishe vase kodom post bere
    #     """

    #     content_type = ContentType.objects.get_for_model(self.__class__)
    #     return content_type

    def get_absolute_url(self):
        """reverse kardane be detail e post"""
        return reverse('posts:post-detail', args=[self.id, self.slug])

    def get_absolute_api_url(self):
        """reverse kardane be detail e post"""
        return reverse('posts-api:post-detail-api', args=[self.pk])

    # def get_like_url(self):
    #     """function e like mesele get absloute url ke dg niaz nist to html id taarif konim"""
    #     return reverse('posts:post-like', args=[self.id, self.slug])

    @property
    def post_like(self):
        """neshun dadane post haye like shude"""
        # likes = LikeDislike.objects.filter_by_model(
        #     instance=self).filter(liked=True)
        likes = LikeDislike.objects.filter_by_model(
            instance=self).filter(likedislike='like')
        return likes

    def add_to_like_post(self, request, get_like=None):
        """like kardane post ha"""
        # get_like = LikeDislike.objects.create_for_instance_model(
        #     instance=self, request=request, liked=True, disliked=False)
        get_like = LikeDislike.objects.create_for_instance_model(
            instance=self, request=request, likedislike='like')
        return get_like

    def recommended_posts(self, request, same_post=None):
        """
        category haye pishnahadi bar assasse view e user to har post.
        baraye inke az tedad like ha baraye post estefade konim ye
        GenericRelation ba Modele LikeDislike zadam
        """
        # liked haro count mikone mirize to count bar assasse hamoon order mikone
        same_post = UserTracker.objects.recommended_list(
            request=request, instance=self).annotate(count=Count('likes__likedislike')).order_by('-count')
        # same_post = UserTracker.objects.recommended_list(
        #     request=request, instance=self).annotate(count=Count('likes__liked')).order_by('-count')
        return same_post

    @property
    def post_viewed(self):
        """tedad view haey ke post khurde"""
        viewed_item = UserTracker.objects.filter_by_model(
            instance=self).values_list('ip_address', flat=True).distinct()
        return viewed_item

    def add_to_bookmarked_post(self, user):
        """Add/Remove kardane bookmark e user baraye Post"""
        book_marked = BookMark.objects.create_by_instance_model(
            user=user, instance=self)
        return book_marked

    @property
    def bookmarked_post(self):
        """check kardane inke post BookMark shude ya na"""
        book_marked = BookMark.objects.filter_by_model(
            instance=self)
        return book_marked

    @property
    def post_rate(self, avg=0):
        """emtiaz dehi be post bar assasse rate entekhab shude (az 1 ta 5) taghsim bar tedad e user haey ke be in post emtiaz dadan"""
        average = Rate.objects.avg_rate(instance=self)
        return average

    @property
    def rated_post(self):
        user_rated = Rate.objects.filter_by_model(
            instance=self)
        return user_rated
