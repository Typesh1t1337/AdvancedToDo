FROM python:3.11

WORKDIR /usr/src/app

COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8003

CMD ["celery", "-A", "worker", "worker", "--loglevel=info"]