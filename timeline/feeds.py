from django.contrib.syndication.feeds import Feed
from tagging.models import Tag
from timeline.models import Timeline


class LatestContent(Feed):
    title = 'En son eklenenler'
    link = '/rss/'
    description = ''

    title_template = 'feeds/title.html'
    description_template = 'feeds/description.html'

    def items(self):
        return Timeline.objects.order_by('-time')[:20]


class LatestByUser(Feed):
    title = 'En son eklenenler'
    link = '/rss/'
    description = ''

    title_template = 'feeds/title.html'
    description_template = 'feeds/description.html'

    def items(self):
        return Timeline.objects.order_by('-time')[:20]

class LatestByTag(Feed):
    title = 'En son eklenenler'
    link = '/rss/'
    description = ''

    title_template = 'feeds/title.html'
    description_template = 'feeds/description.html'

    def items(self):
        return Timeline.objects.order_by('-time')[:20]
