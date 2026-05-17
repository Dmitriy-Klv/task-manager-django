from django.http import HttpRequest, HttpResponse


def greetings(request: HttpRequest) -> HttpResponse:
    return HttpResponse("<h1>Hello from our first view!</h1>")
