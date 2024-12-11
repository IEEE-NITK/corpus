#!/bin/bash

# Configuration
DATE=$(date +"%Y-%m-%d_%H-%M-%S")
BACKUP_DIR="/backups"
DB_NAME=${POSTGRES_DB}
DB_USER=${POSTGRES_USER}
DB_PASSWORD=${POSTGRES_PASSWORD}
DB_HOST="postgres"
BACKUP_FILE="$BACKUP_DIR/db_backup_$DATE.dump"

# Export password for pg_dump
export PGPASSWORD=$DB_PASSWORD

# Create the backup
pg_dump -h $DB_HOST -U $DB_USER -F c $DB_NAME > $BACKUP_FILE

# Unset the password for security
unset PGPASSWORD

# Verify if the backup was successful
if [ $? -eq 0 ]; then
    echo "Database backup successful: $BACKUP_FILE"
else
    echo "Database backup failed!"
    exit 1
fi

# Upload to OneDrive using rclone
rclone copy $BACKUP_FILE onedrive_remote:/backups

# Optional: Delete local backups older than 7 days
find $BACKUP_DIR -type f -name "*.dump" -mtime +7 -exec rm {} \;