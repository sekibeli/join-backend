from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task, Category, Contact, Subtask, Priority, Status

# Serialisierer für die verknüpften Modelle

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')
        

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title','color','author')

class SubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtask
        fields = ('id', 'title', 'completed', 'task')


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
    # category = CategorySerializer()
    assigned = serializers.PrimaryKeyRelatedField(many=True,  queryset=Contact.objects.all())
    subtasks = serializers.PrimaryKeyRelatedField(many=True,  queryset=Subtask.objects.all())
    #priority = PrioritySerializer()
    #status = StatusSerializer()
   # status_id = serializers.IntegerField(write_only=True, required=False)
   
   
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'author', 'created', 'dueDate', 'category','assigned', 'subtasks', 'priority', 'status')
        
    