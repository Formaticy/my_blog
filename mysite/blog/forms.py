from django import forms
from django_summernote.widgets import SummernoteWidget

from .models import Comment


# Два способа создавать формы: класс Form (просто форма) и ModelForm (форма для модели)
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25, required=True, widget=forms.TextInput(attrs={"class": "form-control mb-1", 'placeholder': 'Имя'}))# экземпляр класса CharField с максимальной длиной 25 символов
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={"class": "form-control mb-1", 'placeholder': 'E-Mail'}))
    to = forms.EmailField(required=True, widget=forms.TextInput(attrs={"class": "form-control mb-1", 'placeholder': 'Кому'}))
    comments = forms.CharField(required=False,
                               widget=forms.Textarea(attrs={"class": "form-control mb-1", 'placeholder': 'Комментарий'}))#задан конкретно-прикладной виджет прорисовки поля в HTML-элемент <textarea>


class CommentForm(forms.ModelForm):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': 'Имя'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"class": "form-control", 'placeholder': 'Email'}))
    body = forms.CharField(required=True,
                               widget=SummernoteWidget(
                                   attrs={"class": "form-control", 'summernote': {'width': '100%', 'height': '300px'}}))

    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']


class SearchForm(forms.Form): # Форма для поиска постов по ключевым словам
    query = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control mb-1", 'placeholder': 'Введите поисковый запрос...'}))
