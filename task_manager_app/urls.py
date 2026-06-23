from django.urls import path, include
from rest_framework.routers import DefaultRouter

from task_manager_app.views.home_page import greetings
from task_manager_app.views.tasks import (
    TaskListCreateView,
    TaskDetailView,
    MyTaskListView,
    get_tasks_statistics,
    SubTaskListCreateView,
    SubTaskDetailView,
)

from task_manager_app.views.categories import CategoryViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path("home/", greetings, name="greetings"),
    path("tasks/", TaskListCreateView.as_view(), name="task-list-create"),
    path("tasks/my/", MyTaskListView.as_view(), name="my-task-list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/statistics/", get_tasks_statistics, name="tasks-statistics"),
    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:pk>/', SubTaskDetailView.as_view(), name='subtask-detail-update-delete'),
    path('', include(router.urls)),
]
