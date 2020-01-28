from django import forms
from .models import Category, Post

class CategoryForm(forms.Form):  # Ozel Form
    title = forms.CharField(
        label='Kategori Ismi', max_length=100, 
        help_text="Lutfen Kategori Gir",
    )

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError('5 Karakterden Kucuk')
        return title


class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'user',
            'title',
            'status',
        ]
    
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 5:
            raise forms.ValidationError('5 Karakterden Kucuk')
        return title


class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'category',
            'title',
            'slug',
            'content',
            'cover_image',
            'status',
        ]