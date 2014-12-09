class ViewSetView(object):
    '''
    A mixin for views to make them compatible with ``ViewSet``.
    '''

    # The ``viewset`` will be filled during the instantiation of the
    # ``NamedView`` (i.e. ``NamedView.as_view()`` is called with the
    # kwarg ``viewset``).
    viewset = None
