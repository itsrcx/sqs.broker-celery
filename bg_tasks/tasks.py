from celery import shared_task

@shared_task
def dummy_task(data):
    # Simulate some processing
    print(f"Processing data: {data}")
    return f"Processed: {data}"