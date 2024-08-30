FROM python:3

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app/

# Set the environment variable
ENV DJANGO_SETTINGS_MODULE=chat_service.settings

CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "chat_service.asgi:application"]
