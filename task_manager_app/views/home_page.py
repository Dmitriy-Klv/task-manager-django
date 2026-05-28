from django.http import HttpRequest, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response


def greetings(request: HttpRequest) -> HttpResponse:
    return HttpResponse("<h1>Hello from our first view!</h1>")