from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


class TitleAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'year',
        'description',
    )
    list_filter = ('name',)
    search_fields = (
        'name',
        'genre',
        'category'
    )
    ordering = ('name',)
    empty_value_display = '-пусто-'


admin.site.register(Title, TitleAdmin)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Genre)
admin.site.register(Review)
