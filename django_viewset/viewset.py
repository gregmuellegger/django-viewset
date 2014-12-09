from django.conf.urls import url
from django.utils.datastructures import SortedDict
from django.utils.six import with_metaclass
from .views import NamedView, URLView


def add_view(viewset, named_view, attribute):
    if not getattr(named_view, 'name', None):
        named_view.name = attribute
    setattr(viewset, attribute, named_view)
    viewset.views[attribute] = named_view


class ViewSetMetaClass(type):
    def __new__(cls, name, bases, attrs):
        new_class = super(ViewSetMetaClass, cls).__new__(
            cls, name, bases, attrs)
        # Make a copy of that list. Otherwise we have the same instance on the
        # parent and child class. This would result in views beeing added to
        # the parent which should only be defined on the children.
        new_class.views = getattr(new_class, 'views', SortedDict()).copy()

        views = [
            (attribute, value)
            for attribute, value in attrs.items()
            if isinstance(value, NamedView)]
        views.sort(key=lambda x: x[1].creation_counter)
        for attribute, view in views:
            add_view(new_class, view, attribute)
        return new_class


class ViewSet(with_metaclass(ViewSetMetaClass), object):
    '''
    This can be used as a mixin to provide a container for multiple views.
    Views are attached via attributes to the ViewSet. An example can look as
    follows::

        class CRUDSet(django_viewset.ViewSet):
            create_view = django_viewset.URLView(
                r'^create/$', CreateView, name='create')
            read_view = django_viewset.URLView(
                r'^(?P<pk>[0-9]+)/read/$', ReadView, name='detail')
            update_view = django_viewset.URLView(
                r'^(?P<pk>[0-9]+)/update/$', UpdateView, name='update')
            delete_view = django_viewset.URLView(
                r'^(?P<pk>[0-9]+)/delete/$', DeleteView, name='delete')

    The given URLView's can than be "exported" as urlpatterns view the
    ``get_urls`` method::

        crud_set = CRUDSet()

        urlpatterns = patterns('',
            url(r'^crud/', crud_set.get_urls())
        )
    '''

    urlname_separator = '-'

    def __init__(self, urlname_prefix=None):
        # Make a copy of that list, to prevent changes taking any effect on
        # the class variable.
        self.views = self.views.copy()
        self.urlname_prefix = urlname_prefix

    def add_view(self, named_view, attribute):
        add_view(self, named_view, attribute)

    def get_view(self, name):
        for view in self.views.values():
            if view.name == name:
                return view
        raise ValueError('Cannot find viewset view named {0}'.format(name))

    def get_view_default_kwargs(self, viewset_view):
        return {}

    def get_view_kwargs(self, viewset_view):
        '''
        This will compile a dictionary of all kwargs that shall be passed into
        the ``View.as_view`` constructor. There are few places checked to
        collect these kwargs:

        1. The ``ViewSet.get_view_default_kwargs`` will be used.

        2. Check if the ``ViewSet`` instance has a method called
           ``get_<view-name>_view_kwargs`` and call this. The ``<view-name>``
           part is replaced with the ``viewset_view.name`` attribute of the
           passed in ``viewset_view``.

        3. If no method is found in point 2. then the passed
           ``viewset_view.get_view_kwargs`` method will be used.

        4. The ``viewset`` kwargs will be set to the current ViewSet instance,
           but only if the View has an attribute called ``viewset``. This
           prevents issues with django's class based views, since they will
           raise an error if you pass in a kwargs with a name for which the
           View has not existing attribute.
           What this means is basically: Only pass in the ``viewset`` kwarg if
           the View will accept it.
        '''
        kwargs = self.get_view_default_kwargs(viewset_view)

        # Allow kwargs to be overriden
        method_name = 'get_%s_view_kwargs' % viewset_view.name
        if hasattr(self, method_name):
            kwargs.update(getattr(self, method_name)(viewset_view))
        else:
            kwargs.update(viewset_view.get_view_kwargs())

        # Only set the viewset, if the view will take it as parameter.
        if hasattr(viewset_view.view, 'viewset'):
            kwargs['viewset'] = self
        return kwargs

    def get_view_instance(self, viewset_view):
        kwargs = self.get_view_kwargs(viewset_view)
        try:
            view_instance = viewset_view.view.as_view(**kwargs)
        except Exception as e:
            import sys
            trace = sys.exc_info()[2]
            new_exception = TypeError(
                'Cannot instantiate viewset view "{}.{}". '
                'The error was: {0}'.format(
                    self.__class__.__name__, viewset_view.name, e))
            raise new_exception, None, trace
        return view_instance

    def get_view_urlname(self, viewset_view):
        return '{prefix}{separator}{view_name}'.format(
            prefix=self.urlname_prefix if self.urlname_prefix else '',
            separator=self.urlname_separator if self.urlname_prefix else '',
            view_name=viewset_view.name)

    def get_urls(self):
        patterns = []
        for viewset_view in self.views.values():
            # We will only create url patterns for views that have an actual
            # url attribute. This is for example true for all subclasses of
            # URLView.
            if hasattr(viewset_view, 'url'):
                view_instance = self.get_view_instance(viewset_view)
                patterns.append(
                    url(regex=viewset_view.url,
                        view=view_instance,
                        name=self.get_view_urlname(viewset_view)))
        return patterns


class ModelViewSet(ViewSet):
    def __init__(self, model):
        self.model = model

    def get_view_default_kwargs(self, viewset_view):
        kwargs = super(ModelViewSet, self).get_view_default_kwargs(viewset_view)
        if hasattr(viewset_view.view, 'model'):
            kwargs['model'] = self.model
        return kwargs
