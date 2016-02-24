==============
django-viewset
==============

|pypi-badge| |build-status|

**django-viewset** is an easy way to group multiple Django views into one
class. It's like providing a ``urlpatterns`` for an app, but has some benefits
over it:

- You get the benefit of readability as you see at a glance what views of your
  app belong together and should be put into a ``urls.py`` together.
- Having a class to group views together brings makes it possible to easily
  combine multiple viewsets, override only parts of a viewset and all other
  things you can do with a class.

Here is an example:

.. code:: python

    # In your viewsets.py file.

    from django_viewset URLView
    from django_viewset ViewSet
    from django.contrib.auth.models import User
    from django.views.generic import DetailView, CreateView, UpdateView, DeleteView


    class UserCRUD(ViewSet):
        view_kwargs = {
            'queryset': User.objects.all(),
        }

        create = URLView(r'^create/$', CreateView, view_kwargs=view_kwargs)
        read = URLView(r'^(?P<pk>[0-9]+)/$', DetailView, view_kwargs=view_kwargs)
        update = URLView(r'^(?P<pk>[0-9]+)/update/$', UpdateView, view_kwargs=view_kwargs)
        delete_view = URLView(r'^(?P<pk>[0-9]+)/delete/$', DeleteView,
                              name='delete', view_kwargs=view_kwargs)


    # In your urls.py file.

    from .viewsets import CRUDSet


    user_crud_set = UserCRUD(urlname_prefix='user')

    urlpatterns = patterns(''
        url(r'^users/', user_crud_set.get_urls())
    )

This shows a viewset that combines the typical CRUD features into one class. It
can be placed into your URL config by simply instantiating the viewset and
calling the ``get_urls()`` method as shown above.

The views in the viewset are defined as class attributes. Use ``URLView`` to
attach a view to the viewset. The first argument is the URL under which the
view will be accessible. The second argument is a class-based-view. You can
pass in ``view_kwargs`` that will get passed down to the
``.as_view(**view_kwargs)``.

All urls for the views in a viewset will have a name attached. The name
defaults to the attribute name that the view has on the viewset. But you can
also override this using the ``name`` argument. See the ``detail_view`` view as
example. We cannot use ``delete`` as class argument since that's a reserved
Python keyword, but we can use it as a url name though.

The url names are then prefixed with the ``urlname_prefix`` paramater that you
can pass in when you instantiate the viewset.

Here are a view examples of how viewset url names can be used to get the
corresponding URL:

.. code:: python

    from django.core.urlresolvers import reverse

    reverse('user-create') == '/users/create/'
    reverse('user-read', args=(42,)) == '/users/42/'
    reverse('user-delete', kwargs={'pk': 13}) == '/users/13/delete/'


.. |build-status| image:: https://travis-ci.org/gregmuellegger/django-viewset.svg
    :target: https://travis-ci.org/gregmuellegger/django-viewset

.. |pypi-badge| image:: https://img.shields.io/pypi/v/django-viewset.svg
    :target: https://pypi.python.org/pypi/django-viewset
