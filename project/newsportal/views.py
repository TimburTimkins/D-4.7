from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .filters import NewsFilter
from .forms import NewsForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from .models import News, Subscriber, Category
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.utils import timezone
import pytz
from django.shortcuts import redirect
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import permissions
from newsportal.serializers import *
from .tasks import new_post
from django.utils.translation import gettext as _


class NewsViewset(viewsets.ModelViewSet):
   queryset = News.objects.all()
   serializer_class = NewsSerializer


class CategoryViewset(viewsets.ModelViewSet):
   queryset = Category.objects.all()
   serializer_class = CategorySerializer


class SubscriberViewest(viewsets.ModelViewSet):
   queryset = Subscriber.objects.all()
   serializer_class = SubscriberSerializer


class Index(View):
    def get(self, request):

        models = News.objects.all()

        context = {
            'models': models,
            'current_time': timezone.localtime(timezone.now()),
            'timezones': pytz.common_timezones,
        }

        return HttpResponse(render(request, 'default.html', context))

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')


@cache_page(60 * 15)
def my_view(request):
    ...


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


class NewsportalList(ListView):
    model = News
    ordering = '-date_on'
    template_name = 'default.html'
    context_object_name = 'text'
    paginate_by = 10


class NewsList(ListView):
    model = News
    ordering = '-date_on'
    template_name = 'default.html'
    context_object_name = 'text'
    queryset = News.objects.filter(type= 'NEW')
    paginate_by = 10


class ArtList(ListView):
    model = News
    ordering = '-date_on'
    template_name = 'default.html'
    context_object_name = 'text'
    queryset = News.objects.filter(type= 'ARTICLE')
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

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'new-{self.kwargs["pk"]}',
                        None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'new-{self.kwargs["pk"]}', obj)
            return obj


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

    # def form_valid(self, form):
    #     news = form.save(commit=False)
    #     news.type = 'NEW'
    #     return super().form_valid(form)


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