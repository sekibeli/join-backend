from rest_framework.response import Response
from rest_framework import status as http_status



def create_task_for_user(current_user, request, self):
    task_data = request.data
    category = self.validate_category(task_data)
    priority_value = self.validate_priority(task_data)
    status_data = self.validate_status(task_data)
    task = self.create_task(task_data, category, priority_value, status_data, current_user)
    self.assign_task(task, task_data)
    self.create_subtasks(task, task_data)
    return Response(status=http_status.HTTP_201_CREATED)



