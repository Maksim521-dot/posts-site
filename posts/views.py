from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.core.paginator import Paginator
from datetime import datetime


# Create your views here.
def paginator(queryset, request):
    paginator = Paginator(queryset, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'paginator': paginator,
        'page_number': page_number,
        'page_obj': page_obj
    }
    return context


def ban_info_1(request):
    ban_user = None
    reason = None
    if request.user.is_authenticated:
        ban_user = Ban.objects.filter(user=request.user).exists()
        if Ban.objects.filter(user=request.user).exists():
            bans = get_object_or_404(Ban, user=request.user)
            reason = bans.reason
        else:
            reason = None
    else:
        ban_user = None
    return reason


def ban_info_2(request):
    ban_user = None
    reason = None
    if request.user.is_authenticated:
        ban_user = Ban.objects.filter(user=request.user).exists()
        if Ban.objects.filter(user=request.user).exists():
            bans = get_object_or_404(Ban, user=request.user)
            reason = bans.reason
        else:
            reason = None
    else:
        ban_user = None
    return ban_user


def mute_info_1(request):
    mute_user = None
    reason = None
    if request.user.is_authenticated:
        mute_user = Mute.objects.filter(user=request.user).exists()
        if Mute.objects.filter(user=request.user).exists():
            bans = get_object_or_404(Mute, user=request.user)
            reason = bans.reason
        else:
            reason = None
    else:
        mute_user = None
    return reason


def mute_info_2(request):
    mute_user = None
    reason = None
    if request.user.is_authenticated:
        mute_user = Mute.objects.filter(user=request.user).exists()
        if Mute.objects.filter(user=request.user).exists():
            bans = get_object_or_404(Mute, user=request.user)
            reason = bans.reason
        else:
            reason = None
    else:
        mute_user = None
    return mute_user


def index(request):
    posts_list = Post.objects.all().order_by('-date')
    paginator = Paginator(posts_list, 5)
    reason = None
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    reason = ban_info_1(request)
    ban_user = ban_info_2(request)
    user_set = set()  # Создаем множество для хранения уникальных пользователей
    image_profiles = []
    if request.method == 'GET':
        if not Rank.objects.filter(username=request.user).exists():
            rank = Rank.objects.create(username=request.user, rank="Новичок")
            rank.save()
    for post in posts_list:
        user = post.user
        if user not in user_set:  # Проверяем, добавлен ли уже пользователь
            user_set.add(user)
            if ImageProfile.objects.filter(username=user).exists():
                img = ImageProfile.objects.get(username=user)
                image_profiles.append(img)
    context = {
        'page_obj': page_obj,
        'ban_user': ban_user,
        'reason': reason,
        'image_profiles': image_profiles
    }
    return render(request, 'posts/index.html', context)


def image_profile(request, username):
    img = None
    user = User.objects.get(username=username)
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ImgForm(request.POST)
            if form.is_valid():
                img = form.cleaned_data['image']
                if ImageProfile.objects.filter(username=user).exists():
                    img_create1 = ImageProfile.objects.get(username=user)
                    img_create1.delete()
                img_create = ImageProfile.objects.create(username=user, image=img)
                img_create.save()
                return redirect('posts:my_posts')
            else:
                form = ImgForm()
        else:
            return redirect('posts:index')
    else:
        return redirect('users:signup')
    context = {
        'form': form
    }
    return render(request, 'posts/img_profile.html', context)


