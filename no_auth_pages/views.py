from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'no_auth_pages/index.html')


def error_404_view(request, exception):
    return render(request, 'no_auth_pages/404.html')