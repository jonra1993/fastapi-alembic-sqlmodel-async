import time
from app.core.celery import celery

@celery.task(name="increment_a_value")
def increment(value: int) -> int:
    time.sleep(5)
    new_value = value + 1
    print("new_value", new_value)
    return new_value
