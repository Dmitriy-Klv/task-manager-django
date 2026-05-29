from django.db.models import Count
from django.urls import path
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from task_manager_app.models.task import Task
from task_manager_app.serializers.task import (
    TaskCreateSerializer,
    TaskListAllSerializer,
    TaskSerializer,
)


@api_view(["POST"])
def create_task(request: Request):
    serializer = TaskCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_all_tasks(request: Request):
    task = Task.objects.all()
    task_list = TaskListAllSerializer(task, many=True)
    return Response(task_list.data)


@api_view(["GET"])
def get_task(request: Request, task_id: int):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

    task_serializer = TaskSerializer(task)
    return Response(task_serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_tasks_total_count(request: Request):
    try:
        total_count = Task.objects.count()
        return Response({"total_count": total_count}, status=status.HTTP_200_OK)
    except Exception:
        return Response(
            {"error": "Failed to calculate the total number of tasks."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
def get_tasks_count_by_status(request: Request):
    try:
        query_stats = (
            Task.objects.values("status").annotate(count=Count("id")).order_by("status")
        )

        db_counts = {item["status"]: item["count"] for item in query_stats}

        status_choices = ["New", "In progress", "Pending", "Blocked", "Done"]
        response_data = {
            task_status: db_counts.get(task_status, 0) for task_status in status_choices
        }

        return Response(response_data, status=status.HTTP_200_OK)
    except Exception:
        return Response(
            {"error": "Failed to calculate task counts by status"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


urlpatterns = [
    path("tasks/count/status/", get_tasks_count_by_status, name="tasks-count-status"),
]


@api_view(["GET"])
def get_tasks_overdue_count(request: Request):
    try:
        now = timezone.now()
        overdue_count = (
            Task.objects.filter(deadline__lt=now).exclude(status="completed").count()
        )

        return Response({"overdue_count": overdue_count}, status=status.HTTP_200_OK)
    except Exception:
        return Response(
            {"error": "Failed to count tasks by status."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
