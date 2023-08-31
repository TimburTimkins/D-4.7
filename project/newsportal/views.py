from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import News
from .filters import NewsFilter
from .forms import NewsForm
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from .models import Subscriber, Category


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscriber.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscriber.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscriber.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )


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


class NewsCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    raise_exception = True
    permission_required = ('newsportal.add_news',)
    form_class = NewsForm
    model = News
    template_name = 'news_edit.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.type = 'NEW'
        return super().form_valid(form)


class ArtCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    raise_exception = True
    permission_required = ('newsportal.add_news',)
    form_class = NewsForm
    model = News
    template_name = 'news_edit.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.type = 'AR'
        return super().form_valid(form)


class NewsUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    raise_exception = True
    permission_required = ('newsportal.change_news',)
    form_class = NewsForm
    model = News
    template_name = 'news_edit.html'


class ArtUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    raise_exception = True
    permission_required = ('newsportal.change_news',)
    form_class = NewsForm
    model = News
    template_name = 'news_edit.html'


class NewsDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    raise_exception = True
    permission_required = ('newsportal.delete_news',)
    model = News
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')


class ArtDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    raise_exception = True
    permission_required = ('newsportal.delete_news',)
    model = News
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')