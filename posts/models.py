from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

User = get_user_model()


class Group(models.Model):
    name = models.CharField(max_length=25, verbose_name="Название группы", help_text="Укажите название группы")
    slug = models.SlugField(max_length=50, unique=True, verbose_name="Slug", help_text="Укажите Slug")

    class Meta:
        verbose_name_plural = "Группы"

    def __str__(self):
        return self.name


class Rank(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    rank = models.CharField(max_length=50, verbose_name="Звание")
    date = models.DateTimeField(verbose_name="Дата получения звания", auto_now_add=True)
    rank_img = models.CharField(verbose_name="Значок звания", max_length=50, default="┃")

    class Meta:
        verbose_name_plural = "Звания"
        verbose_name = "Звание"


class Post(models.Model):
    name = models.CharField(verbose_name="Название поста", help_text="Введите название поста", max_length=25)
    text = models.TextField(verbose_name="Текст поста", help_text="Введите текст поста")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор поста")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name="Группа", default=None, related_name="group")
    date = models.DateTimeField(verbose_name="Дата публикации", auto_now_add=True)
    img = models.TextField(verbose_name="Ссылка на фото", help_text="Введите ссылку на фото")
    views = models.IntegerField(verbose_name="Просмотры", default=0)

    class Meta:
        verbose_name_plural = "Посты"
        ordering = ('date',)
    
    def __str__(self) -> str:
        return self.text[:15]


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="Пост", related_name="comments", default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    text = models.TextField(verbose_name="Комментарий")
    date = models.DateTimeField(verbose_name="Дата", auto_now_add=True)

    class Meta:
        verbose_name_plural = "Комментарии"
        ordering = ('date',)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="Пост")

    class Meta:
        verbose_name_plural = "Лайки"


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Подписчик", related_name="user")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор", related_name="author")

    class Meta:
        verbose_name_plural = "Подписки"


class Ban(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь", help_text="Укажите пользователя")
    reason = models.CharField(max_length=50, verbose_name="Причина", default="Причина не указана")

    class Meta:
        verbose_name_plural = "Блокировки"


class Mute(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь", help_text="Укажите пользователя")
    reason = models.CharField(max_length=50, verbose_name="Причина", default="Причина не указана")

    class Meta:
        verbose_name_plural = "Муты"


class Chat(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь 1", related_name="user1")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь 2", related_name="user2")
    message = models.TextField(verbose_name="Сообщение")
    date = models.DateField(verbose_name="Дата", auto_now_add=True)

    class Meta:
        verbose_name_plural = "Сообщения"
        verbose_name = "Сообщение"


class ChatList(models.Model):
    chat_user1 = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь 1", related_name="chat_user1")
    chat_user2 = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь 2", related_name="chat_user2")

    class Meta:
        verbose_name_plural = "Чаты"
        verbose_name = "Чат"


class ImageProfile(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    image = models.CharField(max_length=200, verbose_name="Фото профиля", help_text="Введите ссылку на фото", default="https://ibbea.fcen.uba.ar/wp-content/uploads/2015/06/Pessoa_Neutra23.png")

    class Meta:
        verbose_name_plural = "Фотографии профилей"
        verbose_name = "Фото"
