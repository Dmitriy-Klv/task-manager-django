from rest_framework import status
from rest_framework.decorators import api_view
from task_manager_app.models.task import Task
from task_manager_app.serializers.task import TaskCreateSerializer
from rest_framework.response import Response
from rest_framework.request import Request


@api_view(["POST"])
def create_task(request):
    serializer = TaskCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)