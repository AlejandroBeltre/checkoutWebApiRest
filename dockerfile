# Use an official Python runtime as a parent image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . /code/

# Create static directory
RUN mkdir -p /code/static

# Create database directory
RUN mkdir -p /code/data

# Set permissions for the database directory
RUN chmod 777 /code/data

# Collect static files
RUN python manage.py collectstatic --noinput

# Create database file
RUN touch /code/data/db.sqlite3
RUN chmod 666 /code/data/db.sqlite3

# Run migrations
RUN python manage.py migrate

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "checkoutWebApiRest.wsgi:application"]