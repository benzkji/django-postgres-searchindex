from django import forms
from django.utils.module_loading import import_string
from django.views.generic import ListView

from postgres_searchindex.models import IndexEntry

from . import conf


class SearchForm(forms.Form):
    q = forms.CharField(widget=forms.TextInput())


class SearchView(ListView):
    model = IndexEntry
    template_name = "postgres_searchindex/search.html"
    paginate_by = conf.PAGINATE_BY

    def dispatch(self, request, *args, **kwargs):
        self.form = SearchForm(self.request.GET)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self):
        c = super().get_context_data()
        c["form"] = self.form
        return c

    def get_queryset(self):
        if self.form.is_valid():
            q = self.form.cleaned_data["q"]
            query_func = import_string(conf.QUERY_FUNC)
            return query_func(q, self.request.LANGUAGE_CODE)
        return IndexEntry.objects.filter(pk=-1)
