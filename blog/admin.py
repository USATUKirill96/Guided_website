from django.contrib import admin

from .models import Post, Comment
# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status') #Пункты, отображаемые в панели администратора
    list_filter = ('status', 'created', 'publish', 'author') #По каким критериям можно фильтровать
    search_fields = ('title', 'body') #Поля для функции поиска
    prepopulated_fields = {'slug': ('title',)}  #Автоматическое заполнение слага из заголовка статьи
    raw_id_fields = ('author',) #Поле поиска для автора добавлено
    date_hierarchy = 'publish' #добавление ссылок навигации по дате
    ordering = ('status', 'publish') #сортировка по умолчанию

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name','email','body')