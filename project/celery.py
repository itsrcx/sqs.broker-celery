import os
from django.conf import settings
from celery import Celery
from kombu.utils.url import safequote

from dotenv import load_dotenv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

aws_access_key = safequote(os.getenv("KEY"))
aws_secret_key = safequote(os.getenv("SECRET"))

app = Celery("project")
app.conf.enable_utc = False
app.conf.update(timezone="Asia/Kolkata")

app.config_from_object("project.settings")

app.conf["broker_transport_options"] = {
    "fanout_prefix": True,
    "fanout_patterns": True,
    "max_connections": 1,
    "socket_keepalive": True,
}

SQS_QUEUE = 'sqs_queue'

app.conf.update(
    task_default_queue=SQS_QUEUE,
)

app.conf.update(
    broker_url=f"sqs://{aws_access_key}:{aws_secret_key}@", 
    broker_transport_options = {
        'region': 'us-east-2',
        'predefined_queues': {
            SQS_QUEUE: {
                'url': 'https://sqs.us-east-2.amazonaws.com/931637813668/sqs_queue',
                'access_key_id': os.getenv("KEY"),
                'secret_access_key': os.getenv("SECRET")
            }
        }
    }
)

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
