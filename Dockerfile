# IMPORTANT: This Dockerfile will be used by livecycle to
#            generate preview environments for pull requests.

FROM python:3.11.1-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create the working directory
RUN mkdir /corpus
WORKDIR /corpus

# Install dependencies
RUN apt-get update && \
    apt-get install -y gcc libpq-dev sqlite3 postgresql-client rclone && \
    apt-get clean

# Install Python dependencies
COPY corpus/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir python-dotenv==1.0.0

# Set environment variables
ENV LIVECYCLE 1
COPY env.example .env

# Copy the application
COPY corpus/ .

# Copy the backup script
COPY scripts/backup.sh /corpus/backup.sh

# Make scripts executable
RUN chmod +x start_dev.sh backup.sh

EXPOSE 8000
ENTRYPOINT [ "/corpus/start_dev.sh" ]