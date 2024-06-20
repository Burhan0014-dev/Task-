# Use the official Python image from the Docker Hub
FROM python:3.11

# Set unbuffered output for Python
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install app dependencies


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# FROM postgres:16-bookworm
# RUN apt-get update &&  \ 
#   apt-get -y install postgresql-16-cron && \ 
#   apt-get clean \ 
#   && rm -rf /var/lib/apt/lists/*

# # Install PostgreSQL and pg_cron
# RUN apt-get update && apt-get install -y postgresql-16.1-pg-cron

# Bundle app source
COPY . .

# Expose port
EXPOSE 8000

# Set the entrypoint to run the Django development server
ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]
