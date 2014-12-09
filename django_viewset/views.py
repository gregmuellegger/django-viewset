class NamedView(object):
    '''
    A base class that is used in ViewSetMetaClass to indentify attributes that
    shall be added to the view list of the ViewSet.

    Contrary to the name, it's not an actual view but a wrapper around a
    real class-based-view.
    '''

    creation_counter = 0

    def __init__(self, view, name=None, view_kwargs=None):
        self.view = view
        self.name = name

        self.creation_counter = NamedView.creation_counter
        NamedView.creation_counter += 1
        self.view_kwargs = view_kwargs if view_kwargs is not None else {}

    def get_view_kwargs(self):
        return self.view_kwargs

    def __repr__(self):
        return '<{class_}: {name} ({view})>'.format(
            class_=self.__class__.__name__,
            name=self.name,
            view=self.view.__name__)


class URLView(NamedView):
    '''
    A named view wrapper with an attached url.
    '''

    def __init__(self, url, view, name=None, view_kwargs=None):
        super(URLView, self).__init__(
            view=view,
            name=name,
            view_kwargs=view_kwargs)
        self.url = url
