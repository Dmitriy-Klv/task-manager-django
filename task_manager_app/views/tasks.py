from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.db.models.functions import ExtractWeekDay
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


from task_manager_app.models.task import Task, SubTask
from task_manager_app.serializers.task import (
    TaskCreateSerializer,
    TaskListAllSerializer,
    TaskSerializer,
    SubTaskCreateSerializer
)

WEEK_DAY_MAP = {
    'sunday': 1,
    'monday': 2,
    'tuesday': 3,
    'wednesday': 4,
    'thursday': 5,
    'friday': 6,
    'saturday': 7,
}


@api_view(["POST"])
def create_task(request: Request):
    serializer = TaskCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_all_tasks(request: Request):
    day = request.query_params.get("day")
    tasks = Task.objects.all()

    if day:
        week_day = WEEK_DAY_MAP.get(day.lower())
        if week_day is None:
            return Response(
                {"error": f"Invalid day '{day}'. Valid values: {', '.join(WEEK_DAY_MAP.keys())}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        tasks = tasks.annotate(week_day=ExtractWeekDay('deadline')).filter(week_day=week_day)

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

        status_choices = ["New", "In progress", "Blocked", "Pending", "Done"]
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


class SubTaskListCreateView(APIView, PageNumberPagination):
    page_size = 5

    def get(self, request: Request):
        filters = {}
        task_title = request.query_params.get('task_title')
        status_val = request.query_params.get('status')

        if task_title:
            filters['task__title__icontains'] = task_title

        if status_val:
            filters['status'] = status_val

        queryset = SubTask.objects.filter(**filters).order_by('-created_at')

        result_page = self.paginate_queryset(queryset, request, view=self)
        serializer = SubTaskCreateSerializer(result_page, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request: Request):
        serializer = SubTaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubTaskDetailUpdateDeleteView(APIView):
    def get(self, request: Request, pk: int):
        subtask = get_object_or_404(SubTask, pk=pk)
        serializer = SubTaskCreateSerializer(subtask)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request: Request, pk: int):
        subtask = get_object_or_404(SubTask, pk=pk)
        serializer = SubTaskCreateSerializer(subtask, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, pk: int):
        subtask = get_object_or_404(SubTask, pk=pk)
        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
