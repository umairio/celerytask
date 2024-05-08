FROM python:3
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate --noinput
CMD ["./manage.py", "runserver", "0.0.0.0:8000"]