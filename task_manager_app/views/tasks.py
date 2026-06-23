from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.db.models import Count
from django.db.models.functions import ExtractWeekDay
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend

from task_manager_app.models.task import Task, SubTask
from task_manager_app.serializers.task import (
    TaskCreateSerializer,
    TaskSerializer,
    SubTaskCreateSerializer,
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


class TaskListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskCreateSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']

    def get_queryset(self):
        queryset = Task.objects.all()
        day = self.request.query_params.get('day')
        if day:
            week_day = WEEK_DAY_MAP.get(day.lower())
            if week_day is None:
                raise ValidationError(
                    f"Invalid day '{day}'. Valid values: {', '.join(WEEK_DAY_MAP.keys())}"
                )
            queryset = queryset.annotate(week_day=ExtractWeekDay('deadline')).filter(week_day=week_day)
        return queryset


class TaskDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
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


class SubTaskListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubTaskCreateSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']

    def get_queryset(self):
        return SubTask.objects.all().order_by('-created_at')


class SubTaskDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = SubTask.objects.all()
    serializer_class = SubTaskCreateSerializer
