from django.http import HttpResponse


def hello_world(request):
    print(111)
    return HttpResponse('Hello World')
