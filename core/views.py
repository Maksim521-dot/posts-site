from django.shortcuts import render


def custom_404(request, exception):
    # Переменная exception содержит отладочную информацию;
    # выводить её в шаблон пользовательской страницы 404 мы не станем
    return render(request, 'core/404.html', {'path': request.path}, status=404)


def custom_403(request, reason=''):
    return render(request, 'core/404.html', {'path': request.path}, status=403)


def custom_500(request, reason=''):
    return render(request, 'core/404.html', {'path': request.path}, status=500)
