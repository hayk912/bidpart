from django.views.generic import DetailView, ListView
from models import BlogEntry


class BlogListView(ListView):
    model = BlogEntry
    template_name = 'blog/blog_list.html'
    paginate_by = 20

    def get_queryset(self):
        return BlogEntry.objects.get_active_entries()


class BlogDetailView(DetailView):
    model = BlogEntry
    template_name = 'blog/blog_detail.html'

    def get_object(self, queryset=None):
        object =  BlogEntry.objects.get_active_entry_by_slug(entry_slug=self.kwargs.get('slug'))
        return object

