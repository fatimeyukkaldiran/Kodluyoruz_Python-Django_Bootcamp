from django.contrib import admin
from .models import (
    Category, 
    Post,
    PostLove,
    Tag,
)
from .forms import CategoryModelForm

class CategoryAdmin(admin.ModelAdmin):
    form = CategoryModelForm
    pass


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post)
admin.site.register(PostLove)
admin.site.register(Tag)