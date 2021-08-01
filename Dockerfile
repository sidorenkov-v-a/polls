FROM python:3.8.5

WORKDIR /code

COPY ./requirements.txt .

RUN pip install -r requirements.txt -U --no-deps

COPY . .

CMD bash -c "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn polls_project.wsgi:application --bind 0.0.0.0:8000 --timeout 120"
