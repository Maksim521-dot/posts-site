from django import forms
from .models import *


class PostForm(forms.ModelForm):
    name = forms.CharField(max_length=50, label="Введите название поста")
    group = forms.ModelChoiceField(queryset=Group.objects.all(), label="Группа", empty_label="Группа не выбрана")
    text = forms.CharField(widget=forms.Textarea(), label="Введите текст поста")
    img = forms.CharField(widget=forms.Textarea(), label="Введите ссылку на фото")

    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['user', 'views']


class BanForm(forms.ModelForm):
    class Meta:
        model = Ban
        fields = '__all__'
        exclude = ['user']


class MuteForm(forms.ModelForm):
    class Meta:
        model = Mute
        fields = '__all__'
        exclude = ['user']


class ImgForm(forms.ModelForm):
    class Meta:
        model = ImageProfile
        fields = '__all__'
        exclude = ['username']


class CommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(), label="Текст комментария")


class Search(forms.Form):
    search = forms.CharField(max_length=25, label="Поиск", required=True)


class ChatForm(forms.Form):
    message = forms.CharField(max_length=150, label="Сообщение")
