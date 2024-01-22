from django import forms
from django.contrib.postgres.search import SearchVector
from django.views.generic import ListView
from textblocks.utils import textblock_lazy as _t

from . import conf
from postgres_searchindex.models import IndexEntry


class SearchForm(forms.Form):
    q = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": _t("Suchbegriff")})
    )


class SearchView(ListView):
    model = IndexEntry
    template_name = "postgres_searchindex/search.html"

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
            config = conf.LANGUAGE_2_PGCONFIG.get(self.request.LANGUAGE_CODE, "english")
            print(config)
            return IndexEntry.objects.annotate(
                search=SearchVector(
                    "content",
                    "title",
                    config=config,
                )
            ).filter(index_key=self.request.LANGUAGE_CODE, search=q)
        return IndexEntry.objects.filter(pk=-1)
