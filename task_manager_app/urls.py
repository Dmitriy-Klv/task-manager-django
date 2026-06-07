from django.urls import path

from task_manager_app.views.home_page import greetings
from task_manager_app.views.tasks import (
    create_task,
    get_all_tasks,
    get_task,
    get_tasks_statistics,
    SubTaskListCreateView,
    SubTaskDetailUpdateDeleteView,
)


urlpatterns = [
    path("home/", greetings),
    path("tasks/", get_all_tasks),
    path("tasks/create/", create_task),
    path("tasks/<int:pk>/", get_task, name="task-detail"),
    path("tasks/statistics/", get_tasks_statistics, name="tasks-statistics"),
    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:pk>/', SubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail-update-delete'),
]
