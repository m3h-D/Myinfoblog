from django.db import models
from tinymce import HTMLField
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .utils import uuid_generator

from likes.models import LikeDislike
from .utils import uuid_generator

# from posts.models import Post


User = get_user_model()

# Create your models here.


class CommentManager(models.Manager):
    """
    ye custom filter sakhtim ke to view ya (model property) rahat tar betunim content_object vase 
    comment haro bargardoonim.
    """

    def filter_by_model(self, instance):
        """
        to khat e zir ma az instance.__class__ estefade kardim ke modelio migire ke to
        view ya to (model propert) behesh pas midim.
        """
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        queryset = super(CommentManager, self).filter(
            content_type=content_type, object_id=obj_id).filter(parent=None)
        return queryset

    def form_create_by_model(self, instance, object_id, user, content, parent_obj=None):
        """
        tu inja darim modeli ke dare request midea ro migirim(filter_by_model)
        baad bayad check konim bebinim model.exists ya na
        age bud daghighan mesle form to view ammal mikonim (bedoone commit=False).
        vase API content o bayad shabihe request begirm(validated_data.get('content')).
        """
        # content_type = ContentType.objects.get_for_model(instance.__class__)
        content_type = ContentType.objects.filter(
            model=instance).first()
        uuid = uuid_generator()
        # content_object = self.filter_by_model(instance=instance)

        # some_model = content_type.model_class()
        # obj_qs = some_model.objects.get(id=object_id)
        # if some_model.exists():
        # comment_form = self.model
        # comment_form.user = user
        # comment_form.content = content
        # comment_form.content_object = content_type
        # comment_form.object_id = object_id
        if parent_obj:
            parent_obj = parent_obj
            # comment_form.parent = parent
        # comment_form.save()
        comment_form = super(CommentManager, self).create(user=user, content=content,
                                                          content_type=content_type, object_id=object_id, parent=parent_obj, uuid=uuid)
        return comment_form

        # def create_by_model(self, model_type, object_id, content, user, parent_obj=None):
        # model_qs = ContentType.objects.filter(model=model_type)
        # if not model_qs.exists():
        #     SomeModel = model_qs.first().model__class()
        #     object_qs = SomeModel.objects.filter(id=object_id)
        #     if object_qs.exists():
        #         instance = self.model()
        #         instance.content = content
        #         instance.user = user
        #         instance.content_type = model_qs.first()
        #         instance.object_id = object_qs.first().id
        #         if parent_obj:
        #             instance.parent = parent_obj
        #         instance.save()
        # return instance

        # object_qs = instance.__class__.objects.filter(id=object_id)
        # if object_qs.exists():

        # --------- code create e khudam --------------------------
        # if parent_obj:
        #     queryset = super(CommentManager, self).create(
        #         user=user,
        #         content_type=content_type,
        #         object_id=object_id,
        #         parent=parent_obj,
        #         content=content,
        #     )
        # else:
        #     queryset = super(CommentManager, self).create(
        #         user=user,
        #         content_type=content_type,
        #         object_id=object_id,
        #         content=content,
        #     )
        # return queryset


class Comments(models.Model):
    """comment haye marboot be har user baraye har modeli"""
    user = models.ForeignKey(
        User, related_name='comments', on_delete=models.CASCADE, verbose_name='کاربر')

    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, verbose_name='قسمت')
    object_id = models.PositiveIntegerField(verbose_name='ایدی قسمت')
    content_object = GenericForeignKey('content_type', 'object_id')
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, verbose_name='جواب')
    content = models.TextField(verbose_name='کامنت')
    uuid = models.CharField(max_length=200, unique=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = CommentManager()

    class Meta:
        """order kardane commentha barasase zamane sakht"""
        ordering = ('-timestamp',)
        verbose_name = 'کامنت'
        verbose_name_plural = 'کامنت ها'

    def __str__(self):
        """neshun dadane karbar"""
        if self.parent is None:
            return "{} . کامنت گذاشت برای {} است".format(self.user.username,  self.content_object.title)
        else:
            return "جواب {} به کامنت {} در پست {}".format(self.user.username, self.parent.user.username, self.content_object.title)

    def children(self):
        """comment haye marboot be parent o barmigardoone """
        return Comments.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True

    @property
    def comment_like(self):
        """baraye neshun dadane tedad e like ha estefade mishe"""
        # likes = LikeDislike.objects.filter_by_model(
        #     instance=self).filter(liked=True)
        likes = LikeDislike.objects.filter_by_model(
            instance=self).filter(likedislike='like')

        return likes

    @property
    def comment_dislike(self):
        """baraye neshun dadane tedad e disloke ha estefade mishe"""
        # dislikes = LikeDislike.objects.filter_by_model(
        #     instance=self).filter(disliked=True)
        dislikes = LikeDislike.objects.filter_by_model(
            instance=self).filter(likedislike='dislike')
        return dislikes

    def add_to_like_comment(self, request, get_like=None):
        """
        darsoorati ke commenti like shude bashe gerefte mishe va
        Manager e Model e Like rush logic anjam mide (pak mikone).
        age ham like nashude bashe like e comment baraye request.user True mishe.
        """
        # get_like = LikeDislike.objects.create_for_instance_model(
        #     instance=self, request=request, liked=True, disliked=False)
        get_like = LikeDislike.objects.create_for_instance_model(
            instance=self, request=request, likedislike='like')
        return get_like

    def add_to_dislike_comment(self, request, get_dislike=None):
        """
        age commenti dislike shude bud gerefte mishe to Manager e Model e Like
        Logicash anjam mishe (pak mishe).
        age baraye avvalin bar request.user in comment o dislike karde bud
        barash dislikesh True mishe.
        """
        # get_dislike = LikeDislike.objects.create_for_instance_model(
        #     instance=self, request=request, liked=False, disliked=True)
        get_dislike = LikeDislike.objects.create_for_instance_model(
            instance=self, request=request, likedislike='dislike')
        return get_dislike
