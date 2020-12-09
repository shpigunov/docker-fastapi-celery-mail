import json
from celery import Celery


from celery.utils.log import get_task_logger

import backends

# Create the celery app and get the logger
celery_app = Celery('tasks', broker='pyamqp://guest@rabbit//')
logger = get_task_logger(__name__)


@celery_app.task(name="send", bind=True)
def send(self, msg):

    # Loop through available backends to try and send the message
    for backend_callable in backends.backend_list:
        response = backend_callable(msg)

        # Debug output
        logger.info(
            f"Backend responded: {response.status_code}: {response.content}")

        # Report success and return from execution
        if response.status_code in {200, 201}:
            logger.info("Message sent")
            logger.info(json.dumps(msg))
            return 0

    # Finally, if all backends fail, re-enqueue the task
    logger.info("Message failed to send")
    self.retry(countdown=60*10)

    return -1
