from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from registration.signals import user_activated
from main.models import UserContent
from favorites.models import Favorite
from userprofiles.models import UserProfile
from tagging.models import Tag


class Timeline(models.Model):
    time = models.DateTimeField(db_index=True)
    user = models.ForeignKey(User)
    content_type = models.ForeignKey(ContentType)
    object_id = models.IntegerField()
    object = generic.GenericForeignKey()

    def __unicode__(self):
        return self.object.__unicode__()

    def get_absolute_url(self):
        return self.object.get_absolute_url()

    class Meta:
        unique_together = ('user', 'content_type', 'object_id')
        ordering = ('-time',)


def mark_timeline(instance, created=None, user_activated=None, **kwargs):
    if user_activated:
        if instance.is_active:
            tl, c = Timeline.objects.get_or_create(time=instance.date_joined,
                                                   user=instance,
                                                   object_id=instance.id,
                                                   content_type=ContentType.objects.get_for_model(instance))
    elif created:
        if isinstance(instance, UserContent):
            tl = Timeline.objects.create(time=instance.added,
                                         user=instance.user,
                                         object_id=instance.id,
                                         content_type=ContentType.objects.get_for_model(instance))
            Tag.objects.update_tags(tl, instance.tags)
        elif isinstance(instance, Favorite):
            tl = Timeline.objects.get_or_create(user=instance.user,
                                                object_id=instance.id,
                                                content_type=ContentType.objects.get_for_model(instance),
                                                time=datetime.now())

models.signals.post_save.connect(mark_timeline)
user_activated.connect(mark_timeline)

def remove_deleted(instance, **kwargs):
    if isinstance(instance, UserContent) or isinstance(instance, User) or isinstance(instance, Favorite):
        Timeline.objects.filter(content_type=ContentType.objects.get_for_model(instance),
                                object_id=instance.pk).delete()

models.signals.pre_delete.connect(remove_deleted)
