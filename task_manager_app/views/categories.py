from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Count

from task_manager_app.models.category import Category
from task_manager_app.serializers.task import CategoryCreateSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer

    @action(detail=False, methods=['get'])
    def count_tasks(self, request):
        categories = Category.objects.annotate(task_count=Count('task'))
        data = [
            {
                "id": cat.id,
                "name": cat.name,
                "task_count": cat.task_count,
            }
            for cat in categories
        ]
        return Response(data)