def post_create(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                text = form.cleaned_data['text']
                img = form.cleaned_data['img']
                group = form.cleaned_data['group']
                post_obj = Post.objects.create(name=name, text=text, user=request.user, img=img, group=group)
                post_obj.save()
                return redirect('posts:index')
            else:
                form = PostForm()
        if request.method == 'GET':
            return redirect('posts:index')
    else:
        return redirect('posts:index')
    reason = ban_info_1(request)
    ban_user = ban_info_2(request)
    reason_mute = mute_info_1(request)
    mute_user = mute_info_2(request)
    context = {
        'reason': reason,
        'ban_user': ban_user,
        'form': form,
        'reason_mute': reason_mute,
        'mute_user': mute_user
    }
    return render(request, 'posts/post_create.html', context)


def post_user(request):
    ban_user = Ban.objects.filter(user=request.user).exists()
    img_obj = "https://ibbea.fcen.uba.ar/wp-content/uploads/2015/06/Pessoa_Neutra23.png"
    if ImageProfile.objects.filter(username=request.user):
        img = ImageProfile.objects.get(username=request.user)
        img_obj = img.image
    if request.user.is_authenticated:
        my_posts = Post.objects.filter(user=request.user).order_by('-date')
    else:
        return redirect('users:signup')
    reason = ban_info_1(request)
    ban_user = ban_info_2(request)
    context = {
        'my_posts': my_posts,
        'ban_user': ban_user,
        'reason': reason,
        'img_obj': img_obj
    }
    return render(request, 'posts/post_user.html', context)


def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('posts:index')
    else:
        return redirect('posts:index')


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST or None, instance=post, files=request.FILES or None)
        if form.is_valid():
            form.save()
            return redirect('posts:index')
        else:
            form = PostForm(instance=post)
    if request.method == 'GET':
        return redirect('posts:index')
    reason = ban_info_1(request)
    ban_user = ban_info_2(request)
    reason_mute = mute_info_1(request)
    mute_user = mute_info_2(request)
    context = {
        'post': post,
        'form': form,
        'reason': reason,
        'ban_user': ban_user,
        'reason_mute': reason_mute,
        'mute_user': mute_user
    }
    return render(request, 'posts/post_edit.html', context)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post_user = post.user
    views = post.views
    img = ImageProfile.objects.get(username=post_user)
    img_obj = img.image
    comments = Comment.objects.filter(post=post)
    like_counter = Like.objects.filter(post=post).count()
    if request.user.is_authenticated:
        comment_exist = Like.objects.filter(post=post, user=request.user).exists()
    else:
        comment_exist = Like.objects.filter(post=post).exists()
    if request.method == 'POST':
        views += 1
        post.views = views
        post.save()
    context = {
        'post': post,
        'comments': comments,
        'like_counter': like_counter,
        'comment_exist': comment_exist,
        'img_obj': img_obj,
    }
    return render(request, 'posts/post_detail.html', context)


def chat(request, user2):
    user1_obj = request.user
    user2_obj = User.objects.get(username=user2)
    chat_obj = None
    form = None
    current_datetime = datetime.now()
    current_date = current_datetime.date()
    img_1 = ImageProfile.objects.get(username=user1_obj)
    img_obj_1 = img_1.image
    img_2 = ImageProfile.objects.get(username=user2_obj)
    img_obj_2 = img_2.image 
    chat_message_all = Chat.objects.filter(user1=user1_obj, user2=user2_obj) | Chat.objects.filter(user1=user2_obj, user2=user1_obj).order_by('-pk')
    if request.method == 'POST':
        if request.user == user1_obj or request.user == user2_obj:
            form = ChatForm(request.POST)
            if form.is_valid():
                message = form.cleaned_data['message']
                chat_obj = Chat.objects.create(user1=user1_obj, user2=user2_obj, message=message)
                chat_obj.save()
                if not ChatList.objects.filter(chat_user1=user1_obj, chat_user2=user2_obj).exists():
                    create_chat1 = ChatList.objects.create(chat_user1=user1_obj, chat_user2=user2_obj)
                    create_chat1.save()
                    create_chat2 = ChatList.objects.create(chat_user1=user2_obj, chat_user2=user1_obj)
                    create_chat2.save()
            else:
                form = ChatForm()
        else:
            return redirect('posts:index')
    else:
        if request.user == user1_obj or request.user == user2_obj:
            form = ChatForm()
        else:
            return redirect('posts:index')
    context = {
        'form': form,
        'chat_message_all': chat_message_all,
        'user1_obj': user1_obj,
        'user2_obj': user2_obj,
        'current_date': current_date,
        'img_obj_1': img_obj_1,
        'img_obj_2': img_obj_2
    }
    return render(request, 'posts/chat.html', context)


def chat_message_delete(request, msg_pk):
    chat_msg = Chat.objects.get(pk=msg_pk)
    user2 = chat_msg.user2
    if request.method == 'POST':
        chat_msg.delete()
        return redirect('posts:chat', user2=user2)
    return redirect('posts:chat', user2=user2)


