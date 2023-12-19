FROM python:3.7

RUN pip install Django djangorestframework


COPY . code
WORKDIR /code

EXPOSE 8000

ENTRYPOINT ["python", "server/manage.py"]
CMD ["runserver", "0.0.0.0:8000"]
