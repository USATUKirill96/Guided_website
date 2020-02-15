from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def post_list(request):
    """Возвращает список всех постов, используется на главной странице, где они сокращенные. Обрезка поста до нужной
    длины предпросмотра происходит на стороне фронта в templates/blog/post/list.html"""
    object_list=Post.published.all()  #Передаёт все посты из базы данных для разбивки
    paginator = Paginator(object_list, 3)  #Разбивает посты по 3 на странице. Заменить число для увеличения числа постов
    page = request.GET.get('page')    #Получить номер требуемой страницы из реквеста
    try:
        posts = paginator.page(page)  #Попытаться отобразить нужную страницу (после разбивки через paginator)
    except PageNotAnInteger:
        posts = paginator.page(1)   # Если пользователь запросил не целый номер, вернуть первую
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)   #Если номер страницы больше существующего, вернуть последнюю
    return render(request, 'blog/post/list.html', {'page': page, 'posts':posts})  #Передать в шаблон list.html данные

def post_detail(request, year, month, day, post):
    """Получение подробной информации про пост (открыть полностью)"""
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year,
                             publish__month=month, publish__day=day)
    return render(request, 'blog/post/detail.html',
                  {'post':post})