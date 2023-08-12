from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import News
from .filters import NewsFilter
from .forms import NewsForm
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy


class NewsList(ListView):
    model = News
    ordering = '-date_on'
    template_name = 'default.html'
    context_object_name = 'text'
    paginate_by = 10

class NP_Search(ListView):
    form_class = NewsForm
    model = News
    template_name = 'news_search.html'
    context_object_name = 'text'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsDetail(DetailView):
    model = News
    template_name = 'onenew.html'
    context_object_name = 'new'


def multiply(request):
   number = request.GET.get('number')
   multiplier = request.GET.get('multiplier')

   try:
       result = int(number) * int(multiplier)
       html = f"<html><body>{number}*{multiplier}={result}</body></html>"
   except (ValueError, TypeError):
       html = f"<html><body>Invalid input.</body></html>"

   return HttpResponse(html)

def create_news(request):
    form = NewsForm()
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/news/')

    return render(request, 'news_edit.html', {'form': form})


class NewsCreate(CreateView):
    form_class = NewsForm
    model = News
    template_name = 'news_edit.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.category = 'News'
        return super().form_valid(form)


class ArtCreate(CreateView):
    form_class = NewsForm
    model = News
    template_name = 'news_edit.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.category = 'Article'
        return super().form_valid(form)


class NewsUpdate(UpdateView):
    form_class = NewsForm
    model = News
    template_name = 'news_edit.html'


class ArtUpdate(UpdateView):
    form_class = NewsForm
    model = News
    template_name = 'news_edit.html'


class NewsDelete(DeleteView):
    model = News
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')


class ArtDelete(DeleteView):
    model = News
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')