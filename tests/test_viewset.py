from django.views.generic import DetailView
from django.views.generic import UpdateView

from django_viewset import URLView
from django_viewset import ViewSet


def describe_viewset():

    class SimpleViewSet(ViewSet):
        read = URLView(r'^(?P<pk>[0-9]+)/read/$', DetailView)
        update = URLView(r'^(?P<pk>[0-9]+)/update/$', UpdateView)

    def it_contains_has_correct_order():
        class ThreeViews(ViewSet):
            a = URLView(r'a', DetailView)
            c = URLView(r'c', DetailView)
            b = URLView(r'b', DetailView)

        viewset = ThreeViews()

        assert viewset.views.keys() == ['a', 'c', 'b']

    def it_contains_urlview():
        viewset = SimpleViewSet()

        assert len(viewset.views) == 2
        assert isinstance(viewset.views['read'], URLView)
        assert isinstance(viewset.views['update'], URLView)

    def it_creates_urlconf():
        viewset = SimpleViewSet()
        urls = viewset.get_urls()

        assert len(urls) == 2

        read_pattern = urls[0]

        assert read_pattern.name == 'read'
        assert read_pattern.regex.pattern == '^(?P<pk>[0-9]+)/read/$'
