# -*- coding: utf-8 -*-

from time import strftime
from django.db.models import Max
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import QuerySetPaginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.utils.feedgenerator import Rss201rev2Feed
from django.http import Http404, HttpResponse
from django.template import RequestContext
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.views.decorators.vary import vary_on_headers
from django.template.loader import render_to_string
from favorites.models import Favorite
from main.utils import index_context, list_context, tags_for_model
from tagging.models import TaggedItem, Tag
from timeline.models import Timeline


@vary_on_headers('Host')
def user_list(request):
    queryset = Timeline.objects.filter(user__is_active=True).values('user').annotate(last=Max('time')).order_by('-last')
    if request.current_user:
        ctype = ContentType.objects.get_for_model(User)
        favorites = Favorite.objects.filter(user=request.current_user,
                                            content_type=ctype).values_list('object_id', flat=True)
        queryset = queryset.filter(user__id__in=favorites)
    paginator = QuerySetPaginator(queryset, 20)
    try:
        page = paginator.page(request.GET.get('p', 1))
    except (EmptyPage, InvalidPage):
        page = paginator.page(paginator.num_pages)
    return render_to_response('timeline/user_list.html',
                              {'user_list': [User.objects.get(id=item['user']) for item in page.object_list],
                               'page': page},
                              context_instance=RequestContext(request))

@vary_on_headers('Host')
def rss(request, tag_slug=None, model_name=None):
    items = Timeline.objects.all()
    if model_name:
        if model_name in ('not', 'foto', 'harita', 'yazi', 'uye', 'forum', 'aktivite', 'yer'):
            if model_name == 'not':
                feed_title = u'en son eklenen notlar'
            elif model_name == 'foto':
                feed_title = u'en son eklenen fotoğraflar'
            elif model_name == 'harita':
                feed_title = u'en son eklenen haritalar'
            elif model_name == 'yazi':
                feed_title = u'en son eklenen yazılar'
            elif model_name == 'uye':
                feed_title = u'en son katılan üyeler'
            elif model_name == 'forum':
                feed_title = u'en son forum yazıları'
            elif model_name == 'aktivite':
                feed_title = u'en son eklenen etkinlikler'
            elif model_name == 'yer':
                feed_title = u'en son işaretlenen yerler'
        else:
            raise Http404
        items = items.filter(content_type=ctype)
    else:
        feed_title = u'en son eklenenler'

    if request.current_user:
        items = items.filter(user=request.current_user)
        feed_title = u'%s tarafından %s' % (request.current_user, feed_title)
        feed_link = 'http://%s.%s%s' % (request.current_user, Site.objects.get_current().domain, request.path)
    else:
        feed_title = u'''gezgin'e %s''' % (feed_title,)
        feed_link = request.path

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        items = TaggedItem.objects.get_by_model(items, tag)
        feed_title = u'%s için %s' % (tag.name, feed_title)
    feed = Rss201rev2Feed(title=feed_title,
                          description=feed_title,
                          link=feed_link)
    items = items.order_by('-time')[:50]
    current_site = Site.objects.get_current()
    for tl_item in items:
        feed.add_item(title=render_to_string('timeline/feed_item_title.html', {'item': tl_item,
                                                                               'current_site': current_site}),
                      description=render_to_string('timeline/item.html', {'item': tl_item,
                                                                          'current_site': current_site}),
                      link=render_to_string('timeline/feed_item_link.html', {'item': tl_item,
                                                                             'current_site': current_site}))
    return HttpResponse(feed.writeString('UTF-8'), mimetype=feed.mime_type)

