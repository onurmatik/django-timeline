from django.template import Library
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.utils.safestring import mark_safe


register = Library()


@register.filter(name='model_name')
def model_name(obj):
    return getattr(ContentType.objects.get_for_model(obj), 'name')

@register.filter(name='tags_to_links')
def tags_to_links(obj):
    user = obj.user
    domain = Site.objects.get_current()
    tags = obj.tags.split(',')[:3]
    links = [mark_safe('''<a href="http://%(user)s.%(domain)s/%(tag)s"
                       >%(tag)s</a>''' % {'user': user,
                                          'domain': domain,
                                          'tag': tag.strip().lower()}) for tag in tags]
    return links

