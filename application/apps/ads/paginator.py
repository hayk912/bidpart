# -*- coding: utf-8 -*-
from math import ceil
from django.core.paginator import Paginator, Page

class AdsPaginator(Paginator):

    def __init__(self, *args, **kwargs):
        self.deltafirst = kwargs.pop('deltafirst', 0)
        self.deltafirst_max = kwargs.pop('deltafirst_max', 0)
        super(AdsPaginator, self).__init__(*args, **kwargs)

    def page(self, number):
        """Returns a Page object for the given 1-based page number."""
        number = self.validate_number(number)
        if number == 1:
            bottom = 0
            top = self.per_page - self.deltafirst
        else:
            bottom = (number - 1) * self.per_page - self.deltafirst_max
            top = bottom + self.per_page
        if top + self.orphans >= self.count:
            top = self.count
        return Page(self.object_list[bottom:top], number, self)

    def _get_num_pages(self):
        """Returns the total number of pages."""
        if self._num_pages is None:
            if self.count == 0 and not self.allow_empty_first_page:
                self._num_pages = 0
            else:
                hits = max(1, self.count - self.orphans + self.deltafirst)
                self._num_pages = int(ceil(hits / float(self.per_page)))
        return self._num_pages
    num_pages = property(_get_num_pages)
