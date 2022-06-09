FROM python:3.9


WORKDIR /code/build
# RUN apt update -y && apt install nettools -y

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

ENV PYTHONPATH /code/build/app

#CMD ["python", "app/manage.py", "runserver", "0.0.0.0:8000"]
CMD ["gunicorn", "settings.wsgi", "--threads", "2", \
     "--workers", "4", "--log-level", "debug", "--max-requests", \
     "1000", "--timeout", "10", "--bind=0.0.0.0:8000"]