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
        fields = ('id', 'title', 'completed')


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
        
    # def update(self, instance, validated_data):
    #     status_id = validated_data.pop('status_id', None)
    #     print('StatusId neu:', status_id)
        
    #     if status_id:
    #         instance.status = Status.objects.get(id=status_id)

    #     # Hier aktualisieren Sie alle anderen Felder des Task-Modells
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)

    #     instance.save()
    #     return instance
    # 
    # 
    # def validate(self, data):
    #     data = super().validate(data) 
      
    #     # Your validation logic
    #     return data

    # def update_old(self, instance, validated_data):
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.description = validated_data.get('description', instance.description)
    
    #     category_data = validated_data.pop('category', None)
    #     print('validated data:', category_data)
        
            
    #     if category_data is not None:
       
    #         category_id = category_data.get('id', None)
    #         if category_id:
    #             try:
    #              category_instance = Category.objects.get(id=category_id)
    #              instance.category = category_instance
    #             except Category.DoesNotExist:
    #                 raise serializers.ValidationError("Category with id %s does not exist" % category_id)
       
    #     instance.dueDate = validated_data.get('dueDate', instance.dueDate)
    #     instance.priority = validated_data.get('priority', instance.priority)
    #    # instance.status = validated_data.get('status', instance.status)
    #     assigned = validated_data.pop('assigned', None)
    #     subtasks = validated_data.pop('subtasks', None)

    #     status_id = validated_data.pop('status_id', None)
       
      
        
    #     if status_id:
    #         instance.status = Status.objects.get(id=status_id)
        
    #     if assigned:
    #         instance.assigned.set(assigned)
   

    #     if subtasks is not None:
    #         for subtask_data in subtasks:
    #             subtask_id = subtask_data.get('id', None)
    #             if subtask_id:
    #                 try:
    #                     subtask = instance.subtasks.get(id=subtask_id)
    #                     for attr, value in subtask_data.items():
    #                         setattr(subtask, attr, value)
    #                     subtask.save()
    #                 except Subtask.DoesNotExist:
    #                     raise serializers.ValidationError("Subtask with id %s does not exist" % subtask_id)
    #             else:
    #                 # If the subtask does not exist, create it
    #                 Subtask.objects.create(user=instance.user, task=instance, **subtask_data)

    #     instance.save()
    #     return instance


    # def create(self, validated_data):
    #     assignees_data = validated_data.pop('assigned', None)
    #     subtasks_data = validated_data.pop('subtasks', None)
    #     task = Task.objects.create(**validated_data)
    #     if assignees_data:
    #         task.assignees.set(assignees_data)
    #     if subtasks_data:
    #         for subtask_data in subtasks_data:
    #             # You should include the user in the subtask_data
    #             Subtask.objects.create(task=task, **subtask_data)
    #     return task
    
# class TaskSerializer(serializers.ModelSerializer):
#     """Serializer for tasks."""

#     subtasks = SubtaskSerializer(many=True)

#     class Meta:
#         model = Task
#         fields = ['id', 'title', 'description', 'category', 'assignees', 'subtasks', 'due_date', 'priority', 'created_at', 'updated_at', 'list', 'order']
#         read_only_fields = ['id', 'created_at', 'updated_at']
#         write_only_fields = ['list']

#     def create(self, validated_data):
#         assignees_data = validated_data.pop('assignees', None)
#         subtasks_data = validated_data.pop('subtasks', None)
#         task = Task.objects.create(**validated_data)
#         if assignees_data:
#             task.assignees.set(assignees_data)
#         if subtasks_data:
#             for subtask_data in subtasks_data:
#                 # You should include the user in the subtask_data
#                 Subtask.objects.create(task=task, user=task.user, **subtask_data)
#         return task