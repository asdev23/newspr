from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin

from .models import News, Category
from .forms import ContactForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from newspr.custom_permissions import OnlyLoggedSuperUser

# Create your views here.

def NewsList(request):
    news_list = News.published.all()
    context = {
        'news_list':news_list
    }
    return render(request, "news/news_list.html", context)



def NewsDetail(request, news):
    news=get_object_or_404(News, slug=news, status=News.Status.Published)

    context={}
    hit_count=get_hitcount_model().objects.get_for_object(news)
    hits=hit_count.hits
    hitcontext=context['hitcount']={'pk':hit_count.pk}
    hit_count_response=HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits=hits+1
        hitcontext['hit_counted']=hit_count_response.hit_counted
        hitcontext['hit_message']=hit_count_response.hit_message
        hitcontext['total_hits']=hits

    comments=news.comments.filter(active=True)
    comment_count=comments.count()
    new_comment=None
    if request.method=="POST":
        comment_form=CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment=comment_form.save(commit=False)
            new_comment.news=news
            new_comment.user=request.user
            new_comment.save()
            comment_form=CommentForm()
    else:
        comment_form=CommentForm()

    context={
        'news':news,
        'comments':comments,
        'comment_count':comment_count,
        'new_comment':new_comment,
        'comment_form':comment_form,
    }
    return render(request, 'news/news_detail.html', context)


def HomeView(request):
    category = Category.objects.all()
    news_list=News.published.all()[:5]
    mahalliy = News.published.all().filter(category__name='Mahalliy').order_by('publish_time')[:5]
    xorij = News.published.all().filter(category__name='Xorij').order_by('publish_time')[:5]
    texnologiya = News.published.all().filter(category__name='Texnologiya').order_by('publish_time')[:5]
    sport = News.published.all().filter(category__name='Sport').order_by('publish_time')[:5]
    context={
        'news_list':news_list,
        'category':category,
        'mahalliy':mahalliy,
        'xorij':xorij,
        'texnologiya':texnologiya,
        'sport':sport,
    }
    return render(request, 'news/home.html', context)

# class HomePageView(ListView):
#     model=News
#     template_name = 'news/home.html'
#     context_object_name = 'news'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context=super().get_context_data(**kwargs)
#         context['category']=Category.model.objects.all()
#         context['news_list']=News.published.all().order_by('publish_time')[:5]
#         context['local_one']=News.published.filter(category__name='Mahalliy').order_by('publish_time')[:1]
#         context['local_news']=News.published.all().filter(category__name='Mahalliy').order_by('publish_time')[1:5]
#         return context


def ContactView(request):
    form=ContactForm(request.POST or None)
    if request.method=="POST" and form.is_valid():
        form.save()
        return HttpResponse("<h2>Biz bilan bog'langaniz uchun raxmat!</h2>")
    context={
        "form":form
    }
    return render(request, 'news/contact.html', context)
#
# class Contact(TemplateView):
#     template_name = 'news/contact.html'
#     def get(self, request, *args, **kwargs):
#         form=ContactForm()
#         context={
#             'form':form
#         }
#         return render(request, 'news/contact.html', context)
#     def post(self, request, *args, **kwargs):
#         form=ContactForm(request.POST)
#         if request.method=="POST" and form.is_valid():
#             form.save()
#             return HttpResponse("<h2>Biz bilan bog'langaniz uchun raxmat!</h2>")
#         context={
#             'form':form
#         }
#         return render(request, 'news/contact.html', context)

def Page404(request):
    context={}
    return render(request, 'news/404.html', context)

class MahalliyView(ListView):
    model = News
    template_name = 'news/mahalliy.html'
    context_object_name = 'mahalliy_yangiliklar'

    def get_queryset(self):
        news=self.model.published.all().filter(category__name='Mahalliy')
        return news


class XorijView(ListView):
    model = News
    template_name = 'news/xorij.html'
    context_object_name = 'xorij_yangiliklar'

    def get_queryset(self):
        news=self.model.published.all().filter(category__name='Xorij')
        return news


class TexnoView(ListView):
    model = News
    template_name = 'news/texnologiya.html'
    context_object_name = 'texno_yangiliklar'

    def get_queryset(self):
        news=self.model.published.all().filter(category__name='Texnologiya')
        return news


class SportView(ListView):
    model = News
    template_name = 'news/sport.html'
    context_object_name = 'sport_yangiliklar'

    def get_queryset(self):
        news=self.model.published.all().filter(category__name='Sport')
        return news


class UpdateNews(OnlyLoggedSuperUser,UpdateView):
    model = News
    fields = ('title','body','image','category','status')
    template_name='crud/update.html'

class DeleteNews(OnlyLoggedSuperUser,DeleteView):
    model = News
    template_name = 'crud/delete.html'
    success_url = reverse_lazy('home')


class CreateNews(OnlyLoggedSuperUser,CreateView):
    model = News
    fields = ('title','title_uz','title_en','title_ru',
              'slug','category','image','status',
              'body','body_uz','body_en','body_ru')
    template_name = 'crud/create.html'


class SearchListView(ListView):
    model = News
    template_name = 'news/search_result.html'
    context_object_name = 'barcha_yangiliklar'

    def get_queryset(self):
        query=self.request.GET.get('q')
        return News.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_page_view(request):
    admin_users = User.objects.filter(is_superuser=True)

    context = {
        'admin_users': admin_users
    }
    return render(request, 'pages/admin_page.html', context)
