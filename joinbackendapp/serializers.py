from rest_framework import serializers
from .models import Task, Category, Contact, Subtask, Priority, Status

# Serialisierer für die verknüpften Modelle
class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtask
        fields = '__all__'

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'

# Hauptserialisierer für das Task-Modell
class TaskSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    assigned = ContactSerializer()
    subtask = SubtaskSerializer()
    priority = PrioritySerializer()
    status = StatusSerializer()

    class Meta:
        model = Task
        fields = '__all__'

class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'