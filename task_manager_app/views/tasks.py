from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from task_manager_app.models.task import Task, SubTask
from task_manager_app.serializers.task import (
    TaskCreateSerializer,
    TaskListAllSerializer,
    TaskSerializer,
    SubTaskCreateSerializer
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
    tasks = Task.objects.all()
    serializer = TaskListAllSerializer(tasks, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_task(request: Request, pk: int):
    try:
        task = Task.objects.get(id=pk)
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = TaskSerializer(task)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_tasks_statistics(request: Request):
    try:
        now = timezone.now()

        total_count = Task.objects.count()

        status_choices = ["New", "In progress", "Pending", "Blocked", "Done"]
        query_stats = (
            Task.objects.values("status")
            .annotate(count=Count("id"))
            .order_by("status")
        )
        db_counts = {item["status"]: item["count"] for item in query_stats}
        status_counts = {
            task_status: db_counts.get(task_status, 0) for task_status in status_choices
        }

        overdue_count = (
            Task.objects.filter(deadline__lt=now)
            .exclude(status="Done")
            .count()
        )

        statistics = {
            "total_count": total_count,
            "status_counts": status_counts,
            "overdue_count": overdue_count,
        }

        return Response(statistics, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {"error": f"Failed to calculate tasks statistics: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


class SubTaskListCreateView(APIView):
    def get(self, request):
        subtask = SubTask.objects.all()
        serializer = SubTaskCreateSerializer(subtask, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SubTaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubTaskDetailUpdateDeleteView(APIView):
    def get(self, request, pk):
        subtask = get_object_or_404(SubTask, pk=pk)
        serializer = SubTaskCreateSerializer(subtask)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        subtask = get_object_or_404(SubTask, pk=pk)
        serializer = SubTaskCreateSerializer(subtask, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        subtask = get_object_or_404(SubTask, pk=pk)
        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


