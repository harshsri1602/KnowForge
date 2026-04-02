from celery import Celery

celery_app = Celery(
    "knowforge",
    broker="redis://127.0.0.1:6379/1",
    backend="redis://127.0.0.1:6379/1"
)

celery_app.conf.update(
    timezone="UTC",
    enable_utc=True,
)
celery_app.conf.imports = (
    "nlp.workers.tasks.document_tasks",
)
celery_app.conf.beat_schedule = {
    "poll-documents-every-10s": {
        "task": "nlp.workers.tasks.document_tasks.poll_documents",
        "schedule": 10.0,
    },
}