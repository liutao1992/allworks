from django.shortcuts import render


def home(request):
    """
    render home template
    :param request:
    :return:
    """

    return render(request, 'index/home.html')