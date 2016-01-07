import django


# Is available in Python 2.7 and higher. SortedDict will be removed in Django
# 1.9 and higher.
try:
    from collections import OrderedDict
except ImportError:
    from django.utils.datastructures import SortedDict as OrderedDict
