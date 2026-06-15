from django.urls import path, include
from rest_framework.routers import DefaultRouter

from task_manager_app.views.home_page import greetings
from task_manager_app.views.tasks import (
    create_task,
    get_all_tasks,
    get_task,
    get_tasks_statistics,
    SubTaskListCreateView,
    SubTaskDetailUpdateDeleteView,
)
from task_manager_app.views.categories import CategoryViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path("home/", greetings, name="greetings"),
    path("tasks/", get_all_tasks, name="task-list"),
    path("tasks/create/", create_task, name="task-create"),
    path("tasks/<int:pk>/", get_task, name="task-detail"),
    path("tasks/statistics/", get_tasks_statistics, name="tasks-statistics"),
    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:pk>/', SubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail-update-delete'),
    path('', include(router.urls)),
]
