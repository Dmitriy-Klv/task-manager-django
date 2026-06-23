from django.db.models.fields import CharField
from rest_framework import serializers
from django.utils import timezone

from task_manager_app.models.task import Task, SubTask
from task_manager_app.models.category import Category


class TaskCreateSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Task
        fields = ["id", "title", "description", "status", "deadline", "owner"]

    def validate_deadline(self, value):
        if value and value < timezone.now():
            raise serializers.ValidationError("The deadline cannot be in the past.")

        return value


class TaskListAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
        ]


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "description", "status", "deadline"]


class SubTaskCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = SubTask
        fields = ["id", "title", "description", "status", "deadline", "created_at", "owner"]


class CategoryCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name']

    def create(self, validated_data):
        name = validated_data.get('name')
        if Category.objects.filter(name__iexact=name).exists():
            raise serializers.ValidationError({"name": "A category with this name already exists"})
        return super().create(validated_data)


    def update(self, instance, validated_data):
        name = validated_data.get('name')
        if name:
            if Category.objects.filter(name__iexact=name).exclude(id=instance.id).exists():
                raise serializers.ValidationError({"name": "A category with this name already exists"})
        return super().update(instance, validated_data)


class TaskDetailSerializer(serializers.ModelSerializer):
    subtask = SubTaskCreateSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = '__all__'
