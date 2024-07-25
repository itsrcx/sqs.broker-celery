from django.http import JsonResponse
from rest_framework.decorators import api_view
from .tasks import dummy_task

@api_view(['POST'])
def send_task(request):
    # Extract data from the request
    data = request.data.get('data', 'default_data')

    # Send the task to Celery
    result = dummy_task.delay(data)
    
    return JsonResponse({
        'task_id': result.id,
        'status': 'Task sent to Celery'
    })