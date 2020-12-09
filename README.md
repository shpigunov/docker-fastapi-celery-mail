# Distributed Mailer Demo

## Purpose

Implementation of a RESTful endpoint that accepts a JSON request, validates it and forwards it to one of email backends for sending.

## Technical challenge and Conceptual solution

External email providers may become unresponsive or unreliable, and there is no guarantee that our app can get a fast, or any response, within a timeframe accebrable for the HTTP request-response cycle. The situation can be further aggravated in case of higher traffic.

Therefore, we believe that it would be unsuitable to "simply" iterate through the email backends from the view/endpoint logic, because any delays here would hold the HTTP response and create an impression of sluggishness for the end user.

Instead, we propose to use a **task queue**, where the RESTful endpoint is the **producer** and the task worker is the **consumer**. A successful request to the endpoint will **enqueue** the task, and the worker will **consume** the task, try to complete it, but in case of failure, the worker will **re-enqueue** the task for a certain number of retries.

## Package selection and discussion

### Web framework - Django vs. FastAPI

Although `Django` and its `REST Framework` is more widespread, `FastAPI` was selected becuase it's:

1. stateless and doesn't require a database backend;
2. uses `pydantic` for type checking and built-in validation;
3. requires less setup and configurations;

### Task Queue - Celery vs. self-written

`celery` is selected as an abstraction layer over the message queue to handle task enqueuing and consumption. This package does create additional complexity and requires additional dependencies, but it is robust, easily scalable, well documented and allows for a faster development time.

### Message backend - RabbitMQ vs. Redis

Although `redis` is simpler and more lightweight, it does not (easily) provide persistency, and therefore `rabbitmq` is used instead.

### Service orchestration - Docker-compose

`docker-compose` is an obvious choice to orchestrate several heterogeneous services and make them interoperate in an ensebmle, regardless of the environment.

### Python dependency management - poetry

`poetry` is suggested, because it resolves and locks Python dependencies, and manages virtual environments. `pip-tools` + `venv` can do the same, in two packages, but with a bit more manual work.

## Code organization

- `docker-compose.yml` - servcie images used in the project;
- `Dockerfile` - to build the app image;
- `pyproject.toml` - python requirements for the app;
- `app.py` - the REST endpoint and data validation;
- `worker.py` - task handling and logic;
- `backends.py` - email backends to be used by the worker.

## How to run

Lock Python dependencies:

`poetry lock`

Build the app docker image:
`docker build -t celery_simple:latest .`

Launch the service ensemble:
`docker-compose up`