def chat_list(request):
    chat_list = ChatList.objects.filter(chat_user1=request.user)
    counter = chat_list.count()
    list_global = []
    for element in chat_list:
        list_pk = []
        user2 = element.chat_user2
        object_list = Chat.objects.filter(user1=request.user, user2=user2) | Chat.objects.filter(user1=user2, user2=request.user)
        if object_list:  # Проверяем, что object_list не пуст
            for el in object_list:
                pk = el.pk
                list_pk.append(pk)
            if list_pk:  # Проверяем, что list_pk не пуст перед поиском максимального значения
                max_pk = max(list_pk)
                max_element = Chat.objects.get(pk=max_pk)
                list_global.append(max_element)
    list_global = list(reversed(list_global))
    reason = ban_info_1(request)
    ban_user = ban_info_2(request)
    context = {
        'chat_list': chat_list,
        'counter': counter,
        'reason': reason,
        'ban_user': ban_user,
        'list_global': list_global  # Список из последних сообщений каждого чата
    }
    return render(request, 'posts/chat_list.html', context)


def comments(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CommentForm(request.POST or None)
            if form.is_valid():
                text = form.cleaned_data['text']
                comments = Comment.objects.create(user=request.user, text=text, post=post)
                comments.save()
                return redirect('posts:post_detail', pk=pk)
            else:
                form = CommentForm()
    else:
        return redirect('users:signup')
    context = {
        'form': form,
        'post': post
    }
    return render(request, 'posts/comment.html', context)


def delete_comments(request, pk, post_id):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user.is_authenticated:
        if request.method == 'POST':
            comment.delete()
            return redirect('posts:post_detail', post_id)
        else:
            return redirect('posts:index')
    else:
        return redirect('posts:index')


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.group.all().order_by('-pk')
    context = paginator(posts, request)
    return render(request, 'posts/group_posts.html', context)


def post_author(request, user_post):
    if request.user.is_authenticated:
        user_request = request.user
        user_obj = User.objects.get(username=user_post)
        img = ImageProfile.objects.get(username=user_obj)
        img_obj = img.image
        ban_user = Ban.objects.filter(user=user_obj).exists()
        mute_user = Mute.objects.filter(user=user_obj).exists()
        posts = Post.objects.filter(user=user_obj).order_by('-date')
        counter = Post.objects.filter(user=user_obj).count()
        rank_obj = None
        if Rank.objects.filter(username=user_obj).exists():
            rank_obj = Rank.objects.get(username=user_obj)
            if counter == 0:
                rank_update = "Новичок"
                rank_update_img = "|"
                rank_obj.rank = rank_update
                rank_obj.rank_img = rank_update_img
                rank_obj.save()
            if counter == 1:
                rank_update = "Новичок"
                rank_update_img = "⭑"
                rank_obj.rank = rank_update
                rank_obj.rank_img = rank_update_img
                rank_obj.save()
            if counter == 2:
                rank_update = "Исследователь"
                rank_update_img = "⭑ ⭑"
                rank_obj.rank = rank_update
                rank_obj.rank_img = rank_update_img
                rank_obj.save()
            if counter == 3:
                rank_update = "Ученик"
                rank_update_img = "⭑ ⭑ ⭑"
                rank_obj.rank = rank_update
                rank_obj.rank_img = rank_update_img
                rank_obj.save()
            if counter == 4:
                rank_update = "Знаток"
                rank_update_img = "⋆"
                rank_obj.rank = rank_update
                rank_obj.rank_img = rank_update_img
                rank_obj.save()
            if counter == 5:
                rank_update = "Мастер"
                rank_update_img = "⋆ ⋆"
                rank_obj.rank = rank_update
                rank_obj.rank_img = rank_update_img
                rank_obj.save()
            if counter == 6:
                rank_update = "Эксперт"
                rank_update_img = "⋆ ⋆ ⋆"
                rank_obj.rank = rank_update
                rank_obj.rank_img = rank_update_img
                rank_obj.save()
            if counter == 7:
                rank_update = "Мудрец"
                rank_update_img = "★"
                rank_obj.rank = rank_update
                rank_obj.rank_img = rank_update_img
                rank_obj.save()
            if counter == 8:
                rank_update = "Ветеран"
                rank_update_img = "★ ★"
                rank_obj.rank = rank_update
                rank_obj.rank_img = rank_update_img
                rank_obj.save()
            if counter == 9:
                rank_update = "Легенда"
                rank_update_img = "★ ★ ★"
                rank_obj.rank = rank_update
                rank_obj.rank_img = rank_update_img
                rank_obj.save()
            if counter == 10:
                rank_update = "Бессменный"
                rank_update_img = "˗ˏˋ ✶ ✶ ✶ ˎˊ˗"
                rank_obj.rank = rank_update
                rank_obj.rank_img = rank_update_img
                rank_obj.save()
            if user_obj.is_superuser:
                rank_update = "Администратор"
                rank_update_img = "── ✶⋅★⋅✶ ──"
                rank_obj.rank = rank_update
                rank_obj.rank_img = rank_update_img
                rank_obj.save()
        follow_exist = Follow.objects.filter(author=user_obj, user=request.user).exists()
        counter_follow = Follow.objects.filter(author=user_obj, user=request.user).count()
        context = {
            'posts': posts,
            'user_post': user_post,
            'counter': counter,
            'follow_exist': follow_exist,
            'counter_follow': counter_follow,
            'ban_user': ban_user,
            'mute_user': mute_user,
            'user_request': user_request,
            'img_obj': img_obj,
            'rank_obj': rank_obj
        }
        return render(request, 'posts/post_author.html', context)
    else:
        return redirect('users:signup')


def ban_error(request):
    return render(request, 'posts/ban_error.html')


def ban(request, user):
    ban_user = get_object_or_404(User, username=user)
    if request.method == 'POST':
        if not Ban.objects.filter(user=ban_user).exists():
            form = BanForm(request.POST)
            if form.is_valid():
                reason = form.cleaned_data['reason']
                ban = Ban.objects.create(user=ban_user, reason=reason)
                ban.save()
                return redirect('posts:post_author', user_post=user)
            else:
                form = BanForm()
        else:
            ban = get_object_or_404(Ban, user=ban_user)
            ban.delete()
            return redirect('posts:post_author', user_post=user)
    else:
        return redirect('posts:index')
    context = {
        'form': form,
        'ban_user': ban_user 
    }
    return render(request, 'posts/ban.html', context)


def mute(request, user):
    mute_user = get_object_or_404(User, username=user)
    if request.method == 'POST':
        if not Mute.objects.filter(user=mute_user).exists():
            form = MuteForm(request.POST)
            if form.is_valid():
                reason = form.cleaned_data['reason']
                mute = Mute.objects.create(user=mute_user, reason=reason)
                mute.save()
                return redirect('posts:post_author', user_post=user)
            else:
                form = MuteForm()
        else:
            ban = get_object_or_404(Mute, user=mute_user)
            ban.delete()
            return redirect('posts:post_author', user_post=user)
    else:
        return redirect('posts:index')
    context = {
        'form': form,
        'mute_user': mute_user
    }
    return render(request, 'posts/mute.html', context)


def follow(request, user):
    user_obj = User.objects.get(username=user)
    if request.method == 'POST':
        if request.user != user_obj:
            if not Follow.objects.filter(author=user_obj, user=request.user).exists():
                follow = Follow.objects.create(author=user_obj, user=request.user)
                follow.save()
                return redirect('posts:post_author', user)
            else:
                follow_obj = Follow.objects.get(author=user_obj, user=request.user)
                follow_obj.delete()
                return redirect('posts:post_author', user)
        else:
            return redirect('posts:index')
    else:
        return redirect('posts:index')


def follow_list(request):
    list = Follow.objects.filter(user=request.user)
    reason = ban_info_1(request)
    ban_user = ban_info_2(request)
    counter = list.count()
    context = {
        'list': list,
        'counter': counter,
        'ban_user': ban_user,
        'reason': reason
    }
    return render(request, 'posts/follow_list.html', context)


def like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        if not Like.objects.filter(user=request.user, post=post).exists():
            like = Like.objects.create(post=post, user=request.user)
            like.save()
        else:
            unlike = Like.objects.get(user=request.user, post=post)
            unlike.delete()
    return redirect('posts:post_detail', pk=pk)


def search(request):
    form = Search(request.POST)
    search_obj = "Ничего не найдено"
    reason = ban_info_1(request)
    ban_user = ban_info_2(request)
    if form.is_valid():
        search_name = form.cleaned_data['search']
        search_obj = Post.objects.filter(name=search_name)
    else:
        form = Search()
    context = {
        'search_obj': search_obj,
        'form': form,
        'ban_user': ban_user,
        'reason': reason
    }
    return render(request, 'posts/search_name.html', context)


def signup_next(request):
    return redirect('posts:index')
