from .mixins import ViewSetView


def viewset_view(view_class):
    '''
    A helper to make an existing class-based-view compatible with a
    ``ViewSet``. It therefore creates a new subclass of the passed in view
    and subclasses from the necessary ``ViewSetView`` mixin as first base
    class.
    '''

    class View(ViewSetView, view_class):
        pass

    return View
