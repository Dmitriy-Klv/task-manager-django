from django.urls import path

from task_manager_app.views.home_page import greetings
from task_manager_app.views.tasks import (
    create_task,
    get_all_tasks,
    get_task,
    get_tasks_count_by_status,
    get_tasks_overdue_count,
    get_tasks_total_count,
)

urlpatterns = [
    path("home/", greetings),
    path("tasks/", get_all_tasks),
    path("tasks/create/", create_task),
    path("tasks/<int:pk>/", get_task, name="task-detail"),
    path("tasks/count/total/", get_tasks_total_count, name="tasks-count-total"),
    path("tasks/count/status/", get_tasks_count_by_status, name="tasks-count-status"),
    path("tasks/count/delayed/", get_tasks_overdue_count, name="tasks-count-delayed"),
]
