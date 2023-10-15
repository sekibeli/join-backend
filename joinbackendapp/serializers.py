from rest_framework import serializers
from .models import Task, Category, Contact, Subtask, Priority, Status

# Serialisierer für die verknüpften Modelle
class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields = '__all__'



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtask
        fields = ('id', 'title', 'completed')

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'

# Hauptserialisierer für das Task-Modell


class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
  

class ContactSerializer(serializers.ModelSerializer):
    # Hier verwenden wir 'TaskSerializer' als String. Die tatsächliche Bindung wird später erfolgen.
    tasks = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Contact
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    assigned = ContactSerializer(many=True, read_only=True)
    subtasks = SubtaskSerializer(many=True, read_only=True)  # Achten Sie darauf, dass Sie zuvor auch `SubtaskSerializer` definiert haben.
    priority = PrioritySerializer()
    status = StatusSerializer()

    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'author', 'created', 'due_date', 'category', 'assigned', 'subtasks', 'priority', 'status')
