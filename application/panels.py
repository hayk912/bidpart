# -*- coding: utf-8 -*-
from StringIO import StringIO
import cProfile
from debug_toolbar.panels import DebugPanel
import sys

class ProfilingPanel(DebugPanel):
    name = 'cProfile'
    has_content = True
    content = ''
    title = 'cProfile'

    def nav_title(self):
        return u'cProfile'

    def url(self):
        return ''

    def nav_subtitle(self):
        return ''

    def content(self):
        return self.content


    def process_view(self, request, callback, callback_args, callback_kwargs):
        self.profiler = cProfile.Profile()
        args = (request,) + callback_args
        return self.profiler.runcall(callback, *args, **callback_kwargs)

    def process_response(self, request, response):
        self.profiler.create_stats()
        out = StringIO()
        old_stdout, sys.stdout = sys.stdout, out
        self.profiler.print_stats(1)
        self.content = '<pre>%s</pre>' % out.getvalue()
