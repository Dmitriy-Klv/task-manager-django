from django.contrib import admin
from django.urls import path

from task_manager_app.views.home_page import greetings
from task_manager_app.views.tasks import create_task

urlpatterns = [
    path("home-page/", greetings),
    path("create-task/", create_task),
]